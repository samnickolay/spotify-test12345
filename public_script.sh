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

sudo apt-get install -y pulseaudio pulseaudio-utils dbus-x11 &> /dev/null 

sudo snap install pulseaudio &> /dev/null 
# sudo snap install spotify --channel=1.1.55.498.gf9a83c60/stable &> /dev/null 
sudo snap install spotify &> /dev/null 

echo "Done installing ncspot"

####################

sudo echo '
#!/bin/sh

echo "running test!!!" 
cat /etc/hostname

REBOOT_TIMER=$(($(($(tr -dc 0-9 < /dev/urandom | head -c6 | sed "s/^0*//")*57600/999999))+57600))
# sleep $REBOOT_TIMER && echo "rebooting after timeout! ($REBOOT_TIMER)" && sudo reboot &
sleep $REBOOT_TIMER && echo "rebooting after timeout! ($REBOOT_TIMER)" &

export TERM=xterm

export $(dbus-launch)
pulseaudio --start
pactl -- set-sink-volume 0 200%

sleep 5

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

echo "VPN Connected! $4"
nordvpn connect $4
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

sudo mkdir /run/user/0/

/bin/bash -c "snap run spotify --no-zygote &"
# spotify --no-zygote &
sleep 10

# click login
xdotool mousemove 400 450
sleep 2
xdotool click 1

sleep 2
xdotool type "$1"
sleep 2
xdotool key Tab
sleep 2
xdotool type "$"
sleep 2
xdotool key Return
sleep 10

sleep 2
xdotool key ctrl+l
sleep 2
xdotool type "life contexted"
sleep 2

xdotool mousemove 400 300
sleep 2
xdotool click 1
sleep 2
# xwd -root -out myshot.xwd

xdotool mousemove 530 450
sleep 2
xdotool click 1
sleep 2
# xwd -root -out myshot.xwd

xdotool mousemove 450 450
sleep 2
xdotool click 1
sleep 2
# xwd -root -out myshot.xwd

xdotool mousemove 375 450
sleep 2
xdotool click 1
sleep 2
# xwd -root -out myshot.xwd

sleep 2
xdotool key ctrl+r
sleep 2

xwd -root -out myshot.xwd

# sleep $(big_random);
sleep 20

echo "Disconnecting VPN"
nordvpn disconnect


echo "\nDONE!!\n"

#sudo reboot

'> /root/script2.sh

# ps auxww | grep "Xvfb $DISPLAY" | awk '{print $2}' | xargs kill  

sudo chmod a+x /root/script2.sh

####################

echo "install nordvpn"

sudo apt-get install -y expect xvfb xinit xdotool x11-apps &> /dev/null  

sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

expect -c "
    spawn sudo nordvpn login
    expect -exact \"Username: \"
    send -- \"$VPN_EMAIL\r\"
    expect -exact \"Password: \"
    send -- \"$VPN_PASSWORD\r\"
    expect eof
"


#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "@reboot sleep 60 && /root/script2.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD $PLAYLIST $VPN_NAME $VPN_EMAIL $VPN_PASSWORD >> /home/ubuntu/ncspot.log 2>&1" >> mycron
#install new cron file
crontab mycron
rm mycron

####################

echo "$SPOTIFY_EMAIL" > /etc/hostname


sudo reboot
echo "rebooting!"




