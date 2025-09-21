# utils/elb_manager.py
# A reusable module for managing Application Load Balancers.

import boto3
from botocore.exceptions import ClientError
from . import config

elbv2 = boto3.client('elbv2', region_name=config.REGION_NAME)
ec2 = boto3.client('ec2', region_name=config.REGION_NAME)

def setup_load_balancer(alb_name, security_group_id, subnet_ids, instance_ids, health_check_path='/'):
    """
    Ensures a complete ALB setup exists, creating components as needed.
    """
    # 1. Ensure Load Balancer exists
    alb_arn, alb_dns_name = _create_load_balancer(alb_name, security_group_id, subnet_ids)
    
    # 2. Ensure Target Group exists
    tg_name = f"{alb_name}-tg"
    target_group_arn = _create_target_group(tg_name, health_check_path)
    
    # 3. Register targets 
    print("Registering instances with Target Group...")
    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[{'Id': instance_id} for instance_id in instance_ids]
    )
    
    # 4. Ensure Listener exists
    _create_listener(alb_arn, target_group_arn)
    
    return alb_dns_name

def _create_load_balancer(alb_name, security_group_id, subnet_ids):
    """Creates a new Application Load Balancer."""
    try:
        vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
        lb_response = elbv2.create_load_balancer(
            Name=alb_name, Subnets=subnet_ids, SecurityGroups=[security_group_id],
            Scheme='internet-facing', Type='application'
        )
        alb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
        alb_dns = lb_response['LoadBalancers'][0]['DNSName']
        print(f"Created Load Balancer '{alb_name}'.")
        return alb_arn, alb_dns
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateLoadBalancerName':
            response = elbv2.describe_load_balancers(Names=[alb_name])
            alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
            alb_dns = response['LoadBalancers'][0]['DNSName']
            print(f"Existed Load Balancer '{alb_name}'.")
            return alb_arn, alb_dns
        else:
            raise

def _create_target_group(tg_name, health_check_path='/'):
    """Creates a new Target Group."""
    try:
        vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
        tg_response = elbv2.create_target_group(
            Name=tg_name, Protocol='HTTP', Port=80, VpcId=vpc_id,
            HealthCheckProtocol='HTTP', HealthCheckPath=health_check_path,
            HealthCheckIntervalSeconds=30,  # Check every 30 seconds as per worksheet
            TargetType='instance'
        )
        tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
        print(f"Created Target Group '{tg_name}'.")
        return tg_arn
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateTargetGroupName':
            response = elbv2.describe_target_groups(Names=[tg_name])
            tg_arn = response['TargetGroups'][0]['TargetGroupArn']
            print(f"Existed Target Group '{tg_name}'.")
            return tg_arn
        else:
            raise

def _create_listener(alb_arn, tg_arn):
    """Creates a Listener for the ALB."""
    try:
        elbv2.create_listener(
            LoadBalancerArn=alb_arn, Protocol='HTTP', Port=80,
            DefaultActions=[{'Type': 'forward', 'TargetGroupArn': tg_arn}]
        )
        print("Created Listener for the Load Balancer.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateListener':
            print("Existed Listener for the Load Balancer.")
        else:
            raise



