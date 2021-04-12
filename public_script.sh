#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

sudo apt-get update &> /dev/null
sudo apt-get install -y collectd &> /dev/null

wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb &> /dev/null

sudo dpkg -i -E ./amazon-cloudwatch-agent.deb &> /dev/null

echo '''{
        "agent": {
                "metrics_collection_interval": 60,
                "run_as_user": "root"
        },
        "logs": {
                "logs_collected": {
                        "files": {
                                "collect_list": [
                                        {
                                                "file_path": "/home/ubuntu/stdout.log",
                                                "log_group_name": "stdout.log",
                                                "log_stream_name": "{instance_id}"
                                        },
                                        {
                                                "file_path": "/home/ubuntu/stderr.log",
                                                "log_group_name": "stderr.log",
                                                "log_stream_name": "{instance_id}"
                                        },
                                        {
                                                "file_path": "/home/ubuntu/ncspot.log",
                                                "log_group_name": "ncspot.log",
                                                "log_stream_name": "{instance_id}"
                                        },
                                        {
                                                "file_path": "/home/ubuntu/setup.log",
                                                "log_group_name": "setup.log",
                                                "log_stream_name": "{instance_id}"
                                        }
                                ]
                        }
                }
        },
        "metrics": {
                "append_dimensions": {
                        "AutoScalingGroupName": "${aws:AutoScalingGroupName}",
                        "ImageId": "${aws:ImageId}",
                        "InstanceId": "${aws:InstanceId}",
                        "InstanceType": "${aws:InstanceType}"
                },
                "metrics_collected": {
                        "collectd": {
                                "metrics_aggregation_interval": 60
                        },
                        "disk": {
                                "measurement": [
                                        "used_percent"
                                ],
                                "metrics_collection_interval": 60,
                                "resources": [
                                        "*"
                                ]
                        },
                        "mem": {
                                "measurement": [
                                        "mem_used_percent"
                                ],
                                "metrics_collection_interval": 60
                        },
                        "statsd": {
                                "metrics_aggregation_interval": 60,
                                "metrics_collection_interval": 10,
                                "service_address": ":8125"
                        }
                }
        }
}''' | sudo tee /opt/aws/amazon-cloudwatch-agent/bin/config.json

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s

####################

sudo apt-get update &> /dev/null 

sudo apt-get install -y python-pip &> /dev/null 
sudo apt-get install -y awscli &> /dev/null 

sudo pip install -U pip &> /dev/null 
sudo pip install awscli &> /dev/null 

INSTANCE_ID=$(ec2metadata --instance-id)
REGION=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | grep region | awk -F\" '{print $4}')

VPN_EMAIL_TAG="vpn_email"
VPN_EMAIL=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$VPN_EMAIL_TAG" --region=$REGION --output=text | cut -f5)

VPN_PASSWORD_TAG="vpn_password"
VPN_PASSWORD=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$VPN_PASSWORD_TAG" --region=$REGION --output=text | cut -f5)

VPN_NAME_TAG="vpn_name"
VPN_NAME=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$VPN_NAME_TAG" --region=$REGION --output=text | cut -f5)

SPOTIFY_EMAIL_TAG="spotify_email"
SPOTIFY_EMAIL=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$SPOTIFY_EMAIL_TAG" --region=$REGION --output=text | cut -f5)

SPOTIFY_PASSWORD_TAG="spotify_password"
SPOTIFY_PASSWORD=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$SPOTIFY_PASSWORD_TAG" --region=$REGION --output=text | cut -f5)

PLAYLIST_TAG="playlist"
PLAYLIST=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$PLAYLIST_TAG" --region=$REGION --output=text | cut -f5)

echo "$VPN_EMAIL $VPN_PASSWORD $VPN_NAME"

# sudo apt-get install -y pulseaudio pulseaudio-utils dbus-x11 curl &> /dev/null 
sudo apt-get install -y dbus-x11 curl jack alsa-base pulseaudio alsa-utils alsa-oss &> /dev/null 

sudo apt-get install -y --reinstall libasound2 libasound2-data libasound2-plugins &> /dev/null 
# sudo apt-get install -y alsa-utils alsa-oss

# sudo apt-get --purge --reinstall -y install pulseaudio &> /dev/null 

# sudo snap install pulseaudio &> /dev/null 
# sudo snap install spotify --channel=1.1.55.498.gf9a83c60/stable &> /dev/null 
sudo snap install --devmode spotify &> /dev/null 

# curl -sS https://download.spotify.com/debian/pubkey_0D811D58.gpg | sudo apt-key add -
# echo "deb http://repository.spotify.com stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list
# sudo apt update
# sudo apt install -y spotify-client &> /dev/null 

echo "Done installing ncspot"

####################

sudo echo '
#!/bin/bash

echo "running setup script!"
bash -c "/home/ubuntu/script2.sh $1 $2 $3 $4 $5 $6"

sleep 5;

# echo "running setup script! - 2x"
# # bash -c "/home/ubuntu/script2.sh $1 $2 $3 $4 $5 $6"

# echo "done with setup script!"

'> /home/ubuntu/script1.sh

sudo echo '
#!/bin/bash

echo "running test!!!" 
cat /etc/hostname
whoami

REBOOT_TIMER=$(($(($(tr -dc 0-9 < /dev/urandom | head -c6 | sed "s/^0*//")*57600/999999))+57600))
# sleep $REBOOT_TIMER && echo "rebooting after timeout! ($REBOOT_TIMER)" && sudo reboot &
sleep $REBOOT_TIMER && echo "rebooting after timeout! ($REBOOT_TIMER)" &

