# lab5_main.py
# Main script to set up the infrastructure for Lab 5.

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
        # --- Step 1: Create 2 EC2 instances ---
        print("--- Starting Lab 5 Infrastructure Setup ---")

        # --- User Configuration ---
        INSTANCE_COUNT = 2

        # Create the key pair
        ec2_manager.create_key_pair(config.LAB5_KEY_NAME)
        print(f"Ensured key pair '{config.LAB5_KEY_NAME}' is available.")

        # Define security rules
        lab5_sg_rules = [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
        sg_id = ec2_manager.create_security_group(
            config.LAB5_SECURITY_GROUP_NAME, 
            "Web Server Security Group for Lab 5", 
            lab5_sg_rules
        )
        print(f"Ensured security group '{config.LAB5_SECURITY_GROUP_NAME}' is available.")

        # Get zones and launch instances
        zones = ec2_manager.get_availability_zones()
        if len(zones) == 0:
            raise Exception("No availability zones found in this region.")
        
        print("\nLaunching instances...")
        for i in range(INSTANCE_COUNT):
            instance_name = f"{config.STUDENT_NUMBER}-vm{i+1}"
            
            zone_to_use = zones[i % len(zones)]

            instance_id = ec2_manager.setup_instance(
                name=instance_name, 
                ami_id=config.AMI_ID, 
                instance_type=config.LAB5_INSTANCE_TYPE,
                key_name=config.LAB5_KEY_NAME, 
                sg_id=sg_id, 
                az=zone_to_use
            )
            instance_ids.append(instance_id)

        # Get IPs and print connection info
        print("\nWaiting for instances to initialize...")
        for i, instance_id in enumerate(instance_ids):
            ip = ec2_manager.get_instance_ip(instance_id)
            instance_name = f"{config.STUDENT_NUMBER}-vm{i+1}"
            print(f"-> {instance_name} is running at Public IP: {ip}")
            print(f"   Connect with: ssh -i {config.LAB5_KEY_NAME}.pem ubuntu@{ip}")
        
        print("\n--- EC2 Setup Complete ---")
        
        # --- Step 2: Create the Application Load Balancer ---
        print("\nProceeding to create the Application Load Balancer...")
        all_subnet_ids = ec2_manager.get_all_subnet_ids()
        if len(all_subnet_ids) < 2:
            raise Exception("Cannot create ALB, not enough subnets in the VPC.")

        alb_dns_name = elb_manager.setup_load_balancer(
            alb_name=f"{config.STUDENT_NUMBER}-alb",
            security_group_id=sg_id,
            subnet_ids=all_subnet_ids,
            instance_ids=instance_ids
        )

        print("\n--- ALB Setup Complete ---")
        print(f"->  Access it at: http://{alb_dns_name}")

    except ClientError as e:
        print(f"\nAn AWS error occurred: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

