#!/bin/bash

wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb 

sudo dpkg -i -E ./amazon-cloudwatch-agent.deb 

sudo apt install -y collectd 

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
                                                "file_path": "/home/ubuntu/test.log",
                                                "log_group_name": "test.log",
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


sudo apt-get update 
sudo apt-get install -y python-pip 
sudo pip install -U pip 
sudo pip install awscli 

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

####################

sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

sudo apt-get install -y openvpn zip wget  

cd /etc/openvpn

sudo wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip  

sudo unzip -o ovpn.zip  
sudo rm ovpn.zip  

sudo ip rule add from $(ip route get 1 | grep -Po '(?<=src )(\S+)') table 128
sudo ip route add table 128 to $(ip route get 1 | grep -Po '(?<=src )(\S+)')/32 dev $(ip -4 route ls | grep default | grep -Po '(?<=dev )(\S+)')
sudo ip route add table 128 default via $(ip -4 route ls | grep default | grep -Po '(?<=via )(\S+)')

echo "[Resolve]
DNS=208.67.222.222 208.67.220.220
#FallbackDNS=
#Domains=
#LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#Cache=yes
#DNSStubListener=yes" | sudo tee /etc/systemd/resolved.conf

sudo systemctl restart systemd-resolved.service

printf "$VPN_EMAIL
$VPN_PASSWORD
" > /home/ubuntu/auth.txt

sudo sed -i 's/auth-user-pass/auth-user-pass \/home\/ubuntu\/auth.txt/' /etc/openvpn/ovpn_tcp/us2957.nordvpn.com.tcp.ovpn

nohup sudo openvpn /etc/openvpn/ovpn_tcp/us2957.nordvpn.com.tcp.ovpn  &

####################

sudo apt install -y snapd pulseaudio pulseaudio-utils dbus-x11 

export $(dbus-launch)

# pulseaudio --kill

dbus-launch --exit-with-session pulseaudio --daemon

pactl -- set-sink-volume 0 200%

####################

sudo apt-get update  
sudo apt install -y libncursesw5-dev libdbus-1-dev libpulse-dev libssl-dev libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev  
sudo apt-get install -y protobuf-compiler  

sudo apt install -y cargo  

if cargo install -q ncspot ; then
    echo "cargo install ncspot succeeded"
else
    echo "cargo install ncspot failed"
fi

####################

# { sleep 5; printf "\n"; sleep 1; printf "$SPOTIFY_EMAIL"; sleep 1; printf "\t";  printf "$SPOTIFY_PASSWORD"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 5; printf "\n\n"; sleep 1;  printf "r\n";} | /home/ubuntu/.cargo/bin/ncspot
# { sleep 5; printf "\n"; sleep 1; printf "samnickolay@gmail.com"; sleep 1; printf "\t";  printf "Tlbsj5116"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "spotify:album:4PgleR09JVnm3zY1fW3XBA"; sleep 5; printf "\n\n"; sleep 1;  printf "r\n";} | /home/ubuntu/.cargo/bin/ncspot

# { sleep 5; printf "\n"; sleep 1; printf "samnickolay@gmail.com"; sleep 1; printf "\t";  printf "Tlbsj5116"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "spotify:album:4PgleR09JVnm3zY1fW3XBA"; sleep 3; printf "\n"; sleep 1; printf "r\n";  sleep 10; printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
# { sleep 5; printf ":focus search\n"; sleep 1; printf "spotify:album:4PgleR09JVnm3zY1fW3XBA"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep 10; printf "q"; } | /home/ubuntu/.cargo/bin/ncspot

sleep $(($RANDOM*28800/32767));
echo "Running ncspot script"
{ sleep 5; printf "\n"; sleep 1; printf "$SPOTIFY_EMAIL"; sleep 1; printf "\t";  printf "$SPOTIFY_PASSWORD"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 3; printf "\n"; sleep 1; printf "r\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
echo "sleeping"
sleep $(($RANDOM*28800/32767));

echo "Running ncspot script"
{ sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
echo "sleeping"
sleep $(($RANDOM*28800/32767));

echo "Running ncspot script"
{ sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
echo "sleeping"
sleep $(($RANDOM*28800/32767));

echo "Running ncspot script"
{ sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
echo "sleeping"
sleep $(($RANDOM*28800/32767));

echo "Running ncspot script"
{ sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
echo "sleeping"
sleep $(($RANDOM*28800/32767));

echo "Running ncspot script"
{ sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
echo "sleeping"
sleep $(($RANDOM*28800/32767));

####################

