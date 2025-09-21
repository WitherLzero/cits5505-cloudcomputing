import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Configuration
STUDENT_ID = '24745401'
REGION = 'eu-north-1'
BUCKET_NAME = f'{STUDENT_ID}-cloudstorage'
TABLE_NAME = 'CloudFiles'

# Boto3 resources
s3 = boto3.resource("s3", region_name=REGION)
bucket = s3.Bucket(BUCKET_NAME)
dynamodb = boto3.resource(
    'dynamodb', 
    region_name=REGION,
)

# Local DynamoDB resource
local_dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name=REGION,
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def create_dynamodb_table():
    print(f"Checking for DynamoDB table '{TABLE_NAME}' in AWS cloud...")
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'userId', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'fileName', 'KeyType': 'RANGE'} # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'userId', 'AttributeType': 'S'},
                {'AttributeName': 'fileName', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        # Wait until the table exists.
        table.wait_until_exists()
        print(f"Table '{TABLE_NAME}' created successfully in AWS.")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{TABLE_NAME}' already exists in AWS.")
            return dynamodb.Table(TABLE_NAME)
        else:
            print(f"Error creating table: {e}")
            raise    


def store_s3_metadata_in_dynamodb(table):
    print(f"\nScanning bucket '{BUCKET_NAME}' for file metadata...")
    try:
        for obj in bucket.objects.all():
            print(f"  -> Processing s3://{BUCKET_NAME}/{obj.key}")
            
            acl = obj.Acl()
            owner = acl.owner.get('DisplayName', acl.owner.get('ID')) # Safely get owner name or ID
            permissions = "rw-r--r--" # Placeholder for permissions
            
            table.put_item(
                Item={
                    'userId': STUDENT_ID,
                    'fileName': os.path.basename(obj.key),
                    'path': obj.key,
                    'lastUpdated': obj.last_modified.strftime("%Y-%m-%d %H:%M:%S"),
                    'owner': owner,
                    'permissions': permissions
                }
            )
        print("\nMetadata successfully stored in DynamoDB.")
    except Exception as e:
        print(f"An error occurred while processing S3 objects: {e}")


def create_local_dynamodb_table():
    print(f"Checking for DynamoDB table '{TABLE_NAME}' in local DynamoDB...")
    try:
        table = local_dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'userId', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'fileName', 'KeyType': 'RANGE'} # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'userId', 'AttributeType': 'S'},
                {'AttributeName': 'fileName', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
        print(f"Table '{TABLE_NAME}' created successfully in local DynamoDB.")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{TABLE_NAME}' already exists in local DynamoDB.")
            return local_dynamodb.Table(TABLE_NAME)
        else:
            print(f"Error creating local table: {e}")
            raise


if __name__ == "__main__":
    # Create AWS table and store S3 metadata
    cloudfiles_table = create_dynamodb_table()
    if cloudfiles_table:
        store_s3_metadata_in_dynamodb(cloudfiles_table)
        print("AWS DynamoDB table setup completed successfully.")

    # Create local table and store the same S3 metadata
    local_table = create_local_dynamodb_table()
    if local_table:
        store_s3_metadata_in_dynamodb(local_table)
        print("Local DynamoDB table setup completed successfully.")
        
    print("\nAll setup completed!")