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
arg2="-q -k -K --adjust-extension"
arg3="-U mozilla"
arg4="-p -nH -nd -H --domain=images.booksusi.com "
arg5="--convert-links --random-wait"
args="${arg1} ${arg2} ${arg3} ${arg4} ${arg5}"
GalsinPage=23
#declare -a html1arr=("anal_natur_no_condom")
#declare -a html1arr=("analsex" "anal_natur_no_condom" "gesichtsbesamung_cum_on_face" "mundvollendung_cum_in_mouth")
declare -a html1arr=("analsex" "anal_natur_no_condom")

Testing=0

datum=$(date +%Y-%m-%d_%H%M%S)
html0="https://booksusi.com/service/"
html2="/?&city=wien&page="

#echo "Getallbooksusi Page Downloading Script"
echo "Downloading [ ${html1arr[@]} ]"

for i in "${html1arr[@]}"; do
#for i in 0 1; do
   echo -n "getting $i "
   out_dir=./data/$datum
   arg_out=" -P"${out_dir}"/"
   x=1
   Gals=$GalsinPage
   while [ $Gals -ge ${GalsinPage} ]; do
      wget ${args}$arg_out $html0$i$html2$x
      file=${out_dir}"/"$i$x.html
      mv ${out_dir}"/"index*$x.html $file
      sed -n -i '/<body>/,/<\/body>/p' ${out_dir}"/"$i$x.html
      Gals=$(grep -o "listing" $file | wc -l)
      Gals=$(( $Gals - $Testing ))
      echo -n "$Gals."
      x=$(( $x + 1 ))

   done
   echo
done

cd $out_dir
echo "cleaning up..."
rm *.orig *.svg *.css *.css?* *.js?* *.jpg *.png *.[0-9] *.[0-9][0-9] 2>/dev/null
cd ..//..

#delete all directories older than 3 days
# find ./data/ -type d -ctime +3 -exec rm -rf {} +

# python booksi_a_42.py d

# renamin images
./renamejpgs.sh $out_dir

#echo "rsyncing to drive"
#sleep 2s
#rclone -v copy ./data/$datum fgdrive:/$datum
#--max-age 1d

cd ./data/
echo tar $datum/ to datum.tar.gz
tar -zvcf $datum.tar.gz $datum/
echo rcloning to gdrive
rclone  copy $datum.tar.gz fgdrive:/
cd ..
echo "finished, enjoy!"
