#!/bin/bash

# Function to display help information
show_help() {
    echo "Usage: getGals [options]"
    echo "Options:"
    echo "  -h        Display this help information"
    echo "  -i        Include images"
    echo "  -a        Anal only"
    # Add more options and their descriptions as needed
}

# Check for the --help or -h argument
if [[ "$1" == "--h" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi


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
# Check if the command-line argument is "-img"
if [ "$1" = "-i" ] || [ "$2" = "-i" ] || [ "$3" = "-i" ]; then
   arg4="-p -nH -nd -H --domain=images.booksusi.com "
   echo "include images"
else
   arg4="-nH -nd"
   echo "no images"
fi
#arg4="-p -nH -nd -H --domain=images.booksusi.com "
#arg4="-nH -nd "
arg5="--convert-links --random-wait"
args="${arg1} ${arg2} ${arg3} ${arg4} ${arg5}"
# wget args
#arg1="-e robots=off": This argument tells wget to ignore the robots.txt file on the server, which is a file that website owners use to control which parts of their site can be accessed by web crawlers. By setting robots=off, wget will not respect any crawling restrictions specified in the robots.txt file.
#
#arg2="-q -k -K --adjust-extension": This argument consists of several options:
#
#-q stands for quiet mode, which makes wget less verbose and reduces the amount of output displayed during the download.
#-k enables the conversion of the links in the downloaded HTML files so that they point to local files instead of the original URLs. This is useful for offline browsing or creating a local mirror of a website.
#-K forces the preservation of the original file suffix in case the server modifies it during download.
#--adjust-extension ensures that the file extension of downloaded files matches the actual content type, in case the server response doesn't provide an appropriate extension.
#arg3="-U mozilla": This argument sets the User-Agent header for the HTTP requests made by wget to "mozilla". The User-Agent header identifies the client (in this case, wget) to the server. By setting it to "mozilla", wget emulates the behavior of the Mozilla web browser, which may be useful to handle certain server responses that are browser-specific.
#
#arg4="-p -nH -nd -H --domain=images.book.com ": This argument contains the following options:
#
#-p enables the download of all necessary files to display an HTML page properly, including CSS, JavaScript, and images.
#-nH prevents the creation of a directory hierarchy in the local filesystem. By default, wget creates a directory structure that mimics the server's structure. With this option, all files are downloaded to the current directory.
#-nd disables the creation of directories altogether, ensuring that all downloaded files are saved directly in the current directory.
#-H allows spanning across hosts, meaning that wget will follow links that lead to other domains.
#--domain=images.book.com restricts the spanning across hosts to only include the specified domain, in this case, "images.book.com".
#arg5="--convert-links --random-wait": This argument includes two options:
#--convert-links makes wget convert the links in the downloaded HTML files so that they point to local files. This is similar to the -k option mentioned earlier but does not modify the original files.
#--random-wait adds a random delay between requests to the server, which can help to avoid overloading the server or getting blocked for making too many consecutive requests.


# when less then GalsinPage then it is assumed to be last page
GalsinPage=23
#declare -a html1arr=("analsex" "anal_natur_no_condom" "gesichtsbesamung_cum_on_face" "mundvollendung_cum_in_mouth")
# Check for the -a argument
if [ "$1" = "-a" ] || [ "$2" = "-a" ] || [ "$3" = "-a" ]; then
   # anal only
   declare -a html1arr=("analsex" "anal_natur_no_condom")
else
   declare -a html1arr=("analsex" "anal_natur_no_condom" "gesichtsbesamung_cum_on_face" "mundvollendung_cum_in_mouth")
fi

# for testing
if [ "$1" = "-t" ] || [ "$2" = "-t" ] || [ "$3" = "-t" ]; then
  Testing=10
else
  Testing=0
fi


html0="https://booksusi.com/service/"
html2="/?&city=wien&page="
sumGals=0

datum=$(date +%Y-%m-%d_%H%M%S)
out_dir=./data/$datum
arg_out=" -P"${out_dir}"/"

echo "GetGals $datum"
echo "[ ${html1arr[@]} ]"
echo

for i in "${html1arr[@]}"; do
   echo -n "$i "
   x=1
   sumGals=0
   Gals=$GalsinPage
   while [ $Gals -ge ${GalsinPage} ]; do
      wget ${args}$arg_out $html0$i$html2$x
      file=${out_dir}"/"$i$x.html
      mv ${out_dir}"/"index*$x.html $file
      sed -n -i '/<body>/,/<\/body>/p' ${out_dir}"/"$i$x.html
      Gals=$(grep -o "listing" $file | wc -l)
      Gals=$(( $Gals - $Testing ))
      sumGals=$(( $Gals + $sumGals ))
#      echo -n "$Gals."
      echo -n "."
      x=$(( $x + 1 ))

   done
   echo "$sumGals"
done

echo "cleaning up"
cd $out_dir
rm *.orig *.svg *.css *.css?* *.js?* *.jpg *.png *.[0-9] *.[0-9][0-9] 2>/dev/null
cd ..//..

#delete all directories older than 30 days
find ./data/ -type d -ctime +30 -exec rm -rf {} +

# python booksi_a_42.py d

# renamin images
./renamejpgs.sh $out_dir
cd ./data/
#echo tar $datum/ to datum.tar.gz
tar -zcf $datum.tar.gz $datum/
rm -rf $datum/
# Check if either of the two variables equals "-t"
if [ "$Testing" != 0 ]; then
  echo "testmode"
else
  echo "rcloning to gdrive"
  rclone  copy $datum.tar.gz fgdrive:/
  cd ..
  echo "finished, enjoy!"
fi
exit 0

