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

sudo apt install -y --reinstall libasound2 libasound2-data libasound2-plugins &> /dev/null 
sleep 5
sudo apt install -y --reinstall dbus-x11 curl jack alsa-base pulseaudio alsa-utils alsa-oss alsa-utils &> /dev/null 
sleep 5

sudo apt install -y expect xvfb xinit xdotool x11-apps systemd-container &> /dev/null  

sleep 20

# sudo snap install spotify --channel=1.1.55.498.gf9a83c60/stable &> /dev/null 
sudo snap install spotify --devmode &> /dev/null 

sleep 5

####################

# /home/ubuntu/script2.sh 'alexreid@vizy.io' 'T2x98cGUC3A8!?' 'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3' 'us5396' 'nordvpn1@vizy.io' '3cPDMityEM85xhq'


sudo echo '
export XDG_RUNTIME_DIR=/run/user/1000

sudo mkdir /run/user/1000
sudo mkdir /usr/share/
sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

whoami
env|grep -i runt

# sleep 300

su - ubuntu /bin/bash -i -c "/home/ubuntu/script2.sh $1 $2 $3 $4 $5 $6"


# bash --init-file <(echo "ls; pwd")

' > /home/ubuntu/script1.sh

sudo echo '
#!/bin/bash
export XDG_RUNTIME_DIR=/run/user/1000


if [[ $- == *i* ]]
then
    echo "interactive!"
fi

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu


echo "running test!!!" 

sleep 7800 && echo "rebooting after timeout! (7800 seconds)" &
# sleep 7800 && echo "rebooting after timeout! (7800 seconds)" && sudo reboot &

export TERM=xterm
export NO_AT_BRIDGE=1

echo "$1 $2 $3 $4 $5 $6"


echo "sleeping"
date
sleep 10
# sleep $(($RANDOM/13));
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
# sudo nordvpn connect $4
sleep 20;
dig +short myip.opendns.com @resolver1.opendns.com

echo "
----------

"

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

pulseaudio -k 
sudo alsa force-reload 

sleep 5

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

sleep 2

export $(dbus-launch);
pulseaudio --start;
pacmd load-module module-null-sink sink_name=MySink;
pacmd update-sink-proplist MySink device.description=MySink;
pactl -- set-sink-volume MySink 200%;
pactl load-module module-virtual-sink sink_name=VAC_1to2;
pactl load-module module-virtual-sink sink_name=VAC_2to1;

sleep 2
speaker-test -t wav -l 1
sleep 2

echo "running spotify"
save="$DISPLAY"                          
export DISPLAY=:44                    
Xvfb $DISPLAY -screen 0 800x800x24 &   
sleep 2

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

sleep 2
/snap/bin/spotify --no-zygote &
sleep 10

sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu


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
sleep 100
xwd -root -out myshot0.xwd
sleep 1000
xwd -root -out myshot1.xwd
sleep 5000
xwd -root -out myshot2.xwd
sleep 10000
xwd -root -out myshot3.xwd

# scp  -i ./test.pem ubuntu@ec2-54-193-158-5.us-west-1.compute.amazonaws.com:/home/ubuntu/myshot.xwd ./
# xwud -in myshot.xwd 

echo "Disconnecting VPN"
sudo nordvpn disconnect

echo "
DONE!!
"

'> /home/ubuntu/script2.sh

# ps auxww | grep "Xvfb $DISPLAY" | awk '{print $2}' | xargs kill  

sudo chmod a+x /home/ubuntu/script1.sh
sudo chmod a+x /home/ubuntu/script2.sh

####################

echo "install nordvpn"

sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh) &> /dev/null 

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "
@reboot sleep 60 && /home/ubuntu/script1.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD $PLAYLIST $VPN_NAME $VPN_EMAIL $VPN_PASSWORD >> /home/ubuntu/ncspot.log 2>&1" >> mycron
#install new cron file
sudo crontab -u ubuntu mycron
rm mycron

####################

