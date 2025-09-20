import os
import boto3
import base64
import logging
from botocore.exceptions import ClientError


# Configuration
ROOT_DIR = '.'
BUCKET_NAME = '24745401-cloudstorage'
REGION = 'eu-north-1'  

s3 = boto3.client("s3")

def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name, 
                             CreateBucketConfiguration=location)
        print("Bucket created successfully")

    except ClientError as e:
        logging.error(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file 
    print("Uploading %s to bucket %s as %s" % (file_name, bucket, object_name))
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Main program
if __name__ == "__main__":
# check if bucket exists, if not create it
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        print("Bucket %s already exists" % BUCKET_NAME)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("Bucket %s does not exist. Creating it..." % BUCKET_NAME)
            create_bucket(BUCKET_NAME, REGION)
        else:
            logging.error(e)
            exit()


    # parse directory and upload files 
    for dir_name, subdir_list, file_list in os.walk(ROOT_DIR, topdown=True):
        if dir_name != ROOT_DIR:
            for fname in file_list:
                # Get the full path of the file
                file_path = os.path.join(dir_name, fname)

                # Gnerate the S3 object name
                object_path = os.path.join(dir_name[2:], fname)

                # Upload the file to S3
                upload_file(file_path, BUCKET_NAME, object_path);   

    print("done")
