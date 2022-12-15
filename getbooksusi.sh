#!/bin/bash

#greeting="Welcome"
user=$(whoami)
#echo "$greeting $user"

html="https://booksusi.com/service/analsex/?&city=wien&service=2&page="
html0="https://booksusi.com/service/"
html1="analsex"
html2="/?&city=wien&page="
# Anal
# https://booksusi.com/service/analsex/?&city=wien&service=2&page=
# Anal Natur
# https://booksusi.com/service/anal_natur_no_condom/?&city=wien&service=12&page=
# COF
# https://booksusi.com/service/gesichtsbesamung_cum_on_face/?&city=wien&service=12&page=
# CIM
# https://booksusi.com/service/mundvollendung_cum_in_mouth/?&city=wien&service=13&page=


#`wget --random-wait -r -p -e robots=off -U mozilla http://www.example.com

# home_dir=/home/${user}
# out_dir=${home_dir}/coding/data/booksusi_analsex_$(date +%Y-%m-%d_%H%M%S)
out_dir=./data/$(date +%Y-%m-%d_%H%M%S)
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
    cp ${out_dir}"/"index*$i.html ${out_dir}"/"$html1$i.html
done

cd $out_dir
pwd

