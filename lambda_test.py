
import boto3
import json
import random

IMAGE_ID = 'ami-0121ef35996ede438'
InstanceType = 't3.medium'
IamInstanceProfile = 'arn:aws:iam::590100935479:role/lambdaControlEC2'
SecurityGroupId = 'sg-02ef6b6c1b6f17c12'

KEY_NAME = 'test'

VPN_EMAIL = 'samnickolay@gmail.com'
VPN_PASSWORD = 'z3NjbYH8stYFZEi'

PLAYLISTS = ['spotify:playlist:5PkrnGrf4RN2UtHCad45Yu', 'spotify:playlist:5PkrnGrf4RN2UtHCad45Yu',
             'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3', 'spotify:playlist:2N5MFM7E8OXrj5JEiRDRL3',
             'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M']
PLAYLIST = random.choice(PLAYLISTS)

print(PLAYLIST)

region = 'us-west-1'

accounts = {
    'samnickolay@gmail.com': 'Tlbsj5116'
}


user_data = '''#!/bin/bash -xe
# exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo "fetching bash script"
wget -N https://raw.githubusercontent.com/samnickolay/spotify-test12345/main/public_script.sh
chmod +x ./public_script.sh
echo "running bash script"
# ./public_script.sh 2>/home/ubuntu/stderr.log 1>/home/ubuntu/stdout.log
./public_script.sh 2>&1 | tee /home/ubuntu/stdout.log

'''

ec2 = boto3.client('ec2', region_name=region)
iam = boto3.client('iam', region_name=region)


def lambda_handler(event, context):
    print('lambda_handler starting')

    reservations = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}]).get("Reservations")

    instance_ids = []
    for reservation in reservations:
        for instance in reservation["Instances"]:
            print(instance['InstanceId'] + ' - ' + instance['ImageId'])
            if instance['ImageId'] == IMAGE_ID:
                instance_ids.append(instance['InstanceId'])
    try:
        result = ec2.terminate_instances(InstanceIds=instance_ids)
        print(result)
    except Exception as _e:
        print(_e)

    for email, password in accounts.items():
        TAG_SPEC = [
            {
                "ResourceType": "instance",
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

        # instance_profile = iam.create_instance_profile(InstanceProfileName='Test-instance-profile2')
        # print(instance_profile)
        # response = iam.add_role_to_instance_profile(InstanceProfileName='Test-instance-profile2', RoleName='ec2ReadTags')
        # print(response)

        launchedInstances = ec2.run_instances(
            MaxCount=1,
            MinCount=1,
            ImageId=IMAGE_ID,
            InstanceType=InstanceType,
            IamInstanceProfile={'Name': 'Test-instance-profile2'},
            SecurityGroupIds=[SecurityGroupId],
            TagSpecifications=TAG_SPEC,
            UserData=user_data,
            KeyName=KEY_NAME
        )

        print(launchedInstances)

    print('lambda_handler finishing')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
