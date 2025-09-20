import boto3
import json
from botocore.exceptions import ClientError

# --- Configuration ---
# Replace with your student number and IAM username
STUDENT_NUMBER = "24745401"
IAM_USERNAME = f"{STUDENT_NUMBER}@student.uwa.edu.au"
KEY_ALIAS = f"alias/{STUDENT_NUMBER}"

# Initialize Boto3 KMS client
kms = boto3.client('kms')


def create_kms_key():
    """Creates a new KMS key and an alias, then returns the key's ID."""
    try:
        print("Creating a new KMS key...")
        key_response = kms.create_key(
            Description="KMS key for CITS5503 Lab 4",
            KeyUsage="ENCRYPT_DECRYPT"
        )
        key_id = key_response['KeyMetadata']['KeyId']
        print(f"Successfully created key with ID: {key_id}")

        print(f"Creating alias '{KEY_ALIAS}' for key {key_id}...")
        kms.create_alias(AliasName=KEY_ALIAS, TargetKeyId=key_id)
        print("Successfully created alias.")
        
        # Return the ID so it can be used by other functions
        return key_id

    except ClientError as e:
        if e.response['Error']['Code'] == 'AlreadyExistsException':
            print(f"Warning: Alias '{KEY_ALIAS}' already exists. Please delete it from the AWS KMS console and re-run.")
            return None
        else:
            print(f"An unexpected error occurred during key creation: {e}")
            return None


def attach_key_policy(key_id):
    """Attaches the predefined security policy to the specified KMS key."""
    if not key_id:
        print("No key ID provided. Skipping policy attachment.")
        return

    # Define the Key Policy
    policy = {
        "Version": "2012-10-17",
        "Id": "key-consolepolicy-3",
        "Statement": [
            {
                "Sid": "Enable IAM User Permissions",
                "Effect": "Allow",
                "Principal": {"AWS": "arn:aws:iam::489389878001:root"},
                "Action": "kms:*",
                "Resource": "*"
            },
            {
                "Sid": "Allow access for Key Administrators",
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"},
                "Action": [
                    "kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*",
                    "kms:Update*", "kms:Revoke*", "kms:Disable*", "kms:Get*", "kms:Delete*",
                    "kms:TagResource", "kms:UntagResource", "kms:ScheduleKeyDeletion", "kms:CancelKeyDeletion"
                ],
                "Resource": "*"
            },
            {
                "Sid": "Allow use of the key",
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"},
                "Action": ["kms:Encrypt", "kms:Decrypt", "kms:ReEncrypt*", "kms:GenerateDataKey*", "kms:DescribeKey"],
                "Resource": "*"
            }
        ]
    }

    try:
        print(f"Attaching key policy to key {key_id}...")
        kms.put_key_policy(
            KeyId=key_id,
            PolicyName='default',
            Policy=json.dumps(policy)
        )
        print("Successfully attached key policy.")
    except ClientError as e:
        print(f"An unexpected error occurred during policy attachment: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    # Call the first function and store its result (the key_id)
    new_key_id = create_kms_key()
    
    # Pass the key_id to the second function
    attach_key_policy(new_key_id)