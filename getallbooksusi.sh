#!/bin/bash

#greeting="Welcome"
user=$(whoami)
#echo "$greeting $user"
# Anal 6
# https://booksusi.com/service/analsex/?&city=wien&service=2&page=
# Anal Natur 3
# https://booksusi.com/service/anal_natur_no_condom/?&city=wien&service=12&page=
# COF 7
# https://booksusi.com/service/gesichtsbesamung_cum_on_face/?&city=wien&service=12&page=
# CIM 9
# https://booksusi.com/service/mundvollendung_cum_in_mouth/?&city=wien&service=13&page=


# wget args
arg1="-e robots=off"
arg2="-k -K --adjust-extension -I /files"
arg3="-U mozilla"
arg4="-p -nH -nd"
arg5="--convert-links --random-wait"

args="${arg1} ${arg2} ${arg3} ${arg4} ${arg5}"
echo "$args"

declare -a html1arr=("analsex" "anal_natur_no_condom" "gesichtsbesamung_cum_on_face" "mundvollendung_cum_in_mouth")
declare -a html_pages=(6 3 7 9)
#declare -a html_pages=(1 1 1 1)

datum=$(date +%Y-%m-%d_%H%M%S)

# html="https://booksusi.com/service/analsex/?&city=wien&service=2&page="
html0="https://booksusi.com/service/"
html2="/?&city=wien&page="

#for i in "${html1arr[@]}"
for i in 0 1 2 3; do
#   echo "$html0${html1arr[i]}$html2"	#url name
#   echo "${html_pages[i]}" 
   echo "##.................................................##"
   echo "###   ${html1arr[i]}   ${html_pages[i]} pages"
   echo "##.................................................##"
a
   out_dir=./data/booksusi_${html1arr[i]}_$datum
   arg_out=" -P"${out_dir}"/"
   # or do whatever with individual element of the array
   x=1
   while [ $x -le ${html_pages[i]} ]; do
     wget ${args}$arg_out $html0${html1arr[i]}$html2$x
     mv ${out_dir}"/"index*$x.html ${out_dir}"/"index_${html1arr[i]}$x.html
     rm ${out_dir}"/"index*$x.html
     x=$(( $x + 1 ))
   done
done
# cleaning up
rm ${out_dir}"/*.orig"
rm ${out_dir}"/banner*.jpg"