echo '
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAsRaRERoIfPKR+ArH37S0LdgAd/TwZgRh9aAuHPiir8jcspLp
E+8sCBUS8xUy3jDIu0FvQ+zeYj1aKqw64xmlsEraPyuyZDmF4fMVvh9m+2l1v+qD
bwu4bl7bvJuqt/7VjyPGbHEqsyRMMR0lzHEit7nWAX60VwjAntAMzUQWW3FXeXQX
xhOg++ZpUTyEatiUU6Gl1lUs4vLHykxCq7yFau8sF3CMB+g8/hpL5IXCmFbcx71a
ZleJp8uL8eCYR1uZdO3B0xR7tJdsmkT6n/ZK0J/bz8WQB+ALhaPubMB9fvoawpLL
WjpteZGIBCINnY3i1XLZk/Lcyh8NwRz0P6f8QQIDAQABAoIBAD9xXUFqOTZCVQcv
HZJIk/CEnQ5cwy9ZTJsJ6ttYPDiL1n1nYndQzU6L9kD+DD5L7e4gMDN+jeFWJ5J4
J5Sq4JA7ENtm1T9Q2GUtiFGXwHY7vwKlirbi1Q09kK2Oe2f1tR7V60V4eZq6W02R
KrSGp7B4tHHOqd8wdImw8ZUsWnIhm0S1yU3zGdj+LHC7Ysae4xbhi5coW7GOHJ7H
1zN3rDz6HXZ+EbRBju3WrRlXhE0Qvbq6PrBDJcclmyVtyl/VVa0QFrjgDblxy1dA
SbnD1+gqLPTM1pTeH1XBVGzkVlpNXWIzZ+54MVzmIOC8/o1YuA0Ywo5iZWZziTcA
xKv1wtECgYEA+9dC/ne8Z8zWYZ6vlYvy9c7GUds1DmwVKxBfhK8OKRTBUr7Rl4D3
9PSZTwUFLe5GDiYDIENtjWywkEZ5uO0f/e6HKjtWidm83jFzWYhbB07QG+QyXlMU
Onc4sjH0s5d+1ABZ0hlonBVgI53rTEr8g8/ARVw8Mm/orwLmVkowyFUCgYEAtAND
iUlSHKYSk6SjxSS5ynZIbs50eBGvQpbgWGARDNregB4K0eqSFdKkd87pWuGNaboY
w/4xemmJ440JY6LaNpEDJRucEobe0mQzK8V/fEqsHb5v80mm7ag8es04SQ1fsb9H
67OhcQmR201Hf+NDbfvSOWx8f5SGNUhWWW8nQD0CgYBDNJmzMJ69kIMxP9iZbuRi
RlDULUxGUf+AI3lp/hEoU1qXy0ZBSPBilReIZ82PCUP2qJwy8ut8TyH7DmOTPuxH
pmy5j2YzmUB2hvnCTcoE9DpDBy2N0FvYklI183DasDXvOzy8/XzWEjo6pvzQuj4S
qtEjcU67IvQUKBDxvBCylQKBgHvR7ueE1oU8OnTx/3BAhcdcuw/01KouR+Y+z4wa
cD/uYLOxdnHTrq5yGI0Mdvj7QoEh750IwNHZvG4X+ghd4Uk9T/N7XUxlFumS4JvQ
GpPM7Tz8XBb1Z2v7l7ZEaN3e5B7oWrkm8vpEwd4d9vthwGTrnTvAgpZi/Dm0Syjz
SwVlAoGABCjurSggRwVocb/tJYi09UbKzEul9KboG+IgorgPxN2I+5EPPZ6GhdeY
uAP4toFwzxh1IpXyF34x/kFojg+ooJ6AI3EM46jmoFe9cdLJHvhvaqDfkGUN35Uc
EEu97hV7ggP/9gPy0JgoSO21cv2k022OY5/rREwlYAThVKpfAtk=
-----END RSA PRIVATE KEY-----' > /home/ubuntu/test.pem

chmod 444 /home/ubuntu/test.pem

echo "$SPOTIFY_EMAIL" > /etc/hostname

sudo mkdir /run/user/1000
sudo chown -R ubuntu:ubuntu /run/user/1000
sudo mkdir /usr/share/ 
sudo chown -R ubuntu:ubuntu /usr/share/

sudo chown -R ubuntu:ubuntu /home/ubuntu

sudo reboot
echo "rebooting!"
