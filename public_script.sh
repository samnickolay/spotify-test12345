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

sudo apt-get update &> /dev/null  

sudo apt-get install -y pulseaudio pulseaudio-utils dbus-x11 &> /dev/null 
sudo apt-get install -y libncursesw5-dev libdbus-1-dev libpulse-dev libssl-dev libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev &> /dev/null  
sudo apt-get install -y protobuf-compiler &> /dev/null  

sudo apt-get install -y cargo &> /dev/null  

echo "Installing ncspot"

sudo -H -u ubuntu bash -c "cargo install ncspot"

####################

####################

sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

sudo apt-get install -y openvpn zip wget &> /dev/null  

cd /etc/openvpn

sudo wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip &> /dev/null  

sudo unzip -o ovpn.zip &> /dev/null  
sudo rm ovpn.zip &> /dev/null  

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

echo "Starting VPN"

nohup sudo openvpn /etc/openvpn/ovpn_tcp/us2957.nordvpn.com.tcp.ovpn  &

####################

# export $(dbus-launch)
# # pulseaudio --kill
# dbus-launch --exit-with-session pulseaudio --daemon
# pactl -- set-sink-volume 0 200%

####################


echo "creating scripts!"

sudo echo '
echo "sleeping"
sleep $(($RANDOM*28800/32767));
export $(dbus-launch)
whoami
dbus-launch --exit-with-session pulseaudio --daemon
pactl -- set-sink-volume 0 200%
echo "Running ncspot script"
{ sleep 5; printf "\n"; sleep 1; echo "$1"; sleep 1; printf "\t"; echo "$2"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 10; printf ":focus search\n"; sleep 1; echo "$3"; sleep 3; printf "\n"; sleep 1; printf "r\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
' > /home/ubuntu/script1.sh

sudo chmod a+x /home/ubuntu/script1.sh

sudo echo '
echo "sleeping"
sleep $(($RANDOM*28800/32767));
export $(dbus-launch)
whoami
dbus-launch --exit-with-session pulseaudio --daemon
pactl -- set-sink-volume 0 200%
echo "Running ncspot script"
{ sleep 5; printf ":focus search\n"; sleep 1; printf "$1"; sleep 3; printf "\n"; sleep 1; printf "\n"; sleep $(($RANDOM*28800/32767)); printf "q"; } | /home/ubuntu/.cargo/bin/ncspot
' > /home/ubuntu/script2.sh

sudo chmod a+x /home/ubuntu/script2.sh

echo "done creating scripts!"

####################

sudo -H -u ubuntu bash -c "/home/ubuntu/script1.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD $PLAYLIST"

sudo -H -u ubuntu bash -c "/home/ubuntu/script2.sh $PLAYLIST"

sudo -H -u ubuntu bash -c "/home/ubuntu/script2.sh $PLAYLIST"

sudo -H -u ubuntu bash -c "/home/ubuntu/script2.sh $PLAYLIST"

sudo -H -u ubuntu bash -c "/home/ubuntu/script2.sh $PLAYLIST"

####################

