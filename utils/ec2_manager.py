# ec2_manager.py
# A reusable module with generic functions for managing EC2 resources.

import boto3
from botocore.exceptions import ClientError
import os
from . import config # Use a relative import within the package

# Initialize the client using the region from our config file
ec2 = boto3.client('ec2', region_name=config.REGION_NAME)

def create_key_pair(key_name):
    """Creates an EC2 key pair if it doesn't exist and saves the .pem file."""
    pem_file_path = f"{key_name}.pem"
    if os.path.exists(pem_file_path):
        print(f"Existed key pair: {pem_file_path}")
        return
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        with open(pem_file_path, "w") as f:
            f.write(key_pair['KeyMaterial'])
        os.chmod(pem_file_path, 0o400)
        print(f"Created and saved key pair: {pem_file_path}")
    except ClientError as e:
        if e.response['Error']['Code'] != 'InvalidKeyPair.Duplicate':
            raise

def create_security_group(sg_name, description, rules):
    """Creates a security group with specified inbound rules."""
    try:
        sg_response = ec2.create_security_group(
            GroupName=sg_name, 
            Description=description
        )
        group_id = sg_response['GroupId']
        
        # Authorize SSH Ingress
        ec2.authorize_security_group_ingress(
            GroupId=group_id, 
            IpPermissions=rules
        )
        print(f"Created security group '{sg_name}' with ID: {group_id}")
        return group_id
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
            response = ec2.describe_security_groups(GroupNames=[sg_name])
            group_id = response['SecurityGroups'][0]['GroupId']
            print(f"Existed security group '{sg_name}' with ID: {group_id}")
            return group_id
        else:
            raise

def setup_instance(name,ami_id, instance_type, key_name, sg_id, az = None):
    """
    Ensures an instance with a specific name is running in a specific AZ.
    """
    # This filter checks for BOTH name and availability zone.
    filters = [
        {'Name': 'tag:Name', 'Values': [name]},
    ]

    if az:
        filters.append({'Name': 'availability-zone', 'Values': [az]})

    response = ec2.describe_instances(Filters=filters)

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']
            instance_id = instance['InstanceId']

            if state in ['running', 'pending']:
                print(f"Existed Instance '{name}' is {state}.")
                return instance_id
            elif state == 'stopped':
                print(f"Existed Instance '{name}' is {state}. Starting it...")
                ec2.start_instances(InstanceIds=[instance_id])
                return instance_id
            
    print(f"Launch request sent for {name} in {az}.")
    return _launch_instance(name, ami_id, instance_type, key_name, sg_id, az)

def _launch_instance(name, ami_id, instance_type, key_name, sg_id, az = None):
    """Launches a single, tagged EC2 instance."""
    run_params = {
        'ImageId': ami_id,
        'InstanceType': instance_type,
        'KeyName': key_name,
        'SecurityGroupIds': [sg_id],
        'MinCount': 1,
        'MaxCount': 1,
        'TagSpecifications': [
            {'ResourceType': 'instance', 
             'Tags': [{'Key': 'Name', 'Value': name}]}
        ]
    }

    if az:
        run_params['Placement'] = {'AvailabilityZone': az}

    response = ec2.run_instances(**run_params)
    return response['Instances'][0]['InstanceId']

def get_instance_ip(instance_id):
    """Waits for an instance and returns its public IP."""
    waiter = ec2.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[instance_id])
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')

def get_availability_zones():
    """Returns a list of availability zone names in the configured region."""
    response = ec2.describe_availability_zones()
    return [az['ZoneName'] for az in response['AvailabilityZones']]


    """Finds running or pending instances that match a list of 'Name' tags."""
    if not instance_names: return {}
    
    instances_found = {}
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': instance_names},
            {'Name': 'instance-state-name', 'Values': ['running', 'pending']}
        ]
    )
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_name = [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0]
            instances_found[instance_name] = instance['InstanceId']
    return instances_found

def get_all_subnet_ids():
    """Returns a list of all subnet IDs in the default VPC."""
    response = ec2.describe_subnets()
    return [subnet['SubnetId'] for subnet in response['Subnets']]