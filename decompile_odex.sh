#!/bin/bash

file_odex=$1

target_folder=$2

full_jar_path="$current_path/tools/baksmali-2.5.2.jar"

java -jar $full_jar_path dis "$file_odex" -o "$target_folder"

if [ $? -ne 0 ]; then
    echo "Error during baksmali disassembly for $file_odex"
else
    echo "Baksmali disassembly successful for $file_odex"
fi