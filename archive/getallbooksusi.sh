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
arg2="-q -k -K --adjust-extension -I /files"
arg3="-U mozilla"
arg4="-p -nH -nd"
arg5="--convert-links --random-wait"
args="${arg1} ${arg2} ${arg3} ${arg4} ${arg5}"
GalsinPage=25
declare -a html1arr=("analsex" "anal_natur_no_condom" "gesichtsbesamung_cum_on_face" "mundvollendung_cum_in_mouth")

Testing=0

datum=$(date +%Y-%m-%d_%H%M%S)
html0="https://booksusi.com/service/"
html2="/?&city=wien&page="

echo "Getallbooksusi Page Downloading Script"
echo "Downloading [ ${html1arr[@]} ] into ./data/$datum..."

#for i in "${html1arr[@]}"
for i in 0 1 2 3; do
   echo -n "${html1arr[i]} "
   out_dir=./data/$datum
   arg_out=" -P"${out_dir}"/"
   x=1
   Gals=25
   while [ $Gals -ge ${GalsinPage} ]; do
      wget ${args}$arg_out $html0${html1arr[i]}$html2$x
      file=${out_dir}"/"${html1arr[i]}$x.html
      mv ${out_dir}"/"index*$x.html $file
      sed -n -i '/<body>/,/<\/body>/p' ${out_dir}"/"${html1arr[i]}$x.html
      Gals=$(grep -o "listing" $file | wc -l)
      Gals=$(( $Gals - $Testing ))
      echo -n "$Gals."
      x=$(( $x + 1 ))
   done
   echo
done
cd $out_dir
echo "cleaning up..."
rm *.orig
rm *.jpg*
#rm -v !"*.html"
echo "Contents of $(pwd):"
ls
#ls -1 | sed -e 's/\..*$//'
cd ..//..


#deleta all directories older than 3 days
# find ./data/ -type d -ctime +3 -exec rm -rf {} +

# python booksi_a_42.py d



#echo "rsyncing to drive"
#sleep 2s
rclone -v copy ./data/$datum fgdrive:/$datum
#--max-age 1d

echo "finished, enjoy!"
