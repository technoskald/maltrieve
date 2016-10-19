#!/bin/sh

root_dir="/root/Downloads/hp_pulls/"
all_files="$root_dir*"
for file in $all_files
do
  if [ -f $file ]; then
    outstring=($(eval file $file))
    stringsubone="${outstring[1]}"
  
  if [ ! -d $root_dir$stringsubone ]; then
      mkdir -p "$root_dir$stringsubone"
  fi
    mv $file "$root_dir$stringsubone/"
 fi
done

