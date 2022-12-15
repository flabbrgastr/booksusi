#!/bin/bash
#out_dir=./data/_2022-12-13_114915
out_dir=$1

# all the ugly jpgs
# containing square-small.jpg?0123456789
files=($(ls $out_dir/*.jpg?* 2>/dev/null)) 

echo renaming "${#files[@]}" 

for file in "${files[@]}";do
    # echo $file
    newfile=${file/.jpg?/_}
    mv $file $newfile.jpg
done
echo done

# adding .jpg ending


# removing the .jpg? string