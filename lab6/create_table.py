import boto3
from botocore.exceptions import ClientError

# Configuration
STUDENT_ID = '24745401'
REGION = 'eu-north-1'
TABLE_NAME = 'UserFiles'  # Using the table name from Lab 6 instructions

def create_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb', 
        region_name=REGION
    )
    
    print(f"Creating DynamoDB table '{TABLE_NAME}' in AWS cloud...")
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

def copy_data_from_local_to_aws():
    # Connect to local DynamoDB
    source_dynamodb = boto3.resource(
        'dynamodb', 
        endpoint_url='http://localhost:8000',  # Local DynamoDB endpoint
        region_name='eu-north-1',  # Using the same region as AWS
        aws_access_key_id='dummy',  # Dummy credentials for local
        aws_secret_access_key='dummy'
    )
    source_table = source_dynamodb.Table('CloudFiles')  # Your local table name
    
    # Connect to AWS DynamoDB
    dest_dynamodb = boto3.resource(
        'dynamodb', 
        region_name=REGION,
   )
    dest_table = dest_dynamodb.Table(TABLE_NAME)
    
    # Scan all items from local table
    try:
        response = source_table.scan()
        items = response.get('Items', [])
        
        print(f"Found {len(items)} items in local DynamoDB")
        
        # Copy each item to AWS table
        for item in items:
            dest_table.put_item(Item=item)
            print(f"Copied item: {item.get('fileName', 'unknown')}")
            
        print(f"Successfully copied {len(items)} items to AWS DynamoDB table {TABLE_NAME}")
    except Exception as e:
        print(f"Error copying data: {e}")

if __name__ == "__main__":
    table = create_dynamodb_table()
    if table:
        copy_data_from_local_to_aws()