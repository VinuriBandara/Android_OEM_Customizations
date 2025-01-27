import os
import subprocess
import json
import re
import config

def get_defined_functions(file_path):
    try:
        result = subprocess.check_output(["nm", "-DC", "--defined-only", "--format=posix", file_path], text=True)
        lines = result.splitlines()
        t_functions = {line.split()[0] for line in lines if ' T ' in line}
        return t_functions
    except subprocess.CalledProcessError as e:
        print(f"Failed to process file {file_path}: {e}")
        return set()
    
    
def get_defined_diff(oem_set, aosp_set):
    compiler_pattern = re.compile(
        r'^_Unwind_|^___Unwind_|^__gnu_unwind_|^__aeabi_|^__gnu_|^__cxa_|^unw_|^__udiv|^__aeabi_uidiv'
    )

    filtered_oem_set = {item for item in oem_set if not compiler_pattern.match(item)}
    filtered_aosp_set = {item for item in aosp_set if not compiler_pattern.match(item)}

    vendor_only = filtered_oem_set - filtered_aosp_set
    aosp_only = filtered_aosp_set - filtered_oem_set

    return vendor_only, aosp_only


def find_boring_files(start_path, file_names, target_subdirs):
    found_files = {}
    len_start_path = len(start_path)
    for root, dirs, files in os.walk(start_path):
        for subdir in target_subdirs:
            if subdir in root[len_start_path:]:
                for file in files:
                    if file in file_names:
                        relative_path = os.path.relpath(root, start_path)
                        key = os.path.join(subdir, file)
                        found_files[key] = os.path.join(root, file)
    return found_files


def diff_binaries(device, baseline):
    file_names = ['libssl.so', 'libcrypto.so']
    target_subdirs = ['system/lib', 'system/lib64', 'system_ext/lib', 'system_ext/lib64']

    device_path = device
    baseline_path = os.path.join(config.current_path, "AOSP_BUILDS", baseline)

    device_files = find_boring_files(device_path, file_names, target_subdirs)
    baseline_files = find_boring_files(baseline_path, file_names, target_subdirs)
    

    diff_results={}

    for key in device_files:
        if key in baseline_files:
            device_binary = device_files[key]
            baseline_binary = baseline_files[key]
            
            
            device_defined_functions = get_defined_functions(device_binary)
            baseline_defined_functions = get_defined_functions(baseline_binary)
            
            vendor_only_set, aosp_only_set = get_defined_diff(device_defined_functions, baseline_defined_functions)
            
            diff_results[key] = {
                "vendor_only_functions": list(vendor_only_set),
                "aosp_only_functions": list(aosp_only_set)
            }


    output_path = os.path.join(config.current_path,'diffing_results',os.path.basename(device),'boringssl_diffing.json')
    with open(output_path, 'w') as json_file:
        json.dump(diff_results, json_file, indent=4)