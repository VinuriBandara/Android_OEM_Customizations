import pandas as pd
import json
import numpy as np
import os
import subprocess
import hashlib
import re
import ssdeep
import difflib
from colorama import Fore

import extract_baseline_components as baseline_extract
import config
import diffing
import extract_boringssl_diff


def main():
    
    baseline_extract.create_decomp_structure() 

    directory = input("Enter the firmware image directory: ")
    
    print(Fore.CYAN +"Establishing baseline")
    
    print(Fore.RESET)
    
    build_props = baseline_extract.find_build(directory)
    
    if not build_props:
        print("No build.prop files found.")
        build_fingerprint = input("Enter the build fingerprint of the device: ")
        version = input("Enter the version the device is running on: ")

    else:
        print("Found build.prop files:")
        for i, path in enumerate(build_props, 1):
            print(f"{i}. {path}")
        
        choice = input("\nSelect the number of the build.prop file to use or enter 'None' to manually input the build fingerprint and version: ")
        if choice.lower() == 'none':
            build_fingerprint = input("Enter the build fingerprint of the device: ")
            version = input("Enter the version the device is running on: ")
        else:
            choice = int(choice)
            selected_file = build_props[choice - 1].split(' (possible)')[0]
            print(f"\nProceeding with build.prop: {selected_file}")

            properties = baseline_extract.read_build_prop(selected_file)
        
            if (properties.get('build.fingerprint')):
                build_fingerprint = properties['build.fingerprint']
            else:
                build_fingerprint = input("We can't detect the fingerprint, enter manually: ")
                
            if (properties.get('version.release')):
                version = properties['version.release']
            else:
                version = input("We can't detect the version, enter manually: ")
                
        
    print(f"\nUsing metadata: {build_fingerprint} with version {version} to establish the baseline")
            
    baseline = baseline_extract.build_baseline(version,build_fingerprint)
    
    print(Fore.GREEN + f"\nUsing {baseline} as baseline")
    print(Fore.RESET)
    
#     Check if baseline exists or build baseline---might take few hours and then decompile the networking components
    
    baseline_extract.build_aosp(baseline)

#     Move to decompilation of the network components
    
    print(Fore.CYAN + "\nJava based diffing---JSSE, JCE") 
    print(Fore.RESET)
    diffing.diff_network_components(directory,baseline)
    
    
    print(Fore.CYAN + "\nJCA diffing")
    print(Fore.RESET)
    extract_boringssl_diff.diff_binaries(directory,baseline)
    
if __name__ == "__main__":
    main()