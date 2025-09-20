# config.py
# Centralized settings for the CITS5503 labs.

# --- General AWS Configuration ---
STUDENT_NUMBER = "24745401"
REGION_NAME = "eu-north-1" 
AMI_ID = "ami-042b4708b1d05f512" 

# --- Lab 5 Specific Configuration ---
LAB5_KEY_NAME = f"{STUDENT_NUMBER}-key-lab5"
LAB5_INSTANCE_TYPE = "t3.micro"
LAB5_SECURITY_GROUP_NAME = f"{STUDENT_NUMBER}-sg-lab5"

# --- Lab 6 Specific Configuration ---
LAB6_KEY_NAME = f"{STUDENT_NUMBER}-key-lab6"
LAB6_INSTANCE_TYPE = "t3.micro"
LAB6_SECURITY_GROUP_NAME = f"{STUDENT_NUMBER}-sg-lab6"
