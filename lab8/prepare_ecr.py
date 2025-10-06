import boto3
import base64

def create_or_check_repository(repository_name):
    ecr_client = boto3.client('ecr')
    try:
        response = ecr_client.describe_repositories(repositoryNames=[repository_name])
        repository_uri = response['repositories'][0]['repositoryUri']
    except ecr_client.exceptions.RepositoryNotFoundException:
        response = ecr_client.create_repository(repositoryName=repository_name)
        repository_uri = response['repository']['repositoryUri']
    return repository_uri

def get_docker_login_cmd():
    ecr_client = boto3.client('ecr')
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    registry = token['authorizationData'][0]['proxyEndpoint']
    return f"docker login -u {username} -p {password} {registry}"

if __name__ == "__main__":
    repository_name = '24745401_ecr_repo'
    repository_uri = create_or_check_repository(repository_name)
    print("ECR URI:", repository_uri)
    print(get_docker_login_cmd())