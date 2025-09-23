# lab7_main.py
# Main script to set up the infrastructure for Lab 7.

import sys
import os

# --- Add project root to the path to allow importing from 'utils' ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ---------------------------------------------------------------------

from utils import config
from utils import ec2_manager
from botocore.exceptions import ClientError

if __name__ == "__main__":
    instance_ids = []
    try:
        # --- Step 1: Create a EC2 instance ---
        print("--- Starting Lab 7 Infrastructure Setup ---")

        # --- User Configuration ---
        INSTANCE_NAME = f"{config.STUDENT_NUMBER}-vm-lab7"

        # Create the key pair
        ec2_manager.create_key_pair(config.LAB7_KEY_NAME)
        print(f"Ensured key pair '{config.LAB7_KEY_NAME}' is available.")

        # Define security rules
        lab7_sg_rules = [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8000, 'ToPort': 8000, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
        sg_id = ec2_manager.create_security_group(
            config.LAB7_SECURITY_GROUP_NAME,
            "Web Server Security Group for Lab 7",
            lab7_sg_rules
        )
        print(f"Ensured security group '{config.LAB7_SECURITY_GROUP_NAME}' is available.")

        print("\nLaunching instance...")
        instance_id = ec2_manager.setup_instance(
            name=INSTANCE_NAME,
            ami_id=config.AMI_ID,
            instance_type=config.LAB7_INSTANCE_TYPE,
            key_name=config.LAB7_KEY_NAME,
            sg_id=sg_id
        )
        instance_ids.append(instance_id)

        # Get IPs and print connection info
        print("\nWaiting for instance to initialize...")
        ip = ec2_manager.get_instance_ip(instance_id)
        print(f"-> {INSTANCE_NAME} is running at Public IP: {ip}")
        print(f"-> Connect using: ssh -i {config.LAB7_KEY_NAME}.pem ubuntu@{ip}")

        print("\n--- EC2 Setup Complete ---")
        print(f"Instance ready for Fabric automation.")
        print(f"Next: Install Fabric locally and create SSH config.")

    except ClientError as e:
        print(f"\nAn AWS error occurred: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")