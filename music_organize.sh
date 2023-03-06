#!/bin/sh

# get user path name
echo 'Enter directory name of music files to process'
read path_var

# for song_file in $(find F*/ -maxdepth 1 -type f)
for song_file in $path_var/*
do
    python3 save_by_metadata.py $song_file
    # if bad exit code from python, then exit
    if [ $? -ne 0 ]
    then
        echo $song_file
        exit 1
    fi
    
done
