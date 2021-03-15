
import boto3

IMAGE_ID = 'ami-0121ef35996ede438'
InstanceType='t3.medium'
IamInstanceProfile='ec2ReadTags'

KEY_NAME = 'test'

VPN_EMAIL = 'samnickolay@gmail.com'
VPN_PASSWORD = 'z3NjbYH8stYFZEi'
PLAYLIST = 'spotify:album:4PgleR09JVnm3zY1fW3XBA'

region = 'us-west-1'
ec2 = boto3.client('ec2', region_name=region)

accounts = {
	'samnickolay@gmail.com': 'Tlbsj5116'
}


user_data = '''#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
	echo "fetching bash script"
	wget -N https://raw.githubusercontent.com/samnickolay/spotify-test12345/main/public_script.sh
	chmod +x ./public_script.sh
	echo "running bash script"
	./public_script.sh
'''

def lambda_handler(event, context):
	print('lambda_handler starting')

	print(user_data)

	for instance in ec2.instances.all():
		print(instance.id)
		if instance.imaged.id == IMAGE_ID:
			ec2.stop_instances(InstanceIds=[instance.id])


	for email, password in accounts:
	    TAG_SPEC = [
	        {
	        "ResourceType":"instance",
	        "Tags": [
	                {
	                    "Key": "vpn_email",
	                    "Value": VPN_EMAIL,
	                },
	                {
	                    "Key": "vpn_password",
	                    "Value": VPN_PASSWORD,
	                },
	                {
	                    "Key": "playlist",
	                    "Value": PLAYLIST,
	                },
	                {
	                    "Key": "spotify_email",
	                    "Value": email,
	                },
	                {
	                    "Key": "spotify_password",
	                    "Value": password,
	                }
	            ]
	    	}
	    ]

	    print(TAG_SPEC)

		launchedInstances = ec2.run_instances(
			MaxCount=1,
			MinCount=1,
			ImageId=IMAGE_ID,
	    	InstanceType=InstanceType,
	    	IamInstanceProfile={'Name': IamInstanceProfile},
			#LaunchTemplate=lt_specifics,  
			TagSpecifications=TAG_SPEC,
			KeyName=KEY_NAME)

		print(launchedInstances)

	print('lambda_handler finishing')
