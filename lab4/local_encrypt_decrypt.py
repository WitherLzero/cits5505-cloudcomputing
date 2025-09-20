import boto3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# --- Configuration ---
STUDENT_NUMBER = "24745401"
BUCKET_NAME = f"{STUDENT_NUMBER}-lab4-bucket"
PASSWORD = "my-super-secret-password" 
s3 = boto3.client('s3')

# --- Cryptographic Functions ---
def encrypt(plaintext, password):
    """Encrypts plaintext using a password-derived key and AES CBC mode."""
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Pad the plaintext to be a multiple of the AES block size (16 bytes)
    padded_plaintext = plaintext + b'\0' * (AES.block_size - len(plaintext) % AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Return the combined salt, iv, and ciphertext for storage
    return salt + cipher.iv + ciphertext

def decrypt(encrypted_data, password):
    """Decrypts data that was encrypted using the above function."""
    # Extract the salt, iv, and ciphertext from the combined data
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    
    # Re-derive the key using the extracted salt and the original password
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_padded = decipher.decrypt(ciphertext)
    
    # Unpad the plaintext by stripping the null bytes
    return decrypted_padded.rstrip(b'\0')

# --- Main S3 Processing Function ---
def local_encrypt_decrypt_cycle():
    """Handles S3 operations and calls crypto functions."""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' not in response:
            print("No files to process.")
            return

        for obj in response['Contents']:
            file_key = obj['Key']
            # Process only original files, skip already processed ones
            if not file_key.startswith('rootdir/') or 'local' in file_key:
                continue
            
            print(f"\n--- Processing cycle for: {file_key} ---")
            
            # Download
            original_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
            plaintext = original_object['Body'].read()

            # Encrypt using the dedicated function
            encrypted_blob = encrypt(plaintext, PASSWORD)
            
            # Upload encrypted file
            encrypted_key = f"{file_key}.localencrypted"
            s3.put_object(Bucket=BUCKET_NAME, Key=encrypted_key, Body=encrypted_blob)
            print(f"Uploaded encrypted file to {encrypted_key}")

            # Download encrypted file for decryption
            encrypted_object_from_s3 = s3.get_object(Bucket=BUCKET_NAME, Key=encrypted_key)
            encrypted_data_from_s3 = encrypted_object_from_s3['Body'].read()

            # Decrypt using the dedicated function
            decrypted_text = decrypt(encrypted_data_from_s3, PASSWORD)

            # Upload decrypted file for verification
            decrypted_key = f"{file_key}.localdecrypted"
            s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_key, Body=decrypted_text)
            print(f"Uploaded decrypted file to {decrypted_key}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    local_encrypt_decrypt_cycle()