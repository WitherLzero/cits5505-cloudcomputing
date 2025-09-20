import boto3
from botocore.exceptions import ClientError
import os

# --- Configuration ---
# Replace with your details
STUDENT_NUMBER = "24745401"
BUCKET_NAME = f"{STUDENT_NUMBER}-lab4-bucket"
KEY_ALIAS = f"alias/{STUDENT_NUMBER}"

# Initialize Boto3 clients
s3 = boto3.client('s3')
kms = boto3.client('kms')

# Temporary local directory for processing files
DOWNLOAD_DIR = "/tmp/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def encrypt_decrypt_cycle():
    """
    Encrypts and decrypts each file in the S3 bucket using the KMS key.
    """
    try:
        print(f"Listing files in bucket '{BUCKET_NAME}'...")
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        if 'Contents' not in response:
            print("No files found in the bucket.")
            return

        for obj in response['Contents']:
            file_key = obj['Key']
            # Skip any previously encrypted/decrypted files to avoid loops
            if file_key.endswith('.encrypted') or file_key.endswith('.decrypted'):
                continue

            print(f"\n--- Processing file: {file_key} ---")
            local_path = os.path.join(DOWNLOAD_DIR, os.path.basename(file_key))

            # 1. Download original file from S3
            print("Downloading original file...")
            s3.download_file(BUCKET_NAME, file_key, local_path)
            
            with open(local_path, 'rb') as f:
                plaintext = f.read()

            # 2. Encrypt the file content using KMS
            print("Encrypting with KMS...")
            encrypt_response = kms.encrypt(
                KeyId=KEY_ALIAS,
                Plaintext=plaintext
            )
            ciphertext_blob = encrypt_response['CiphertextBlob']
            
            # 3. Upload the encrypted file to S3
            encrypted_key = f"{file_key}.encrypted"
            print(f"Uploading encrypted file to {encrypted_key}...")
            s3.put_object(Bucket=BUCKET_NAME, Key=encrypted_key, Body=ciphertext_blob)

            # 4. Decrypt the file content using KMS
            print("Decrypting with KMS...")
            decrypt_response = kms.decrypt(
                CiphertextBlob=ciphertext_blob
            )
            decrypted_plaintext = decrypt_response['Plaintext']

            # 5. Upload the decrypted file to S3 to verify
            decrypted_key = f"{file_key}.decrypted"
            print(f"Uploading decrypted file to {decrypted_key}...")
            s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_key, Body=decrypted_plaintext)

            print(f"Successfully completed cycle for {file_key}.")

    except ClientError as e:
        print(f"An error occurred: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    encrypt_decrypt_cycle()