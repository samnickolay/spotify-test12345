#!/bin/bash
set -m

export XDG_RUNTIME_DIR=/run/user/1000

sudo mkdir /run/user/1000
sudo mkdir /usr/share/
sudo chown -R ubuntu:ubuntu /run/user/1000
sudo chown -R ubuntu:ubuntu /usr/share/
sudo chown -R ubuntu:ubuntu /home/ubuntu

whoami
env|grep -i runt


chmod 400 test.pem


echo "running checker script!"
/bin/bash -i -c './checker_script.sh' &


ssh -tt -o 'StrictHostKeyChecking no' -i ./test.pem ubuntu@localhost "/bin/bash -i -c '/home/ubuntu/script2.sh $1 $2 $3 $4 $5 $6'"


# bash --init-file <(echo "ls; pwd")
