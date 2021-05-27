#!/bin/bash
set -m

export XDG_RUNTIME_DIR=/run/user/1000


sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu


SECONDS_UNTIL_SEVEN=$(( $(date +%s -d "today 14:00") - $( date +%s ) ))
TWO_HOURS=$(($RANDOM/5))

echo "sleeping"
date
sleep 10

if (( $SECONDS_UNTIL_SEVEN > 0 )); then
    sleep $SECONDS_UNTIL_SEVEN 
fi
sleep $TWO_HOURS
date
echo "done sleeping"

# echo "sleeping"
# date
# sleep 10
# sleep $(($RANDOM/6));
# date
# echo "done sleeping"

# RAND=$RANDOM

FIFTEEN_HOURS=54000
FOUR_HOURS=$(($RANDOM/2))
TOTAL=$(( $FIFTEEN_HOURS + $FOUR_HOURS))

echo "running test for $TOTAL seconds" 

INSTANCE_ID=$(ec2metadata --instance-id)

# sleep $TOTAL && echo "rebooting after timeout - $TOTAL seconds" && printf "successful - restarting" >> /home/ubuntu/stderr.log  &
sleep $TOTAL && echo "rebooting after timeout - $TOTAL seconds" && date && sudo reboot &

export TERM=xterm
export NO_AT_BRIDGE=1

echo "$@"

artists=('spotify:artist:1FB5eEgWflHL5FPLGeUAKj' 'spotify:artist:65D3pXVviGny9ATzKlPeeF' 'spotify:artist:3eHWSVXnTmRuEebZbPpb9x' 'spotify:artist:0SOWqU3A9j1p0NBVL7I5AA' 'spotify:artist:1FB5eEgWflHL5FPLGeUAKj');
playlists=("$6" "$6" "$6" "$6" "$6" "$6" "$6" "$6" "$6" "spotify:playlist:37i9dQZF1DXdbXrPNafg9d" "spotify:playlist:37i9dQZF1DX4JAvHpjipBk", "spotify:playlist:37i9dQZF1DXbpmT3HUTsZm" "spotify:playlist:1sJqZLpvNeR9fSlpj1PHwp");

echo ${artists[*]}
echo ${playlists[*]}

# array=("${artists[@]}" "${playlists[@]}")
array=("spotify:playlist:37i9dQZF1DXdbXrPNafg9d" "spotify:playlist:37i9dQZF1DX4JAvHpjipBk", "spotify:playlist:37i9dQZF1DXbpmT3HUTsZm" "spotify:playlist:1sJqZLpvNeR9fSlpj1PHwp");

echo ${array[*]}

rand=$[$RANDOM % ${#array[@]}]
PLAYLIST=${array[$rand]}

echo "PLAYLIST:"
echo $PLAYLIST

dig +short myip.opendns.com @resolver1.opendns.com

printf "\n\n----------\n"

expect -c "
    spawn sudo nordvpn login
    expect -exact \"Username: \"
    send -- \"$4\r\"
    expect -exact \"Password: \"
    send -- \"$5\r\"
    expect eof
"

echo "VPN Connected! $3"
sudo nordvpn connect $3 || sudo nordvpn connect The_Americas  
sleep 20;
dig +short myip.opendns.com @resolver1.opendns.com

printf "\n----------\n\n"

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

pulseaudio -k 
sudo alsa force-reload 

sleep 5

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

sleep 5

export $(dbus-launch);
pulseaudio --start;
pacmd load-module module-null-sink sink_name=MySink;
pacmd update-sink-proplist MySink device.description=MySink;
pactl -- set-sink-volume MySink 200%;
pactl load-module module-virtual-sink sink_name=VAC_1to2;
pactl load-module module-virtual-sink sink_name=VAC_2to1;

sleep 5
speaker-test -t wav -l 1
sleep 5

echo "running spotify"
date
save="$DISPLAY"                          
export DISPLAY=:44                    
Xvfb $DISPLAY -screen 0 800x800x24 &   
sleep 10

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

sleep 10
/snap/bin/spotify --no-zygote &
sleep 120

# sudo chown -R ubuntu:ubuntu /run/user/1000
# sudo chown -R ubuntu:ubuntu /usr/share/
# sudo chown -R ubuntu:ubuntu /home/ubuntu

sleep 5
xdotool key "Escape"
sleep 5

xdotool mousemove 400 450
sleep 5
xdotool click 1
sleep 20

xwd -root -out myshot99.xwd

sleep 5
xdotool type "$1"
sleep 5
xdotool key Tab
sleep 5
xdotool type "$2"
sleep 5

xwd -root -out myshot98.xwd

xdotool key Return
sleep 20

sleep 5
xdotool key "Escape"
sleep 5

xwd -root -out myshot97.xwd

sleep 5
xdotool key ctrl+l
sleep 5
xdotool type "$PLAYLIST"
sleep 5
xdotool key Return
sleep 5

# xdotool mousemove 400 300
# sleep 5
# xdotool click 1
# sleep 5

xdotool mousemove 530 450
sleep 5
xdotool click 1
sleep 5

xdotool mousemove 450 450
sleep 5
xdotool click 1
sleep 5

sleep 5
xdotool key "Escape"
sleep 5

xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5


FILE=/home/ubuntu/loop.txt
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
    touch $FILE
    sleep 10

    xdotool mousemove 350 690
    sleep 5
    xdotool click 1
    sleep 5

    xdotool mousemove 530 690
    sleep 5
    xdotool click 1
    sleep 5
fi

sleep 10
xwd -root -out myshot.xwd
sleep 100
xwd -root -out myshot0.xwd
sleep 1000
xwd -root -out myshot1.xwd

sleep 5

# INSTANCE_ID=$(ec2metadata --instance-id)
echo "s3://spotify-test12345/$INSTANCE_ID.xwd"
aws s3 cp ./myshot1.xwd "s3://spotify-test12345/$INSTANCE_ID.xwd"

sleep 5

date

sleep $RANDOM
# stop
echo "pause 1"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot2.xwd
sleep $(($RANDOM/6))
# start
echo "play 1"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot3.xwd

date

sleep $RANDOM
# stop
echo "pause 2"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot4.xwd
sleep $(($RANDOM/6))
# start
echo "play 2"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot5.xwd

date

sleep $RANDOM
# stop
echo "pause 3"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot6.xwd
sleep $(($RANDOM/6))
# start
echo "play 3"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot7.xwd

date

sleep $RANDOM
# stop
echo "pause 4"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot8.xwd
sleep $(($RANDOM/6))
# start
echo "play 4"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot9.xwd

date

sleep $RANDOM
# stop
echo "pause 5"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot10.xwd
sleep $(($RANDOM/6))
# start
echo "play 5"
xdotool mousemove 375 450
sleep 5
xdotool click 1
sleep 5
xwd -root -out myshot11.xwd

date

# sleep 5000
# xwd -root -out myshot2.xwd
# sleep 10000
# xwd -root -out myshot3.xwd
# sleep 20000
# xwd -root -out myshot4.xwd
# sleep 20000
# xwd -root -out myshot5.xwd
# sleep 20000
# xwd -root -out myshot5.xwd
# sleep 20000
# xwd -root -out myshot6.xwd

# scp  -i ./spotify_key.pem ubuntu@ec2-54-183-224-74.us-west-1.compute.amazonaws.com:/home/ubuntu/myshot*.xwd ./
# xwud -in myshot.xwd 


# echo "Disconnecting VPN"
# sudo nordvpn disconnect

# printf "\nDONE!!\n"
