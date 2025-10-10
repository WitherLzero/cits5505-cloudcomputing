#!/usr/bin/env python3
"""
Lab 9 - Setup S3 Bucket for AWS Rekognition
Creates S3 bucket and uploads images.
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils import config
import boto3
import logging
from botocore.exceptions import ClientError

# Configuration
BUCKET_NAME = f'{config.STUDENT_NUMBER}-lab9-in-ap'
REGION = 'ap-southeast-2'  # Use Rekognition region for S3 bucket
IMAGES_DIR = './images'

s3 = boto3.client("s3", region_name=REGION)

def create_bucket(bucket_name, region=None):
    # Check if bucket exists, if not create it
    try:
        s3.head_bucket(Bucket=bucket_name)
        print("Bucket %s already exists" % bucket_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("Bucket %s does not exist. Creating it..." % bucket_name)
            try:
                if region is None:
                    s3.create_bucket(Bucket=bucket_name)
                else:
                    location = {'LocationConstraint': region}
                    s3.create_bucket(Bucket=bucket_name,
                                     CreateBucketConfiguration=location)
                print("Bucket created successfully")
                return True
            except ClientError as create_error:
                logging.error(create_error)
                return False
        else:
            logging.error(e)
            return False

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
    # Create bucket (checks if exists inside function)
    if not create_bucket(BUCKET_NAME, REGION):
        print("Failed to create or access bucket")
        exit()

    # Upload images from images directory
    if os.path.exists(IMAGES_DIR):
        for fname in os.listdir(IMAGES_DIR):
            if fname.endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(IMAGES_DIR, fname)
                upload_file(file_path, BUCKET_NAME, fname)
    else:
        print("Images directory not found. Please create '%s' and add your images:" % IMAGES_DIR)
        print("  - urban.jpg: An image of an urban setting")
        print("  - beach.jpg: An image of a person on the beach")
        print("  - faces.jpg: An image with people showing their faces")
        print("  - text.jpg: An image with text")

    print("done")
