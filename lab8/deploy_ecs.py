import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils import config
from utils import ecs_manager
from utils import ec2_manager
import boto3

if __name__ == "__main__":
    ecs_client = boto3.client('ecs')

    ecr_uri = '489389878001.dkr.ecr.eu-north-1.amazonaws.com/24745401_ecr_repo:latest'

    # Create Task Definition
    task_definition_response = ecs_manager.create_ecs_task_definition(
        ecs_client,
        image_uri=ecr_uri,
        account_id=config.ACCOUNT_ID,
        task_role_name='SageMakerRole',
        execution_role_name='ecsTaskExecutionRole',
        student_id=config.STUDENT_NUMBER,
        log_group='/ecs/lab8-service', 
        log_region=config.REGION_NAME,
        port=8888
    )
    task_definition_arn = task_definition_response['taskDefinition']['taskDefinitionArn']
    print(f"Task Definition ARN: {task_definition_arn}")

    # Create Cluster
    cluster_name = f'{config.STUDENT_NUMBER}-cluster'
    ecs_manager.create_ecs_cluster(ecs_client, cluster_name)
    print(f"ECS Cluster: {cluster_name}")

    # Get Subnets and Security Group
    subnet_ids = ec2_manager.get_all_subnet_ids()
    lab8_sg_rules = [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8888, 'ToPort': 8888, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    sg_id = ec2_manager.create_security_group(
        config.MY_SECURITY_GROUP_NAME, 
        "Security Group for general use", 
        lab8_sg_rules
    )

    # Create Service
    service_name = f'{config.STUDENT_NUMBER}-service'
    service_response = ecs_manager.create_ecs_service(
        ecs_client, 
        cluster_name, 
        service_name, 
        task_definition_arn, 
        subnet_ids, 
        [sg_id]
    )
    print(f'ECS Service created: {service_response["service"]["serviceArn"]}')

    print(f'Waiting for service {service_name} to become stable...')
    ecs_manager.wait_for_service_stability(ecs_client, cluster_name, service_name)
    print(f'Service {service_name} is now stable.')