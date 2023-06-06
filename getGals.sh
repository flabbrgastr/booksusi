#!/bin/bash

# Function to display help information
show_help() {
    echo "Usage: getGals [options]"
    echo "Options:"
    echo "  -h        Display this help information"
    echo "  -i        Include images"
    echo "  -a        a only"
    echo "  -l        local storage, default is rsync"
    echo "  -f        folder, default is tar.gz"
    # Add more options and their descriptions as needed
}

# Check for the --help or -h argument
if [[ "$1" == "--h" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Read options from config file into an array
#mapfile -t html1arr < gals.config
# Read lines within [htmls] section until the last line or first empty line
declare -a htmls_lines=()
htmls_found=false

while IFS= read -r line || [[ -n "$line" ]]
do
    # Check for section header [htmls]
    if [[ $line == "[htmls]" ]]; then
        htmls_found=true
        continue
    fi
    # Check if [htmls] section is found and store lines until the last line or first empty line
    if [ "$htmls_found" = true ]; then
        if [[ -z "$line" ]]; then
            break  # Exit the loop when encountering an empty line
        fi
        html1arr+=("$line")
    fi
done < gals.conf

declare -A variables
variables_section=false
while IFS='=' read -r key value || [[ -n "$key" ]]
do
    # Check for section header [variables]
    if [[ $key == "[variables]" ]]; then
        variables_section=true
        continue
    fi
    # Check if in [variables] section and process variable assignments
    if [ "$variables_section" = true ]; then
        # Skip comments and empty lines
        if [[ $key =~ ^\s*# ]] || [[ -z "$key" ]]; then
            continue
        fi
        # Trim leading/trailing whitespace from key and value
        key=${key// /}
        value=${value// /}
        # Assign variable
        variables["$key"]="$value"
    fi
done < gals.conf

# Testmode
#if [ "$1" = "-t" ] || [ "$2" = "-t" ] || [ "$3" = "-t" ]; then
if [[ "$*" == *"-t"* ]]; then
   echo "Testmode"
  Testing=10
  # Print the variables
  for key in "${!variables[@]}"
  do
      value="${variables[$key]}"
      echo "$key=$value"
  done
else
  Testing=0
fi


user=$(whoami)

# wget args
arg1="-e robots=off"
arg2="-q -k -K --adjust-extension"
arg3="-U mozilla"
if [[ "$*" == *"-i"* ]]; then
# Check if the command-line argument is "-img"
   arg4="-nH -nd -p -H ${variables[arg4i]} "
   echo "include images"
else
   arg4="-nH -nd"
fi
arg5="--convert-links --random-wait"
args="${arg1} ${arg2} ${arg3} ${arg4} ${arg5}"

# wget args
#arg1="-e robots=off": This argument tells wget to ignore the robots.txt file on the server, which is a file that website owners use to control which parts of their site can be accessed by web crawlers. By setting robots=off, wget will not respect any crawling restrictions specified in the robots.txt file.
#arg2="-q -k -K --adjust-extension": This argument consists of several options:
#-q stands for quiet mode, which makes wget less verbose and reduces the amount of output displayed during the download.
#-k enables the conversion of the links in the downloaded HTML files so that they point to local files instead of the original URLs. This is useful for offline browsing or creating a local mirror of a website.
#-K forces the preservation of the original file suffix in case the server modifies it during download.
#--adjust-extension ensures that the file extension of downloaded files matches the actual content type, in case the server response doesn't provide an appropriate extension.
#arg3="-U mozilla": This argument sets the User-Agent header for the HTTP requests made by wget to "mozilla". The User-Agent header identifies the client (in this case, wget) to the server. By setting it to "mozilla", wget emulates the behavior of the Mozilla web browser, which may be useful to handle certain server responses that are browser-specific.
#arg4="-p -nH -nd -H --domain=images.book.com ": This argument contains the following options:
#-p enables the download of all necessary files to display an HTML page properly, including CSS, JavaScript, and images.
#-nH prevents the creation of a directory hierarchy in the local filesystem. By default, wget creates a directory structure that mimics the server's structure. With this option, all files are downloaded to the current directory.
#-nd disables the creation of directories altogether, ensuring that all downloaded files are saved directly in the current directory.
#-H allows spanning across hosts, meaning that wget will follow links that lead to other domains.
#--domain=images.book.com restricts the spanning across hosts to only include the specified domain, in this case, "images.book.com".
#arg5="--convert-links --random-wait": This argument includes two options:
#--convert-links makes wget convert the links in the downloaded HTML files so that they point to local files. This is similar to the -k option mentioned earlier but does not modify the original files.
#--random-wait adds a random delay between requests to the server, which can help to avoid overloading the server or getting blocked for making too many consecutive requests.


# Check for the -a argument
if [[ "$*" == *"-a"* ]]; then
   # anal only
   keyword="an"
   filtered_arr=()
   for option in "${html1arr[@]}"
   do
      if [[ $option == *"$keyword"* ]]; then
        filtered_arr+=("$option")
      fi
   done
   # Update html1arr with filtered_arr values
   html1arr=("${filtered_arr[@]}")
fi

# when less then GalsinPage then it is assumed to be last page
GalsinPage="${variables[GalsinPage]}"
html0="${variables[html0]}"
html2="${variables[html2]}"
datum=$(date +%Y-%m-%d_%H%M%S)
out_dir=./data/$datum
arg_out=" -P"${out_dir}"/"

echo "Getting Gals on $datum"
echo "[ ${html1arr[@]} ]"
echo ""

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

#delete all directories and files older than N days
find ./data/ -mtime ${variables[N]} -delete

# python booksi_a_42.py d

# renamin images
./renamejpgs.sh $out_dir
cd ./data/
#echo tar $datum/ to datum.tar.gz
tar -zcf $datum.tar.gz $datum/

if [[ "$*" != *"-f"* ]]; then # if not local storage
   rm -rf $datum/             # delete folder to save space on local storage
fi

if [ "$Testing" != 0 ]; then
  echo "testmode"
else
   if [[ "$*" != *"-l"* ]]; then
      echo "rcloning to gdrive"
      rclone  copy $datum.tar.gz fgdrive:/
      cd ..
   fi
fi
echo "finished, enjoy!"
exit 0

