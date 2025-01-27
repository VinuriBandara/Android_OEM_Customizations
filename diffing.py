import os
import json
from colorama import Fore

import config
import extract_oem_components as oem_extraction
import function_diffing as fdiffing


def save_results_as_json(results, filename):
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)

        

def diff_network_components(device,baseline):

    results_directory = os.path.join(config.current_path, 'diffing_results', os.path.basename(device))
    os.makedirs(results_directory, exist_ok=True)

    # JSSE Diffing
    print(Fore.LIGHTRED_EX + "\nJSSE extraction and diffing")
    print(Fore.RESET)
    decompiled_jsse = oem_extraction.extract_jsse(device)
    if decompiled_jsse:
        decompiled_baseline_jsse = os.path.join(config.current_path, 'decompilations/jsse/baseline', baseline)
        function_results = fdiffing.diff_function_level(decompiled_baseline_jsse, decompiled_jsse)
        save_results_as_json(function_results, os.path.join(results_directory, "jsse_diff.json"))

    # Conscrypt Diffing
    print(Fore.LIGHTRED_EX + "\nConscrypt extraction and diffing")
    print(Fore.RESET)
    decompiled_conscrypt = oem_extraction.extract_conscrypt(device)
    if decompiled_conscrypt:
        decompiled_baseline_conscrypt = os.path.join(config.current_path, 'decompilations/jce/conscrypt/baseline', baseline)
        function_results = fdiffing.diff_function_level(decompiled_baseline_conscrypt, decompiled_conscrypt)
        save_results_as_json(function_results, os.path.join(results_directory, "conscrypt_diff.json"))