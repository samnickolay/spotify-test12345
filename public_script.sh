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

# PLAYLIST2_TAG="playlist2"
# PLAYLIST2=$(aws ec2 describe-tags --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=$PLAYLIST2_TAG" --region=$REGION --output=text | cut -f5)

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

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# sleep 5
# aws configure set default.region us-west-2
# sleep 5
# aws configure set aws_access_key_id AKIAYSZGBWM3RLWPHGTL
# sleep 5
# aws configure set aws_secret_access_key 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

####################

sudo chmod a+x /home/ubuntu/spotify_script.sh
sudo chmod a+x /home/ubuntu/setup_script.sh

####################

echo "install nordvpn"

sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh) &> /dev/null 

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "
@reboot sleep 60 && /home/ubuntu/setup_script.sh $SPOTIFY_EMAIL $SPOTIFY_PASSWORD $VPN_NAME $VPN_EMAIL $VPN_PASSWORD $PLAYLIST >> /home/ubuntu/ncspot.log 2>&1" >> mycron
#install new cron file
sudo crontab -u ubuntu mycron
rm mycron

####################

echo '
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAiU1C7Bu7GokYxdXGbS01nQxY3Go0IWPg4rexMIIzQJFwsD2L
MobNBoi/3TQNWtWtOjAAI8+g/9/pKiuK0mCmeuFKyinFesEcBZ8fxTVZ0E3u85Sw
sEnmuy4Z1qgne1qNMwpth+TsxU8Ku3F2coEiZbSEs6h9k41VGYYiU8Ndswd7N0UJ
PxnEljEdpv9zHzENqxLCwV+Z7k7nO5WzxLOsh17ZPF0RBB8WtyOIAzH46nKxi/2D
7kG9Ori4nh4N+X663FE1wNxpitFhlp9P+3s5r14sPy3zTm6M2pTDgfATB1TAkWbe
u09bncwiH8K6p9rFIGXuJyOZ8mEi/ciNtvErvwIDAQABAoIBAD90RYl5B2+sDJbh
xWKPkkeSfT7gllcYIcalvm38vlMI5FuPFdW0Fuz+Ji3E8KcaOYS6ylXCj1Wx1cB3
fyDbKhWAKWBlDa89sAWpFLW/glKSsexAu6e9f7TiCW77J8QKhVchap1zXzmQ3hTi
yysAIzV9yBZ/uAmJN9sj8pljoNor3aqMhcTnR4wuZw47kst/QHmpf5DJ5U+HQJgY
b/+uAA8JHxITBNLJJfSdE2GaaiIz+gnywl3ln5jLKykG0+MwepO+E8jvAAJfzNNx
b3okMzjlJuJ2LURw2GCF5ZhdxJkrpfvH1Rtfzn2oT19NNKDnPowG+0maB2AfSenj
o1Ot3YECgYEAvJo/zzBHZ1UAQqnGi+b2WdUr4FmFkEbS/iQ5TL9RyTDgA0pRQBDW
oab7fjl9tQNYMcDsIL+Bj9C768MMeEVCqDCH3sUJvBrqk2Vzl26WYGwsm5Tya/oI
TeXsmgnYSNB/Q0n0ZZpTLva5tNDRW/CAv4Fy3+SwYCjxWOZifFJ23dsCgYEAul3q
LVVwe+x7v5CbNd3f/mj0Dzd+KVrVtKAke193QeRqKSfaIGtjkM4i1OwSj2R7fpf5
4z6kEdblXwJnwW9/kvkz+gSW9pZx+BZor+7F5vId9TcsHTc0Xv6tykc+oMYLuc02
jngI8DlWvu0Pw8C3vphGtFLEw6QOMzoKIbGv2O0CgYAAh45WTpRkveBaT4+3JNbc
ObT91EKDvS8qd3+Rr5fTMMfwOm0v+NwhaA6ctByePXwp55jCHseGV9evOcT3MXqW
bkxzW6pDVPADqe1BJ5ZUfvlBFpH3q6QKU/LuG8j3q14wGi0Ne/lv0FGFKHDuCSbT
YtGnv0SfgH3s+fic0L50sQKBgDAmO25i+KDLxF0F21PbcxejvgqAZ9P/Z9820LYf
QAyCGvtvFGfz1tF+sHkaVOE/MLjQQvt3H6SMRM57LJtJV0h9ofQiY25qCB/0ii+K
HQ9B1oOYMYmKzbkNS5FLPt8Cy9zBLCs6z/RgnAzP6pbEn7RaW0oTaEqzhAewIxX5
dlkxAoGBALGA1w2HfLnfwdHKaXyHn2SsKrhuxuxcOXS/39sITro1KPeMpgftFchp
cIZnAGlazoUFjfH0BQMFRf+8kv9Il+11K7uO9uCRh4cfKpuRbVizlEnJd+89tB1s
Ho5mGRu4WapYrfAe8SZbx9XE6/RCQBcxwT2n4s8Ms7DMmnzjkATo
-----END RSA PRIVATE KEY-----' > /home/ubuntu/spotify_key.pem

chmod 444 /home/ubuntu/spotify_key.pem

echo "$SPOTIFY_EMAIL" > /etc/hostname

sudo mkdir /run/user/1000
sudo chown -R ubuntu:ubuntu /run/user/1000
sudo mkdir /usr/share/ 
sudo chown -R ubuntu:ubuntu /usr/share/

sudo chown -R ubuntu:ubuntu /home/ubuntu

sudo reboot
echo "rebooting!"
