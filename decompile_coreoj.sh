#!/bin/bash

file_jar=$1

target_folder=$2

current_path=$(pwd)

full_jar_path="$current_path/tools/baksmali-2.5.2.jar"


java -jar $full_jar_path dis $file_jar -o "$target_folder"

if [ $? -ne 0 ]; then

    echo "Error during baksmali disassembly for $file_jar"

else
    echo "Baksmali disassembly successful for $file_jar"
fi