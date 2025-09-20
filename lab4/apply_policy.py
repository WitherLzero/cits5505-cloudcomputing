import boto3
import json
from botocore.exceptions import ClientError

# --- Configuration ---
# Replace these with your actual details
BUCKET_NAME = "24745401-lab4-bucket"
STUDENT_NUMBER = "24745401"
# The folder within your bucket you want to protect
FOLDER_NAME = "rootdir"

# Initialize Boto3 S3 client
s3 = boto3.client('s3')

# Define the bucket policy 
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "AllowS3ActionsInUserFolderForUserOnly",
        "Effect": "DENY",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": f"arn:aws:s3:::{BUCKET_NAME}/{FOLDER_NAME}/*",
        "Condition": {
            "StringNotLike": {
                "aws:username": f"{STUDENT_NUMBER}@student.uwa.edu.au"
            }
        }
    }]
}

# --- Main Execution ---
try:
    # 1. Explicitly check if the bucket exists
    print(f"Verifying bucket '{BUCKET_NAME}' exists...")
    s3.head_bucket(Bucket=BUCKET_NAME)
    print("Bucket found.")

    # 2. Convert the policy to a JSON string and apply it
    policy_string = json.dumps(bucket_policy)
    
    print("Applying security policy...")
    s3.put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=policy_string
    )
    print(f"Successfully applied policy to bucket '{BUCKET_NAME}'.")

except ClientError as e:
    # Handle specific errors
    if e.response['Error']['Code'] == '404':
        print(f"Error: Bucket '{BUCKET_NAME}' does not exist.")
    else:
        print(f"An unexpected error occurred: {e}")