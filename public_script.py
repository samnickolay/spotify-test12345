import sys
import time
import subprocess
import random

s = '{{ sleep 5; printf "\n"; sleep 1; printf "{}"; sleep 1; printf "\t";  printf "{}"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "{}"; sleep 5; printf "\n\n"; sleep 1;  printf "r\n";}} | /home/ubuntu/.cargo/bin/ncspot'
s2 = '{{ sleep 5; printf ":focus search\n"; sleep 1; printf "{}"; sleep 5; printf "\n\n"; sleep 1;  printf "r\n";}} | /home/ubuntu/.cargo/bin/ncspot'

email = sys.argv[1]
password = sys.argv[2]
playlist = sys.argv[3]

s_final = s.format(email, password, playlist)
s2_final = s.format(playlist)

print(s_final)
print(s2_final)

# try:
#     rc = subprocess.Popen(s_final, shell=True)
# except Exception as _e:
#     print(_e)

while True:
    print('waiting to start script')
    seconds_to_wait = random.randint(0, 28800)  # sleep between 0 and 8 hours
    print(seconds_to_wait)
    time.sleep(seconds_to_wait)
    print('starting script')
    try:
        p = subprocess.Popen(s2_final, shell=True)

        seconds_to_wait = random.randint(0, 28800)  # sleep between 0 and 8 hours
        time.sleep(seconds_to_wait)
        print(seconds_to_wait)
        print('stopping script')

        p.terminate()
        p.wait()
    except Exception as _e:
        print(_e)
