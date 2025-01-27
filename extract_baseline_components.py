import os 
import config
import subprocess

def create_decomp_structure():
    parent_dir = "decompilations"
    
    os.makedirs(parent_dir,exist_ok=True)
    
    package_files = "decompilation_results"
    
    os.makedirs(package_files,exist_ok=True)

    directories = [
        "jce",
        "jsse",
        "jce/conscrypt/baseline",
        "jce/conscrypt/oem",
        "jsse/baseline",
        "jsse/oem"
    ]


    for directory in directories:
        os.makedirs(os.path.join(parent_dir, directory), exist_ok=True)
        
    os.makedirs('diffing_results', exist_ok=True)

def create_decomp_dest(hash_folder):

    if os.path.exists(hash_folder):
        if not os.listdir(hash_folder):
            script_path = os.path.join(current_path,'remove_folders.sh')
            
            subprocess_cmd = ['bash', script_path,hash_folder]
            
            subprocess.run(subprocess_cmd)
            
            return 'make'
        
        else:
            return 'no'
            
    else:
        return 'make'
   

def decomp_baseline(tag,baseline_path):

    for root, dirs, files in os.walk(baseline_path):
        for file in files:
            if file == 'core-oj.jar':
                core_path = os.path.join(root, file)
                
                target_folder = os.path.join(config.current_path,'decompilations/jsse/baseline')
                
                target_folder = os.path.join(target_folder,tag)
                
                result = create_decomp_dest(target_folder)
                
                if (result == 'make'):
                
                    script_path = os.path.join(config.current_path,'decompile_coreoj.sh')


                    subprocess_cmd = ['bash', script_path,core_path, target_folder]

                    subprocess.run(subprocess_cmd)
                
                    
                    
            if file == 'conscrypt.jar':
                core_path = os.path.join(root, file)
                
                target_folder = os.path.join(config.current_path,'decompilations/jce/conscrypt/baseline')
                
                target_folder = os.path.join(target_folder,tag)
                
                result = create_decomp_dest(target_folder)
            
                
                if (result == 'make'):
                
                    script_path = os.path.join(config.current_path,'decompile_coreoj.sh')

                    subprocess_cmd = ['bash', script_path,core_path, target_folder]

                    subprocess.run(subprocess_cmd)
                


def build_aosp(tag):
    baseline_path  = os.path.join(config.current_path,"AOSP_BUILDS",tag)
    
    if os.path.exists(baseline_path):
        print('Baseline exists',tag)

    else:
        print('We are building the baseline, this may take sometime',tag)
        
        android_version = tag

        script_path = os.path.join(config.current_path, 'AOSP_SOURCE','build_aosp.sh')

        subprocess_cmd = ['bash', script_path, android_version]

        subprocess.run(subprocess_cmd)
        
    decomp_baseline(tag,baseline_path)


def custom_split(value):
    if value.startswith('android-security-'):
        return value.split('android-security-')[1].split('.')[0]
    elif value.startswith('android-'):
        return value.split('android-')[1].split('.')[0]
    else:
        return value

def build_baseline(ver,fg):

    build_id = fg.split('/')[3]
    tag_row = config.androidTags[config.androidTags['build_id'] == build_id]
    if not(tag_row.empty):
        tag = tag_row['tag'].values[0]
        from_tag_version = custom_split(tag)
        if (from_tag_version != str(ver)):
            template = "android-{}.0.0_r1"
            tag = template.format(ver)
            return tag
        else:
            return tag
            
    else:
        template = "android-{}.0.0_r1"
        tag = template.format(ver)
        return tag



def find_build(device):
    build_props = []
    for root, dirs, files in os.walk(device):
        if 'build.prop' in files:
            path = os.path.join(root, 'build.prop')
            mark = " (possible)" if "system/" in path or "system_ext/" in path else ""
            build_props.append(f"{path}{mark}")
    return build_props
        

def read_build_prop(file_path):
    properties = {}
    keywords = ['build.id', 'version.release', 'version.sdk', 'system.manufacturer', 'build.fingerprint']
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().lower()  
                    matched_keyword = next((keyword for keyword in keywords if key.endswith(keyword)), None)
                    if matched_keyword:
                        properties[matched_keyword] = value.strip()
                        
    except:
        print(f"We are having issues with reading {file_path}")
           
    return properties