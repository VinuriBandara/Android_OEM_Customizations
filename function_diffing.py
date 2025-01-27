import os 
import re


def extract_method_names(smali_code):
    method_names = []
    pattern = r'\.method (.*?)\('

    for line in smali_code.splitlines():
        match = re.match(pattern, line)
        if match:
            method_name = match.group(1)
            method_names.append(method_name)
    return method_names

def diff_function_level(base, directory):
    
    prefixes = ('access$','lambda', '-','<')
    
    baseline_methods = {}
    oem_methods = {}

    for root, dirs, files in os.walk(base):
        for file in files:
                file_path = os.path.join(root, file)
               
                relative_path = os.path.relpath(file_path, start=base)
                base_class_name = '/'.join(relative_path.split(os.sep)[1:])  
                base_class_name = base_class_name.split('$')[0] if '$' in base_class_name else base_class_name[:-6] 

                with open(file_path, "r") as smali_file:
                    smali_code = smali_file.read()
                    method_names = extract_method_names(smali_code)
                    simple_method_names = {method_name.split()[-1] for method_name in method_names}

                    if base_class_name not in baseline_methods:
                        baseline_methods[base_class_name] = simple_method_names
                    else:
                        baseline_methods[base_class_name].update(simple_method_names)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".smali"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start=directory)
                base_class_name = '/'.join(relative_path.split(os.sep)[1:]) 
                base_class_name = base_class_name.split('$')[0] if '$' in base_class_name else base_class_name[:-6]

                if os.path.exists(file_path):
                    with open(file_path, "r") as smali_file:
                        smali_code = smali_file.read()
                        method_names = extract_method_names(smali_code)
                        simple_method_names = {method_name.split()[-1] for method_name in method_names}

                        if base_class_name not in oem_methods:
                            oem_methods[base_class_name] = simple_method_names
                        else:
                            oem_methods[base_class_name].update(simple_method_names)
                            

    differences_json = []
    for class_name, baseline_class_methods in baseline_methods.items():
        if class_name in oem_methods:
            oem_class_methods = oem_methods[class_name]
            
            baseline_class_methods = {method for method in baseline_class_methods if not method.startswith(prefixes)}
            oem_class_methods =  {method for method in oem_class_methods if not method.startswith(prefixes)}
            
            differences = baseline_class_methods.symmetric_difference(oem_class_methods)

            if differences:
                only_aosp_methods = list(differences.intersection(baseline_class_methods))
 
                only_oem_methods = list(differences.intersection(oem_class_methods))
 
                class_diff = {
                    "class_name": class_name,
                    "only_aosp_methods": only_aosp_methods,
                    "only_oem_methods": only_oem_methods
                }
                differences_json.append(class_diff)
                
    return differences_json