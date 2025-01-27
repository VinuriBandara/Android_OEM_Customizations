import subprocess
import config
import os
import hashlib

def decomp_exec(exec_file, hash_path):

    if exec_file.endswith('.oat'):
        
            script_path = os.path.join(config.current_path,'decompile_oats.sh')
            
            subprocess_cmd = ['bash', script_path ,exec_file, hash_path]
            
            subprocess.run(subprocess_cmd)

        
        
    if exec_file.endswith('.jar'):
        
            script_path = os.path.join(config.current_path,'decompile_coreoj.sh')
            
            subprocess_cmd = ['bash', script_path,exec_file, hash_path]
            
            subprocess.run(subprocess_cmd)
            

        
            
    if exec_file.endswith('.odex'):
        
            script_path = os.path.join(config.current_path,'decompile_odex.sh')
            
            subprocess_cmd = ['bash', script_path,exec_file, hash_path]
            
            subprocess.run(subprocess_cmd)

def create_decomp_dest(hash_folder):

    if os.path.exists(hash_folder):
        if not os.listdir(hash_folder):
            script_path = os.path.join(config.current_path,'remove_folders.sh')
            
            subprocess_cmd = ['bash', script_path,hash_folder]
            
            subprocess.run(subprocess_cmd)
            
            return 'make'
        
        else:
            return 'no'
            
    else:
        return 'make'
    
def calc_hash(files):
    hash_val = hashlib.md5(open(files,'rb').read()).hexdigest()
    return hash_val
        
    
    

def extract_jsse(device):
    folder_path = device
    file_names = ['core-oj.jar','boot.oat']

    dest_parent = os.path.join(config.current_path,'decompilations/jsse')
    
    dest_vendor = 'oem'
    
    matching_files = []
    

    with open(os.path.join(config.current_path,'decompilation_results/files_jsse.txt'), 'a') as f0:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                for file_name in file_names:
                    if file == file_name:
                        full_path = os.path.join(root, file)
                        hash_file = calc_hash(full_path)
                        f0.write("Device:{}\t Hash Value: {}\t Matched File: {}\n".format(device,hash_file, full_path))
                        matching_files.append(full_path)
                    
                    
    
    with open(os.path.join(config.current_path,'decompilation_results/hashes_jsse.txt'), 'a') as f1:
        if (matching_files != []):
            for matched_file in matching_files:
 
                hash_val = calc_hash(matched_file)
                
                hash_folder = os.path.join(dest_parent, dest_vendor, hash_val)

                result = create_decomp_dest(hash_folder)

                if (result == 'make'):
                    decomp_exec(matched_file, hash_folder)

                    if (os.path.exists(hash_folder)):
                         f1.write("Hash Value: {}\t Matched File: {}\n".format(hash_val, full_path))

                else:

                    print('We are skipping decompilation, we have the decompiled package in our database', hash_folder)
                    
                return hash_folder
            
        else:
            return None

    
        
def extract_conscrypt(device):
    
    folder_path = device
    file_names = ['conscrypt.jar','boot-conscrypt.oat','conscrypt.odex']
    
    dest_parent = os.path.join(config.current_path,'decompilations/jce/conscrypt')
    
    dest_vendor = 'oem'
    
    matching_files = []
    
    
    with open(os.path.join(config.current_path,'decompilation_results/files_conscrypt.txt'), 'a') as f0:
        for root, dirs, files in os.walk(folder_path):
            for file in files:

                for file_name in file_names:
                    if file == file_name:
                        full_path = os.path.join(root, file)
#                         print("Found file",full_path)
                        hash_file = calc_hash(full_path)
                        f0.write("Device:{}\t Hash Value: {}\t Matched File: {}\n".format(device,hash_file, full_path))
                        matching_files.append(full_path)
                        
                   
    with open(os.path.join(config.current_path,'decompilation_results/hashes_conscrypt.txt'), 'a') as f1:                 
        if (matching_files != []):
            for matched_file in matching_files:
                print(matched_file)

                hash_val = calc_hash(matched_file)

                hash_folder = os.path.join(dest_parent, dest_vendor, hash_val)


                result = create_decomp_dest(hash_folder)

                if (result == 'make'):

                    decomp_exec(matched_file, hash_folder)

                    if (os.path.exists(hash_folder)):
                        f1.write("Hash Value: {}\t Matched File: {}\n".format(hash_val, full_path))

                else:

                    print('We are skipping decompilation, we have the decompiled package in our database', hash_folder)
           
            return hash_folder
                
        else:
            return None