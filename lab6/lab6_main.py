# lab6_main.py
# Main script to set up the infrastructure for Lab 6.

import sys
import os

# --- Add project root to the path to allow importing from 'utils' ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ---------------------------------------------------------------------

from utils import config
from utils import ec2_manager
from utils import elb_manager
from botocore.exceptions import ClientError

if __name__ == "__main__":
    instance_ids = []
    try:
        # --- Step 1: Create a EC2 instance ---
        print("--- Starting Lab 6 Infrastructure Setup ---")

        # --- User Configuration ---
        INSTANCE_NAME = f"{config.STUDENT_NUMBER}-vm-lab6"

        # Create the key pair
        ec2_manager.create_key_pair(config.LAB6_KEY_NAME)
        print(f"Ensured key pair '{config.LAB6_KEY_NAME}' is available.")

        # Define security rules
        lab6_sg_rules = [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
        sg_id = ec2_manager.create_security_group(
            config.LAB6_SECURITY_GROUP_NAME, 
            "Web Server Security Group for Lab 6", 
            lab6_sg_rules
        )
        print(f"Ensured security group '{config.LAB6_SECURITY_GROUP_NAME}' is available.")

        print("\nLaunching instance...")
        instance_id = ec2_manager.setup_instance(
            name=INSTANCE_NAME, 
            ami_id=config.AMI_ID, 
            instance_type=config.LAB6_INSTANCE_TYPE,
            key_name=config.LAB6_KEY_NAME, 
            sg_id=sg_id
        )
        instance_ids.append(instance_id)

        # Get IPs and print connection info
        print("\nWaiting for instance to initialize...")
        ip = ec2_manager.get_instance_ip(instance_id)
        print(f"-> {INSTANCE_NAME} is running at Public IP: {ip}")
        print(f"-> Connect using: ssh -i {config.LAB6_KEY_NAME}.pem ubuntu@{ip}")

        print("\n--- EC2 Setup Complete ---")

        # --- Step 2: Create the Application Load Balancer ---
        print("\nProceeding to create the Application Load Balancer...")
        all_subnet_ids = ec2_manager.get_all_subnet_ids()
        if len(all_subnet_ids) < 2:
            raise Exception("Cannot create ALB, not enough subnets in the VPC.")

        alb_dns_name = elb_manager.setup_load_balancer(
            alb_name=config.LAB6_ALB_NAME,
            security_group_id=sg_id,
            subnet_ids=all_subnet_ids,
            instance_ids=instance_ids,
            health_check_path='/polls/'  # Lab 6 specific requirement
        )

        print("\n--- ALB Setup Complete ---")
        print(f"-> Access it at: http://{alb_dns_name}/polls/")
        
        print("\n--- Lab 6 Infrastructure Complete ---")
        print(f"Direct EC2 access: http://{ip}/polls/")
        print(f"Load Balancer access: http://{alb_dns_name}/polls/")

    except ClientError as e:
        print(f"\nAn AWS error occurred: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")