import boto3
from botocore.exceptions import ClientError

def create_ecs_cluster(client, cluster_name):
    response = client.describe_clusters(clusters=[cluster_name])
    active_clusters = [c for c in response.get('clusters', []) if c['status'] == 'ACTIVE']
    if active_clusters:
        print(f"Cluster '{cluster_name}' already exists and is active.")
        return {'cluster': active_clusters[0]}
    
    print(f"Cluster '{cluster_name}' not found or not active. Creating...")
    response = client.create_cluster(clusterName=cluster_name)
    return response

def create_ecs_task_definition(
    client, image_uri, account_id, task_role_name, execution_role_name, student_id,
    environment_dict=None, log_group=None, log_region=None, port=8888, cpu='256', memory='512'
):
    task_role_arn = f'arn:aws:iam::{account_id}:role/{task_role_name}'
    execution_role_arn = f'arn:aws:iam::{account_id}:role/{execution_role_name}'

    env_list = [{'name': k, 'value': v} for k, v in (environment_dict or {}).items()]
    
    response = client.register_task_definition(
        family=f'{student_id}-task-family',
        networkMode='awsvpc',
        requiresCompatibilities=['FARGATE'],
        cpu=cpu,
        memory=memory,
        taskRoleArn=task_role_arn,
        executionRoleArn=execution_role_arn,
        containerDefinitions=[
            {
                'name': f'{student_id}-container',
                'image': image_uri,
                'essential': True,
                'portMappings': [
                    {
                        'containerPort': port,
                        'hostPort': port,
                        'protocol': 'tcp'
                    },
                ]
            },
        ],
    )
    return response

def create_ecs_service(client, cluster_name, service_name, task_definition, subnet_ids, security_group_ids):
    response = client.describe_services(cluster=cluster_name, services=[service_name])
    active_services = [s for s in response.get('services', []) if s['status'] == 'ACTIVE']
    if active_services:
        print(f"Service '{service_name}' already exists and is active.")
        return {'service': active_services[0]}

    print(f"Service '{service_name}' not found or not active. Creating...")
    response = client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_definition,
        desiredCount=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnet_ids,
                'securityGroups': security_group_ids,
                'assignPublicIp': 'ENABLED'
            }
        },
        deploymentConfiguration={
            'maximumPercent': 200,
            'minimumHealthyPercent': 100
        }
    )
    return response

def wait_for_service_stability(client, cluster_name, service_name):
    waiter = client.get_waiter('services_stable')
    waiter.wait(cluster=cluster_name, services=[service_name])
