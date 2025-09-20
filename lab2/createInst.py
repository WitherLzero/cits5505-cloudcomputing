# This script is based on the content from Lab2EC2Docker.md
import boto3
import os
import time

# --- Configuration from Lab Instructions ---
# You must replace these with your actual details
STUDENT_NUMBER = "24745401" # <--- REPLACE with your student number
AMI_ID = "ami-042b4708b1d05f512" # <--- REPLACE with the AMI for your assigned region
INSTANCE_TYPE = "t3.micro"

# Resource names are made unique to avoid conflict with CLI-created resources
KEY_NAME = f"{STUDENT_NUMBER}-key-boto3"
SECURITY_GROUP_NAME = f"{STUDENT_NUMBER}-sg-boto3"
INSTANCE_NAME = f"{STUDENT_NUMBER}-vm-boto3"
PEM_FILE_NAME = f"{KEY_NAME}.pem"

# Initialize Boto3 EC2 client
ec2 = boto3.client('ec2')

try:
    # Create Security Group
    sg_response = ec2.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description="Boto3 security group for lab 2"
    )
    security_group_id = sg_response['GroupId']

    # Authorize SSH Ingress
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    
    # Create Key Pair and save it
    key_pair_response = ec2.create_key_pair(KeyName=KEY_NAME)
    with open(PEM_FILE_NAME, "w") as pem_file:
        pem_file.write(key_pair_response['KeyMaterial'])
    os.chmod(PEM_FILE_NAME, 0o400)

    # Launch Instance
    instance_response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SecurityGroupIds=[security_group_id],
        MinCount=1,
        MaxCount=1
    )
    instance_id = instance_response['Instances'][0]['InstanceId']

    # Wait for the instance to be running
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

    # Tag the instance
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': INSTANCE_NAME}]
    )

    # Describe instance to get Public IP
    describe_response = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = describe_response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    print("--- Boto3 Script Finished ---")
    print(f"Instance {instance_id} is running at IP: {public_ip}")
    print(f"Connect with: ssh -i {PEM_FILE_NAME} ubuntu@{public_ip}")

except Exception as e:
    print(f"An error occurred: {e}")