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

SPOTIFY_EMAIL_TAG="spotify_email"
SPOTIFY_EMAIL=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$SPOTIFY_EMAIL_TAG" --region=$REGION --output=text | cut -f5)

SPOTIFY_PASSWORD_TAG="spotify_password"
SPOTIFY_PASSWORD=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$SPOTIFY_PASSWORD_TAG" --region=$REGION --output=text | cut -f5)

PLAYLIST_TAG="playlist"
PLAYLIST=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$PLAYLIST_TAG" --region=$REGION --output=text | cut -f5)

sudo apt-get install -y pulseaudio pulseaudio-utils dbus-x11 &> /dev/null 
sudo apt-get install -y libncursesw5-dev libdbus-1-dev libpulse-dev libssl-dev libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev &> /dev/null  
sudo apt-get install -y protobuf-compiler &> /dev/null  

sudo apt-get install -y cargo &> /dev/null  

echo "Installing ncspot"

cargo install ncspot  &> /dev/null 

echo "Done installing ncspot"


####################

sudo echo '
export $(dbus-launch)
dbus-launch --exit-with-session pulseaudio --daemon
# pactl -- set-sink-volume 0 200%
echo "Running ncspot setup script"
{ sleep 10; printf "\n"; sleep 3; echo "$1"; sleep 3; printf "\t"; echo "$2"; sleep 3; printf "\t"; sleep 3; printf "\n"; sleep 10; printf "r"; sleep 5; printf "q"; } | sudo /root/.cargo/bin/ncspot
echo "Done running ncspot setup script"
'> /home/ubuntu/script1.sh


sudo echo '
export $(dbus-launch)
dbus-launch --exit-with-session pulseaudio --daemon
# pactl -- set-sink-volume 0 200%
echo "Running ncspot script"
# { sleep 5; printf ":focus search\n"; sleep 3; printf "$1"; sleep 3; printf "\n"; sleep 3; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | sudo /root/.cargo/bin/ncspot
{ sleep 5; printf ":focus search\n"; sleep 3; printf "$1"; sleep 3; printf "\n"; sleep 3; printf "\n"; sleep 60; printf "q"; } | sudo /root/.cargo/bin/ncspot
echo "Done running ncspot script"
'> /home/ubuntu/script2.sh

sudo chmod a+x /home/ubuntu/script1.sh
sudo chmod a+x /home/ubuntu/script2.sh

####################

echo "install nordvpn"

sudo apt-get install -y expect  &> /dev/null  

sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

expect -c "
    spawn sudo nordvpn login
    expect -exact \"Username: \"
    send -- \"$VPN_EMAIL\r\"
    expect -exact \"Password: \"
    send -- \"$VPN_PASSWORD\r\"
    expect eof
"

# nordvpn connect The_Americas
echo "VPN Connected!"
dig +short myip.opendns.com @resolver1.opendns.com
sleep 5;


# echo "sleeping"
# sleep $(($RANDOM*28800/32767));

# if test -z "$DBUS_SESSION_BUS_ADDRESS" ; then
# eval `dbus-launch --sh-syntax`
# echo "D-Bus per-session daemon address is:"
# echo "$DBUS_SESSION_BUS_ADDRESS"
# fi



# sudo bash /home/ubuntu/script1.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD
# sleep 30

# sudo bash /home/ubuntu/script2.sh $PLAYLIST

# sleep 60

# sudo bash /home/ubuntu/script2.sh $PLAYLIST



# echo "sudo bash /home/ubuntu/script1.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD
# sleep 30
# sudo bash /home/ubuntu/script2.sh $PLAYLIST

# sleep 60

# sudo bash /home/ubuntu/script2.sh $PLAYLIST

# echo 'all done playing music!" | at now + 5 minutes


# bash /home/ubuntu/script1.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD

# bash /home/ubuntu/script2.sh $PLAYLIST

# sleep 60

# bash /home/ubuntu/script2.sh $PLAYLIST



# echo "sleeping"
# sleep $(($RANDOM*28800/32767));
# bash /home/ubuntu/script.sh $PLAYLIST

# echo "sleeping"
# sleep $(($RANDOM*28800/32767));
# bash /home/ubuntu/script.sh $PLAYLIST

echo "Disconnecting VPN"
# nordvpn disconnect