export TERM=xterm
XDG_RUNTIME_DIR=/run/user/1000
export NO_AT_BRIDGE=1

echo "$1 $2 $3 $4 $5 $6"

big_random () {
  echo $(($(tr -dc 0-9 < /dev/urandom | head -c6 | sed "s/^0*//")*28800/999999))
}
# echo $(big_random)

small_random () {
  echo $(($(tr -dc 0-9 < /dev/urandom | head -c6 | sed "s/^0*//")*14400/999999))
}
# echo $(small_random)

echo "sleeping"
date
sleep 10
# sleep $(small_random);
date
echo "done sleeping"

dig +short myip.opendns.com @resolver1.opendns.com

echo "

----------
"

expect -c "
    spawn sudo nordvpn login
    expect -exact \"Username: \"
    send -- \"$5\r\"
    expect -exact \"Password: \"
    send -- \"$6\r\"
    expect eof
"

echo "VPN Connected! $4"
sudo nordvpn connect $4
sleep 20;
dig +short myip.opendns.com @resolver1.opendns.com

echo "
----------

"


echo "running spotify"
save="$DISPLAY"                          
export DISPLAY=:44                    
Xvfb $DISPLAY -screen 0 800x800x24 &   
sleep 2

sudo chown -R ubuntu:ubuntu /home/ubuntu

mkdir /run/user/1000
sudo chown -R ubuntu:ubuntu /run/user/1000

pulseaudio -k 
sudo alsa force-reload 

sleep 5

export $(dbus-launch);
# sudo pulseaudio -system &;
pulseaudio --start;
pacmd load-module module-null-sink sink_name=MySink;
pacmd update-sink-proplist MySink device.description=MySink;
pactl -- set-sink-volume MySink 200%;
pactl load-module module-virtual-sink sink_name=VAC_1to2;
pactl load-module module-virtual-sink sink_name=VAC_2to1;

sleep 2
/snap/bin/spotify --no-zygote &
sleep 10

xdotool mousemove 400 450
sleep 2
xdotool click 1

sleep 2
xdotool type "$1"
sleep 2
xdotool key Tab
sleep 2
xdotool type "$2"
sleep 2
xdotool key Return
sleep 10

sleep 2
xdotool key "Escape"
sleep 2

sleep 2
xdotool key ctrl+l
sleep 2
xdotool type "life contexted"
sleep 2

xdotool mousemove 400 300
sleep 2
xdotool click 1
sleep 2

xdotool mousemove 530 450
sleep 2
xdotool click 1
sleep 2

xdotool mousemove 450 450
sleep 2
xdotool click 1
sleep 2

xdotool mousemove 375 450
sleep 2
xdotool click 1
sleep 2


sleep 10

xwd -root -out myshot.xwd

sleep 2

# cp myshot.xwd /home/ubuntu/

# sleep $(big_random);

echo "Disconnecting VPN"
nordvpn disconnect


echo "\nDONE!!\n"

sleep 7800
sudo reboot

'> /home/ubuntu/script2.sh

# ps auxww | grep "Xvfb $DISPLAY" | awk '{print $2}' | xargs kill  

sudo chmod a+x /home/ubuntu/script1.sh

sudo chmod a+x /home/ubuntu/script2.sh

####################

echo "install nordvpn"

sudo apt-get install -y expect xvfb xinit xdotool x11-apps &> /dev/null  

sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

# sudo echo '
# #!/bin/bash

# expect -c "
#     spawn sudo nordvpn login
#     expect -exact \"Username: \"
#     send -- \"$1\r\"
#     expect -exact \"Password: \"
#     send -- \"$2\r\"
#     expect eof
# "'> /home/ubuntu/vpn_login.sh

# sudo chmod a+x /home/ubuntu/vpn_login.sh


# su -c "/home/ubuntu/vpn_login.sh $VPN_EMAIL $VPN_PASSWORD" - ubuntu

# expect -c "
#     spawn sudo nordvpn login
#     expect -exact \"Username: \"
#     send -- \"$VPN_EMAIL\r\"
#     expect -exact \"Password: \"
#     send -- \"$VPN_PASSWORD\r\"
#     expect eof
# "

# su ubuntu 
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "@reboot sleep 60 && /home/ubuntu/script1.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD $PLAYLIST $VPN_NAME $VPN_EMAIL $VPN_PASSWORD >> /home/ubuntu/ncspot.log 2>&1" >> mycron
#install new cron file
sudo crontab -u ubuntu mycron
rm mycron

# sudo crontab -u ubuntu mycron


####################

echo "$SPOTIFY_EMAIL" > /etc/hostname

# su ubuntu

# whoami

# expect -c "
#     spawn sudo nordvpn login
#     expect -exact \"Username: \"
#     send -- \"$VPN_EMAIL\r\"
#     expect -exact \"Password: \"
#     send -- \"$VPN_PASSWORD\r\"
#     expect eof
# "


# su - ubuntu -- -- "$VPN_EMAIL" "$VPN_PASSWORD"

# sleep 2 

# expect -c "
#     spawn sudo nordvpn login
#     expect -exact \"Username: \"
#     send -- \"$1\r\"
#     expect -exact \"Password: \"
#     send -- \"$2\r\"
#     expect eof
# "'

# sleep 5


sudo reboot
echo "rebooting!"




