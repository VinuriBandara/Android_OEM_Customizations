#!/bin/bash

set -e

CURRENT_PATH=$(pwd)

BASE_DIR="${CURRENT_PATH}/AOSP_SOURCE"

mkdir -p "${BASE_DIR}/bin"


curl https://storage.googleapis.com/git-repo-downloads/repo > "${BASE_DIR}/bin/repo"


chmod a+x "${BASE_DIR}/bin/repo"


ANDROID_VERSION=$1


cd "${BASE_DIR}"


python3 "${BASE_DIR}/bin/repo" init -u https://android.googlesource.com/platform/manifest -b "$ANDROID_VERSION"


python3 "${BASE_DIR}/bin/repo" sync -j12


source "${BASE_DIR}/build/envsetup.sh"


lunch aosp_arm-eng


make -j8


OUTPUT_DIR="${BASE_DIR}/AOSP_BUILDS/$ANDROID_VERSION"

mkdir -p "$OUTPUT_DIR"


cp -r out/target/product/generic/system "$OUTPUT_DIR"

rm -rf out