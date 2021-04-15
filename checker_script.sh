#!/bin/bash

export XDG_RUNTIME_DIR=/run/user/1000

rm /home/ubuntu/spotify_text.txt

while :
do
	echo "Running checker script!"
	
    FILENAME=/home/ubuntu/spotify_text.txt
    FILESIZE=$(stat -c%s "$FILENAME")
    
    if (( $FILESIZE > 50 )); then
        printf  "error - restarting" >> /home/ubuntu/stderr.log
        sudo reboot
    fi
    
    sleep 60

done


