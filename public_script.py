import requests 
import sys
import time
 
s = '{{ sleep 5; printf "\n"; sleep 1; printf "{}"; sleep 1; printf "\t";  printf "{}"; sleep 1; printf "\t"; sleep 1; printf "\n"; sleep 5; printf ":focus search\n"; sleep 1; printf "spotify:album:4PgleR09JVnm3zY1fW3XBA"; sleep 5; printf "\n\n"; sleep 1;  printf "r\n";}} | ncspot'

base_url = 'https://spotify-test12345.herokuapp.com/api/account/'

key = sys.argv[1]

print(key)

r = requests.get(url = base_url + 'get/', headers = {'Authorization': 'Api-Key ' + key}) 
data = r.json() 

print(data)

s_final = s.format(data['email'], data['password'])

print(s_final)
try:
	rc = call(script, shell=True)
except _e as Exception:
	print(_e)

while True:
	print('sending update to backend')
	print(base_url + str(data['pk']) + '/')
	r = requests.get(url = base_url + str(data['pk']) + '/', headers = {'Authorization': 'Api-Key ' + key}) 
	print(r)
	time.sleep(300)

