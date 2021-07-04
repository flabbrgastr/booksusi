#!/bin/bash

#greeting="Welcome"
user=$(whoami)
#echo "$greeting $user"

html="https://booksusi.com/service/analsex/?&city=wien&service=2&page="

#`wget --random-wait -r -p -e robots=off -U mozilla http://www.example.com

home_dir=/home/${user}
out_dir=${home_dir}/coding/data/booksusi_analsex_$(date +%Y-%m-%d_%H%M%S)
out_file=booksusi

#echo "$html1 $out_dir $out_file" 

arg1="-e robots=off"
arg2="-k -K --adjust-extension -I /files"
arg3="-U mozilla"
arg4="-p -nH -nd -P"${out_dir}"/"
arg5="--convert-links --random-wait"

args="${arg1} ${arg2} ${arg3} ${arg4} ${arg5}"
echo "args ${args}"

#echo "wget ${args} --output-document=${out_dir}/${out_file}_$i.html ${html}$i"
echo "wget ${args} --output-document=${out_file}$i.html ${html}$i"


for i in 1 2 3 4 5 6; do
#    wget --output-document=${out_dir}/${out_file}_$i.html ${html}$i
#    wget ${args} --output-document=${out_file}_$i.html ${html}$i
    wget ${args} ${html}$i
    cp ${out_dir}"/"index*$i.html ${out_dir}"/"index_$i.html
done
