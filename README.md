# Android Vendor Customizations
We present a scalable pipeline for extracting Android Vendor/Manufacturer introduced API level customizations to Java and Native level packages. Currently the scope is limited to Android networking stack.

## Methodology Overview

This project analyzes vendor customizations in Android's cryptographic and networking components by comparing vendor-specific implementations against the corresponding AOSP baseline. The methodology follows a structured pipeline that includes firmware extraction, version detection, differential analysis, and customization impact assessment. 

1. Data Collection
  - Input: Android firmware images or system dumps.
  - Process: The [Firmware Scanner](https://play.google.com/store/apps/details?id=org.imdea.networks.iag.preinstalleduploader&pcampaignid=web_share) extracts system components, collecting relevant package and configuration data.

2. Version Detection & AOSP Baseline Matching
  - The extracted build information (e.g., build.prop) determines the Android version.
  - A corresponding **AOSP build** is identified and used as the baseline for comparison.

3. Vendor Package Extraction
  - Vendor-specific cryptographic and networking components are extracted for differential analysis.
   
4. Differential Analysis

  - Identifying modifications to key security-related libraries: JSSE, JCE (Conscrypt) and JCA (BoringSSL).

6. Customization Impact Assessment

  - The extracted differences provide insights into how vendor modifications affect:
    - Network security and TLS behavior
    - Cryptographic functionality and API compatibility
    - Potential security risks introduced by vendor-specific changes
   
## Prerequisites

Make sure your machine meets the following requirements:

- Disk Space: At least 400 GB of free disk space (250 GB to check out + 150 GB to build Android images).
- Software Packages: Install the required packages from the Android Open Source Project and these additional Python libraries:
    - pandas
    - numpy
    - ssdeep
    - colorama
    - pyOpenSSL

## Running the Pipeline

1. Download OEM Firmware Images:

  - Navigate to the firmware_images/ directory.
  - We provide two sample Android images, you can find more Android images in Android dumps or alternatives. 

    
2. Prepare AOSP Images:

  - We provide 5 baseline AOSP images for major Android releases in the AOSP_BUILDS/ folder.
  - If your target Android image is built on a different AOSP baseline, the pipeline will build it for you (This might take a few hours).

3. Execute the Pipeline:

  - Run the main.py file and follow the on-screen prompts.
  - Establish the baseline and proceed with the diffing process.
    
4. Review Results:
   
  - All results will be stored in the diffing_results/ folder under the name of your input folder.
