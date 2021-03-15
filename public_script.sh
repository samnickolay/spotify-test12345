#!/bin/bash

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

sudo apt-get install -y openvpn zip wget &>/dev/null 

cd /etc/openvpn

sudo wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip &>/dev/null 

sudo unzip ovpn.zip &>/dev/null 
sudo rm ovpn.zip &>/dev/null 

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

sudo openvpn /etc/openvpn/ovpn_tcp/us2957.nordvpn.com.tcp.ovpn

nohup sudo openvpn /etc/openvpn/ovpn_tcp/us2957.nordvpn.com.tcp.ovpn &>/dev/null &

####################

sudo apt install -y snapd pulseaudio pulseaudio-utils dbus-x11 &> /dev/null

export $(dbus-launch)

dbus-launch --exit-with-session pulseaudio --daemon

pactl -- set-sink-volume 0 200%

export $(dbus-launch)

####################

sudo apt-get update
sudo apt install -y  libncursesw5-dev libdbus-1-dev libpulse-dev libssl-dev libxcb1-dev libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev
sudo apt install -y cargo
cargo install ncspot

####################

{ sleep 5; printf "\n"; sleep 1; printf "$SPOTIFY_EMAIL"; sleep 1; printf "\t";  printf "$SPOTIFY_PASSWORD"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "$PLAYLIST"; sleep 5; printf "\n\n"; sleep 1;  printf "r\n";} | /home/ubuntu/.cargo/bin/ncspot

####################

