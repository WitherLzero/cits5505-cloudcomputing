import os
import boto3
import logging
from botocore.exceptions import ClientError

# Configuration
BUCKET_NAME = '24745401-cloudstorage'
REGION = 'eu-north-1'

# Boto3 client 
s3 = boto3.client("s3", region_name=REGION)

def restore_file(bucket_name):
    try:
        print("Fetching file list from bucket: %s" % bucket_name)
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' not in response:
            print("No files found in bucket %s" % bucket_name)
            return
        
        print("Beginning restoration of files...")
        for obj in response['Contents']:
            obj_name = obj['Key']

            local_file_path = obj_name

            local_dir = os.path.dirname(local_file_path)
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)

            print("Restoring file %s from s3://%s/%s to ./%s" 
                  % (obj_name, bucket_name, obj_name, local_file_path))
            s3.download_file(bucket_name, obj_name, local_file_path)
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print("Bucket %s does not exist." % bucket_name)
        else:
            logging.error(e)
            exit()

if __name__ == "__main__":
    restore_file(BUCKET_NAME)
    print("done")