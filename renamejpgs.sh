#!/bin/bash

out_dir=$1

files=($(ls $out_dir/*.jpg?* 2>/dev/null)) 

# renaming jpgs
for file in "${files[@]}";do
    # echo $file
    newfile=${file/.jpg?/_}
    mv $file $newfile.jpg
done
#echo done
