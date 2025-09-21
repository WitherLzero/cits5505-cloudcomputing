<div class="cover-page">
  <div class="cover-content">
    <div style="font-size: 2em; font-weight: bold;">Labs 1-5</div>
    <p>Student ID: 24745401</p>
    <p>Student Name: Xinqi Lin</p>
  </div>
</div>


<div style="page-break-after: always;"></div

# Lab 1

## AWS Account and Log in

### [1] Log into an IAM user account created for you on AWS.

The first step was to sign in the IAM user account on AWS. On the login page, I entered the provided account name and password. After signing in successfully,  I followed the prompt to change the temporary password to a new, personal one for security purposes.

#### Result:

![573cff787b948134aeb90d696f3315b9](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/573cff787b948134aeb90d696f3315b9.jpg) 

The screenshot above confirms my successful login to the AWS Management Console, using the assigned username and my newly created secure password.

### [2] Search and open Identity Access Management

To enable programmatic access to AWS via the command line or scripts, it was necessary to generate an Access Key and a Secret Access Key. I navigated to the **"Security credentials"** tab for my user account and clicked the **"Create access key"** button. After selecting the appropriate use case, I retrieved the generated access key and secret key, and then saved them securely to my local computer.

## Set up recent Unix-like OSes

### [1] Preparing the WSL2 on Windows 11

To create a suitable Unix-like environment on my Windows 11 machine, my first step was to enable the Windows Subsystem for Linux (WSL). I navigated to the "Turn Windows features on or off" panel, selected the WSL option, and then restarted my laptop to apply the necessary changes.

After the system rebooted, I opened the command prompt to verify the installation and ensure it was up-to-date. 

#### Command:

First, to check the current status of WSL:

```powershell
wsl --status
```

Next, to ensure all WSL components were updated to the latest version:

```powershell
wsl --update
```

### [2] Installing the Ubuntu 22.04 LTS

With WSL2 updated and ready, the next step was to install the specific Linux distribution required for the lab: Ubuntu 22.04 LTS.

#### Command:

First, I listed all the available distributions to find the exact name for the installation command.:

```powershell
wsl --list --online
```

The command returned a comprehensive list, from which I identified `Ubuntu-22.04`.

Next, I proceeded with the installation.:

```powershell
wsl --install -d Ubuntu-22.04
```

​	This command downloaded and installed the Ubuntu 22.04 LTS distribution. Upon completion, the terminal launched automatically for its one-time initial setup. During this process, I was prompted to create a default user account by providing a new username and a secure password. This user is now the default for the system and has the necessary administrative (`sudo`) privileges for subsequent tasks.

Finally, to verify the installation was successful:

```powershell
wsl --list
```

#### **Result: ** 

The output confirmed the successful installation:

```powershell
Windows Subsystem for Linux distributions:
Ubuntu-22.04 (Default)
```

## Install Linux packages

### [1] Install Python

First, I ensured the Python environment was correctly set up by updating the system's package manager and then installing `pip`, the package installer for Python.

#### Command:

To update all system packages to their latest versions:

```bash
sudo apt update && sudo apt -y upgrade
```

To install the Python package installer:

```bash
sudo apt install -y python3-pip
```

Finally, to verify the installation was successful, I checked the versions of both tools:

```bash
python3 -V
pip3 -V
```

#### **Result: ** 

The screenshot below comfirms my successful installation.

![image-20250731003222728](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731003222728.png)  

### [2] Install awscli

Next, I installed the AWS Command Line Interface (CLI) to enable interaction with AWS services from the terminal. The process involved installing the base package and then upgrading it to the latest version using pip for full functionality.

#### Command:

To install and upgrade the AWS CLI:

```bash
sudo apt install awscli
pip3 install awscli --upgrade
```

To verify the installation was successful:

```bash
aws --version
```

#### **Result: ** 

The screenshot below comfirms my successful installation.

![image-20250731003740880](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731003740880.png)  

### [3] Configure AWS

To link the AWS CLI to my IAM user account, I ran the configuration command. This securely stores the necessary credentials for programmatic access.

#### Command:

To begin the configuration process:

```bash
aws configure
```

This command presented a series of prompts. I entered my personal **AWS Access Key ID**, **AWS Secret Access Key**, my assigned **Default region name**, and `json` for the **Default output format**.

#### **Result: ** 

The screenshot below comfirms my successful configuration.

![image-20250731005224081](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731005224081.png)   

### [4] Install boto3

The final package to install was Boto3, the official AWS SDK for Python, which allows scripts to manage AWS resources.

#### Command:

To install the Boto3 library

```bash
pip3 install boto3
```

To confirm that the library was installed correctly

```bash
pip3 show boto3
```

#### **Result: ** 

The screenshot below comfirms my successful installation.

![image-20250731005502952](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731005502952.png)    

## Test the installed environment

### [1] Test the AWS environment

First, I verified that the AWS CLI could successfully communicate with AWS using the credentials I configured. I ran a command to describe the available AWS regions.

#### Command:

To test the AWS CLI connection:

```bash
aws ec2 describe-regions --output table
```

#### **Result: ** 

The screenshot below shows the command returned a formatted table of all available regions, which confirmed that the CLI was properly installed and authenticated.

![](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731010640989.png)     

### [2] Test the Python environment

Next, I tested the Python environment to ensure the Boto3 library could also connect to AWS. For a more comfortable experience, I used VS Code's remote development features to connect directly to my WSL2 environment.

To open VS Code and connect to my Ubuntu-22.04:

![image-20250731011142153](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731011142153.png)  

Within VS Code, I created a directory for codes and a new Python script called `lab1_untabulatedResp.py` with following content:

#### Code:

```python
import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_regions()
print(response)
```

#### **Result: ** 

I ran the code, and the output in the screenshot below confirms that Boto3 is correctly installed and authenticated.

![](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731011839863.png)      

### [3] Write a Python script

The final task was to write a Python script that fetches the AWS regions and presents the data in a clean, tabulated format.

#### Code:

```python
# lab1_tabulatedResp.py
import boto3

# Create a client to interact with the EC2 service
ec2 = boto3.client('ec2')

# Retrieve a list of all AWS regions for the EC2 service
response = ec2.describe_regions()

# Print the table headers, formatted to align
print(f"{'RegionName':<20} {'Endpoint':<40}")
print("-" * 60) # Print a separator line

# Loop through each region dictionary in the 'Regions' list
for region in response['Regions']:
    # Extract the RegionName and Endpoint for each region
    region_name = region['RegionName']
    endpoint = region['Endpoint']

    # Print the formatted row
    print(f"{region_name:<20} {endpoint:<40}")
```

#### Explanation:

This script demonstrates key concepts for AWS API interaction and data formatting:

- **Boto3 Client Creation**: The `boto3.client('ec2')` creates a client object that automatically uses the credentials configured earlier with `aws configure`, enabling secure API communication with AWS.
- **API Response Processing**: The `describe_regions()` method returns a structured dictionary with a 'Regions' key containing a list of region objects. Each region object includes properties like 'RegionName' and 'Endpoint'.
- **Data Extraction and Formatting**: The for loop iterates through the response data, extracting specific values from each region dictionary. Python's f-string formatting with alignment specifiers (`:<20`, `:<40`) ensures consistent column alignment by padding strings to fixed widths.
- **Table Presentation**: The script creates a professional-looking table output with headers and a separator line, making the AWS region data easily readable and well-organized.

#### **Result: ** 

I ran the code and got the output like sceenshot showed:

![](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250731012109423.png)     

<div style="page-break-after: always;"></div>

# Lab 2

## Create an EC2 instance using awscli

The first part of this lab involved provisioning a virtual server (EC2 instance) directly from the command line using the AWS CLI. This process was broken down into several sequential steps, from setting up security to launching and connecting to the instance.

### [1] Create a security group

First, I created a security group to act as a virtual firewall for the instance.

#### Command:

To create the security group, named with my student number:

```bash
aws ec2 create-security-group --group-name 24745401-sg --description "security group for development environment"
```

#### **Result:** 

 The screenshot below shows the successful creation of the security group and the returned `GroupId`.

![9bc578cd9ec459d3dfe6577720a2f0b3](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/9bc578cd9ec459d3dfe6577720a2f0b3.png)  

### [2] Authorise inbound traffic for ssh  

Next, I added a rule to the security group to allow inbound SSH traffic on port 22 from any IP address, which is necessary for remote access.

#### Command:

To add the ingress rule:

```bash
aws ec2 authorize-security-group-ingress --group-name 24745401-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
```

#### **Result:** 

The screenshot below confirms that the rule was successfully added to the security group.

![351be5a27c9fa9808ca0177a79029220](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/351be5a27c9fa9808ca0177a79029220.png)  

### [3] Create a key pair

I then generated an SSH key pair, which is required for securely authenticating when connecting to the instance. The private key was saved to a `.pem` file.

#### Command:

To create the key pair and save it:

```bash
aws ec2 create-key-pair --key-name 24745401-key --query 'KeyMaterial' --output text > 24745401-key.pem
```

To ensure the key file has the correct secure permissions, I moved it to the `.ssh` directory and restricted its permissions:

```bash
mkdir -p ~/.ssh
mv 24745401-key.pem ~/.ssh/
chmod 400 ~/.ssh/24745401-key.pem
```

####  **Result:** 

 The screenshot below confirms the key was created and its permissions were set correctly.

![e0b68f873a1999b6b275a8793dd78fbe](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/e0b68f873a1999b6b275a8793dd78fbe.png) 

### [4] Create the instance

With the prerequisites in place, I launched the `t3.micro` EC2 instance using the appropriate AMI for my assigned region (`ap-southeast-2`).

#### Command:

To run the instance:

```bash
aws ec2 run-instances --image-id ami-042b4708b1d05f512 --security-group-ids 24745401-sg --count 1 --instance-type t3.micro --key-name 24745401-key       --query 'Instances[0].InstanceId'
```

#### **Result:** 

The command returned the `InstanceId` for the newly launched instance, as shown in the screenshot.

![1cfd9a90988a0accfb313aaecffe1c17](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/1cfd9a90988a0accfb313aaecffe1c17.png) 

### [5] Add a tag to your Instance

To easily identify the instance in the AWS Console, I added a "Name" tag.

#### Command:

To tag the instance:

```bash
aws ec2 create-tags --resources i-0f04fe75c81599ce2 --tags Key=Name,Value=24745401-vm
```

### [6] Get the public IP address

I retrieved the public IP address of the instance, which is needed to connect to it.

#### Command:

To get the public IP:

```bash
aws ec2 describe-instances --instance-ids i-0f04fe75c81599ce2 --query 'Reservations[0].Instances[0].PublicIpAddress'
```

#### **Result:** 

The command returned the public IP address of the instance.

![c7ea3357682d1ca680a2da5885aa1dbb](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/c7ea3357682d1ca680a2da5885aa1dbb.png)

### [7] Connect to the instance via ssh

Finally, I connected to the running instance using the SSH command.

#### Command:

To connect via SSH:

```bash
ssh -i ~/.ssh/24745401-key.pem ubuntu@13.60.38.246
```

#### **Result:** 

The screenshot shows a successful connection to the Ubuntu shell on the remote EC2 instance.

![52af24705360b4f5090a9271fe2b0978](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/52af24705360b4f5090a9271fe2b0978.png) 



## Create an EC2 instance with Python Boto3

This section involved automating the entire instance creation process using a Python script with the Boto3 library. 

#### Code:

```python
# lab2_createInst.py
import boto3
import os
import time

# --- Configuration from Lab Instructions ---
# You must replace these with your actual details
STUDENT_NUMBER = "24745401" 
AMI_ID = "ami-042b4708b1d05f512" 
INSTANCE_TYPE = "t3.micro"

# Resource names are made unique to avoid conflict with CLI-created resources
KEY_NAME = f"{STUDENT_NUMBER}-key-boto3"
SECURITY_GROUP_NAME = f"{STUDENT_NUMBER}-sg-boto3"
INSTANCE_NAME = f"{STUDENT_NUMBER}-vm-boto3"
PEM_FILE_NAME = f"{KEY_NAME}.pem"

# Initialize Boto3 EC2 client
ec2 = boto3.client('ec2')

try:
    # Create Security Group
    sg_response = ec2.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description="Boto3 security group for lab 2"
    )
    security_group_id = sg_response['GroupId']

    # Authorize SSH Ingress
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )
    
    # Create Key Pair and save it
    key_pair_response = ec2.create_key_pair(KeyName=KEY_NAME)
    with open(PEM_FILE_NAME, "w") as pem_file:
        pem_file.write(key_pair_response['KeyMaterial'])
    os.chmod(PEM_FILE_NAME, 0o400)

    # Launch Instance
    instance_response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SecurityGroupIds=[security_group_id],
        MinCount=1,
        MaxCount=1
    )
    instance_id = instance_response['Instances'][0]['InstanceId']

    # Wait for the instance to be running
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

    # Tag the instance
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': INSTANCE_NAME}]
    )

    # Describe instance to get Public IP
    describe_response = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = describe_response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    print("--- Boto3 Script Finished ---")
    print(f"Instance {instance_id} is running at IP: {public_ip}")
    print(f"Connect with: ssh -i {PEM_FILE_NAME} ubuntu@{public_ip}")

except Exception as e:
    print(f"An error occurred: {e}")
```

#### Explanation:

This script automates the entire EC2 instance creation workflow using Python's Boto3 library:

- **Configuration Management**: The script uses variables at the top to centralize configuration, making resource names unique with the `-boto3` suffix to avoid conflicts with CLI-created resources.
- **Sequential Resource Creation**: The script follows the same logical sequence as the CLI commands - creating security groups, adding ingress rules, generating key pairs, and launching instances.
- **Error Handling**: The entire process is wrapped in a try-except block to catch and display any AWS API errors that might occur during resource creation.
- **Waiter Pattern**: The `waiter = ec2.get_waiter('instance_running')` demonstrates AWS's waiter functionality, which polls the instance state until it reaches the desired running state, avoiding the need for manual sleep delays.
- **File Operations**: The script handles file creation for the private key and sets appropriate permissions using `os.chmod(PEM_FILE_NAME, 0o400)`, replicating the security measures from the CLI approach.

#### **Result:** 

I ran the script in the Vscode successfully and it printed the new instance ID and public IP address. On the AWS EC2 Console I also confirmed that both CLI-created instance (`24745401-vm`) and the Boto3-created instance (`24745401-vm-boto3`) are running.

![b18e0c0f1ae6990f7c3663547bf0374c](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/b18e0c0f1ae6990f7c3663547bf0374c.png) 

![af2eb3d438c45448c9e65d072e4b07f8](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/af2eb3d438c45448c9e65d072e4b07f8.png) 



## Install Docker

The section focused on the containerization with Docker, performd within my local WSL.

#### Command:

To install Docker, start its service, and add my user to the `docker` group to avoid using `sudo`:

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker $USER
```

To verify the installation:

```bash
docker --version
```

#### **Result:** 

The screenshot below confirms that the Docker service was installed and is running correctly.

![8c76d284ab92441763ea2df4b208a4f5](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/8c76d284ab92441763ea2df4b208a4f5.png) 

## Build and run an httpd container

The final task was to build a custom Docker image containing a simple webpage.

First, I created a directory structure like the screenshot below showed:

![image-20250807004541279](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250807004541279.png) 

Then, I edited the `index.html` and `Dockerfile` with the following content:

![image-20250811193545628](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250811193545628.png)  

![image-20250807004628499](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250807004628499.png) 

#### Command:

To build the docker image from the Dockerfile:

```bash
docker build -t my-apache2 .
```

To run the container from the newly built image, mapping port 80:

```bash
docker run -p 80:80 -dit --name my-app my-apache2
```

#### Explanation:

The Docker commands demonstrate containerization concepts:

- **`docker build -t my-apache2 .`**: Builds a Docker image from the Dockerfile in the current directory (`.`). The `-t` flag tags the image with the name `my-apache2` for easy reference.
- **`docker run -p 80:80 -dit --name my-app my-apache2`**: Runs a container from the built image with several important flags:
  - **`-p 80:80`**: Maps port 80 on the host to port 80 in the container, allowing external access to the web server
  - **`-d`**: Runs the container in detached mode (in the background)
  - **`-i`**: Keeps the container's STDIN open for interactive access
  - **`-t`**: Allocates a pseudo-TTY for the container
  - **`--name my-app`**: Assigns a custom name to the container for easier management

#### **Result:** 

The screenshot below shows the successful build and run process. And the browser accessing `http://localhost` displays the "Hello World!" message, confirming the containerized web server is working correctly.

![image-20250913230622554](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250913230622554.png)  

#### Command:

Finally,  I ran the following commands to list all Docker containers, stop and remove specified container:

```bash
docker ps -a
docker stop my-app
docker rm my-app
```

#### **Result:** 

![8611b4b428406c97e8bcb6fae296907c](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/8611b4b428406c97e8bcb6fae296907c.png) 

<div style="page-break-after: always;"></div>

# Lab 3

## Program

This lab focused on building a cloud storage application using AWS S3 for object storage and DynamoDB for metadata management.

### [1] Preparation

The first step was to prepare a local directory structure with sample files to simulate the data that would be backed up to the cloud.

- First, I downloaded the `cloudstroage.py` script from the course repository and placed it in a new lab3 directory within my project folder.

- Next, I used VS Code to create the necessary directory structure. I created `rootdir` and `subdir` as instructed. Then I wrote the required content into the two text files

#### Result:

 The screenshot below shows the final directory structure in VS Code, which is now ready for the upload process. 

![image-20250814151316337](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814151316337.png) 

## [2] Save to S3 by updating `cloudstorage.py`

Next, I modified the provided `cloudstorage.py` script to upload the contents of the `rootdir` to an S3 bucket, preserving the folder hierarchy. 

#### Code:

```python
# cloudstroage.py
import os
import boto3
import base64
import logging
from botocore.exceptions import ClientError

# ------------------------------
# CITS5503
#
# cloudstorage.py
#
# skeleton application to copy local files to S3
#
# Given a root local directory, will return files in each level and
# copy to same path on S3
#
# ------------------------------ 

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
```

#### Explanation:

This script demonstrates cloud storage implementation using AWS S3:

- **Bucket Management**: The script first checks if the target bucket exists using `s3.head_bucket()`. If the bucket doesn't exist (404 error), it creates a new one in the specified region using `CreateBucketConfiguration`.
- **Directory Traversal**: The `os.walk()` function recursively traverses the local directory structure, yielding tuples of (directory path, subdirectory names, file names) for each level.
- **Path Processing**: The script constructs S3 object keys by removing the first two characters from the directory path (`dir_name[2:]`) to eliminate the leading `./` from relative paths, preserving the folder hierarchy in S3.
- **File Upload**: Each file is uploaded using the `upload_file()` function, which handles the actual S3 API call and provides error logging for failed uploads.

#### **Result:**

The script successfully created the S3 bucket and uploaded the files.And The screenshot from the AWS S3 Console confirms that the `rootdir` contents, including the `subdir` folder, have been replicated in the bucket. 

![image-20250814152934606](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814152934606.png) 

![image-20250814151750743](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814151750743.png) 

## [3] Restore from S3

To simulate a data recovery scenario, I created a new script, `restorefromcloud.py`, designed to download all files from the S3 bucket and recreate the original directory structure locally.

#### Code:

```python
# restorefromcloud.py
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
```

#### Explanation:

This restoration script implements a complete data recovery workflow:

- **Object Listing**: The script uses `list_objects_v2()` to retrieve metadata about all objects in the S3 bucket, checking for the 'Contents' key to ensure files exist.
- **Directory Recreation**: For each object, `os.path.dirname()` extracts the directory path, and `os.makedirs()` creates the necessary local directories if they don't exist, preserving the original folder structure.
- **File Download**: The `download_file()` method retrieves each object from S3 and saves it to the local filesystem using the same relative path structure as stored in the bucket.
- **Error Handling**: The script includes specific handling for common scenarios like missing buckets (`NoSuchBucket` error) and provides informative status messages throughout the restoration process.

Before running the script, I deleted the `subfile.txt`  to test the restoration process:

![image-20250814153949077](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814153949077.png) 

Then execute the restore script:

```bash
python3 restorefromcloud.py
```

#### **Result:** 

The script ran successfully. The screenshot of my `lab3` directory shows that the `rootdir` folder and its contents were correctly downloaded and recreated from the S3 bucket. 

![image-20250814155110193](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814155110193.png) 

## [4] Write information about files to DynamoDB

This section involved storing metadata about the S3 files in a NoSQL database.

#### Command:

First, I prepared the local DynamoDB instance. In a new, separate terminal, I created a directory, downloaded the DynamoDB Local package, and extracted it.

```bash
mkdir ~/dynamodb
cd ~/dynamodb
wget https://s3-ap-northeast-1.amazonaws.com/dynamodb-local-tokyo/dynamodb_local_latest.tar.gz
tar -zxvf dynamodb_local_latest.tar.gz
```

With the files extracted, I started the DynamoDB server. This terminal was left running to host the local database. 

```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

![5705c8ae2a8757f1cb75a9f47f5d8f48](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/5705c8ae2a8757f1cb75a9f47f5d8f48.png) 

Next, I wrote a script, `dynamodb_manager.py`, to create a table named `CloudFiles` and populate it with metadata (path, owner, etc.) for each object in my S3 bucket.

#### Code:

```python
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Configuration
STUDENT_ID = '24745401'
REGION = 'eu-north-1'
BUCKET_NAME = f'{STUDENT_ID}-cloudstorage'
TABLE_NAME = 'CloudFiles'

# Boto3 resources
s3 = boto3.resource("s3", region_name=REGION)
bucket = s3.Bucket(BUCKET_NAME)
dynamodb = boto3.resource(
    'dynamodb', 
    region_name=REGION
)

def create_dynamodb_table():
    print(f"Checking for DynamoDB table '{TABLE_NAME}' in AWS cloud...")
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'userId', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'fileName', 'KeyType': 'RANGE'} # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'userId', 'AttributeType': 'S'},
                {'AttributeName': 'fileName', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 
                                   'WriteCapacityUnits': 5}
        )
        # Wait until the table exists.
        table.wait_until_exists()
        print(f"Table '{TABLE_NAME}' created successfully in AWS.")
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{TABLE_NAME}' already exists in AWS.")
            return dynamodb.Table(TABLE_NAME)
        else:
            print(f"Error creating table: {e}")
            raise    


def store_s3_metadata_in_dynamodb(table):
    print(f"\nScanning bucket '{BUCKET_NAME}' for file metadata...")
    try:
        for obj in bucket.objects.all():
            print(f"  -> Processing s3://{BUCKET_NAME}/{obj.key}")
            
            acl = obj.Acl()
            owner = acl.owner.get('DisplayName', acl.owner.get('ID')) 
            # Safely get owner name or ID
            permissions = "rw-r--r--" # Placeholder for permissions
            
            table.put_item(
                Item={
                    'userId': STUDENT_ID,
                    'fileName': os.path.basename(obj.key),
                    'path': obj.key,
                    'lastUpdated': obj.last_modified.strftime("%Y-%m-%d %H:%M:%S"),
                    'owner': owner,
                    'permissions': permissions
                }
            )
        print("\nMetadata successfully stored in DynamoDB.")
    except Exception as e:
        print(f"An error occurred while processing S3 objects: {e}")


if __name__ == "__main__":
    cloudfiles_table = create_dynamodb_table()
    if cloudfiles_table:
        store_s3_metadata_in_dynamodb(cloudfiles_table)
        print("done")
```

#### Explanation:

This script demonstrates NoSQL database operations with DynamoDB:

- **Table Schema Design**: The table uses a composite primary key with `userId` as the partition key and `fileName` as the sort key, enabling efficient queries by user and file combinations.
- **Resource vs Client**: The script uses `boto3.resource()` for higher-level object-oriented access to DynamoDB and S3, providing more intuitive methods like `bucket.objects.all()` compared to the lower-level client interface.
- **Metadata Extraction**: For each S3 object, the script retrieves metadata including the ACL owner information, last modified timestamp, and file path, storing this information as structured data in DynamoDB.
- **Error Handling**: The script handles the `ResourceInUseException` which occurs when attempting to create an already-existing table, allowing for script reusability.

#### **Result:** 

The screenshot of the terminal output shows the script successfully connecting to the local DynamoDB, creating the table, and processing the metadata for the two files from the S3 bucket. 

![image-20250814160741223](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814160741223.png) 

## [5] Scan the table

To verify that the data was written correctly, I used the AWS CLI to scan all items in the local `CloudFiles` table.

To scan the table:

```bash
aws dynamodb scan --table-name CloudFiles 
```

#### **Result:** 

The screenshot below shows the JSON output from the command, displaying the two items and their attributes as stored in the local DynamoDB table.

![image-20250814160941607](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814160941607.png) 

![image-20250814161011552](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814161011552.png)  

## [6] Delete the table

As the final cleanup step, I deleted the local DynamoDB table.

To delete the table:

```bash
aws dynamodb delete-table --table-name CloudFiles 
```

#### **Result:** 

The command returned a JSON description of the table being deleted. A subsequent `list-tables` command confirmed that the table was successfully removed. 

![image-20250814161359651](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814161359651.png) 

![image-20250814161419879](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250814161419879.png) 



<div style="page-break-after: always;"></div>

# Lab 4

## Apply a policy to restrict permissions on the bucket

### [1] Write a Python script

First, I wrote a Python script to apply a security policy to my S3 bucket.

#### Code:

```python
import boto3
import json
from botocore.exceptions import ClientError

# --- Configuration ---
BUCKET_NAME = "24745401-lab4-bucket"
STUDENT_NUMBER = "24745401"
# The folder within bucket needed to protect
FOLDER_NAME = "rootdir"

# Initialize Boto3 S3 client
s3 = boto3.client('s3')

# Define the bucket policy 
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "AllowS3ActionsInUserFolderForUserOnly",
        "Effect": "DENY",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": f"arn:aws:s3:::{BUCKET_NAME}/{FOLDER_NAME}/*",
        "Condition": {
            "StringNotLike": {
                "aws:username": f"{STUDENT_NUMBER}@student.uwa.edu.au"
            }
        }
    }]
}

# --- Main Execution ---
try:
    # 1. Explicitly check if the bucket exists
    print(f"Verifying bucket '{BUCKET_NAME}' exists...")
    s3.head_bucket(Bucket=BUCKET_NAME)
    print("Bucket found.")

    # 2. Convert the policy to a JSON string and apply it
    policy_string = json.dumps(bucket_policy)
    
    print("Applying security policy...")
    s3.put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=policy_string
    )
    print(f"Successfully applied policy to bucket '{BUCKET_NAME}'.")

except ClientError as e:
    # Handle specific errors
    if e.response['Error']['Code'] == '404':
        print(f"Error: Bucket '{BUCKET_NAME}' does not exist.")
    else:
        print(f"An unexpected error occurred: {e}")
```

#### Explanation:

This script demonstrates S3 bucket security through policy-based access control:

- **Policy Structure**: The bucket policy follows AWS IAM policy syntax with `Version`, `Statement`, `Effect`, `Principal`, and `Condition` elements. The `DENY` effect blocks all S3 actions (`s3:*`) for the specified resource.
- **Resource Targeting**: The `Resource` field uses ARN format (`arn:aws:s3:::bucket-name/folder/*`) to specifically target objects within the protected folder, ensuring the policy only affects the intended directory.
- **Conditional Access**: The `StringNotLike` condition with `aws:username` creates an exclusion rule, allowing only the specified user to bypass the deny policy while blocking all other principals.
- **JSON Serialization**: The `json.dumps()` function converts the Python dictionary to a JSON string format required by the AWS API, ensuring proper policy syntax.

### [2] Check whether the script works

To check if the policy worked, I used the AWS CLI to view the attached policy. Then, I tested my access by downloading a file from the protected folder.

#### Command:

```bash
# Command to view the attached policy
aws s3api get-bucket-policy --bucket 24745401-lab4-bucket

# Command to test other user's access
aws s3 cp s3://24745401-lab4-bucket/rootdir/rootfile.txt .
```

#### **Result:**

The CLI commands confirmed the policy was in place. Any other user would be denied access.

![image-20250828110757381](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250828110757381.png) 

![image-20250913225826104](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250913225826104.png) 

## AES Encryption using KMS

### [1] Create a KMS key

I wrote a script to create a new KMS key and gave it a unique alias using my student number. 

#### Code:

```python
import boto3
from botocore.exceptions import ClientError

STUDENT_NUMBER = "24745401"
KEY_ALIAS = f"alias/{STUDENT_NUMBER}"
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

if __name__ == "__main__":
    create_kms_key()
```

#### Explanation:

This script creates and configures AWS KMS encryption keys for secure data protection:

- **Key Creation**: The `create_key()` method generates a new customer-managed KMS key with `ENCRYPT_DECRYPT` usage, providing full control over the key lifecycle compared to AWS-managed keys.
- **Alias Management**: Creating an alias with `create_alias()` provides a human-readable reference to the key, making it easier to reference in applications without remembering the complex key ID.
- **Error Handling**: The `AlreadyExistsException` handling prevents script failures on re-runs, demonstrating idempotent design patterns essential for automation scripts.
- **Key Identification**: The function returns the key ID for use by subsequent operations, enabling modular script design where key creation and policy attachment are separate concerns.

### [2] Attach a policy to the created KMS key

Next, I updated the script to attach a policy to the key. This policy makes my IAM user the administrator and user of the key. 

#### Code:

```python
import boto3
import json
from botocore.exceptions import ClientError

# --- Configuration ---
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
                "Principal": {"AWS": 	 
                           f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"},
                "Action": [
                    "kms:Create*", "kms:Describe*", "kms:Enable*", 
                    "kms:List*", "kms:Put*","kms:Update*", "kms:Revoke*", 
                    "kms:Disable*", "kms:Get*", "kms:Delete*",
                    "kms:TagResource", "kms:UntagResource", 
                    "kms:ScheduleKeyDeletion", "kms:CancelKeyDeletion"
                ],
                "Resource": "*"
            },
            {
                "Sid": "Allow use of the key",
                "Effect": "Allow",
                "Principal": {"AWS": 
                           f"arn:aws:iam::489389878001:user/{IAM_USERNAME}"},
                "Action": ["kms:Encrypt", "kms:Decrypt", "kms:ReEncrypt*", 
                           "kms:GenerateDataKey*", "kms:DescribeKey"],
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
```

#### Explanation:

This script applies security policies to KMS keys for fine-grained access control:

- **Multi-Statement Policy**: The policy contains three distinct statements - root permissions, administrative permissions, and usage permissions - following the principle of least privilege by granting specific permissions to specific principals.
- **Principal Specification**: Using ARN format (`arn:aws:iam::account:user/username`) ensures precise identification of the authorized user, preventing accidental access grants to similarly named users in other accounts.
- **Administrative vs Usage Permissions**: The separation between administrative actions (`Create*`, `Delete*`, `Disable*`) and usage actions (`Encrypt`, `Decrypt`, `GenerateDataKey*`) allows for role-based access control.
- **Policy Application**: The `put_key_policy()` method with `PolicyName='default'` replaces the existing key policy, ensuring consistent security posture across key management operations.

#### **Result:**

The script successfully created a new KMS key and attached the policy to it.

![image-20250828111355099](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250828111355099.png) 

### [3] Check whether the script works

I checked the AWS KMS Console to verify the key was created. I found the key using its alias and confirmed the correct policy was attached.

### **Result:**

The key policy tab in the KMS console showed the correct JSON policy, with my user ARN listed as an administrator and user.

![image-20250828111509957](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250828111509957.png) 

![image-20250828111517427](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250828111517427.png) 

### [4] Use the created KMS key for encryption/decryption

To use the key, I wrote a script that encrypted and then decrypted the files in my S3 bucket using the KMS service. 

#### Code:

```python
import boto3
from botocore.exceptions import ClientError
import os

# --- Configuration ---
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
            if file_key.endswith('.encrypted') or 
            	file_key.endswith('.decrypted'):
                continue

            print(f"\n--- Processing file: {file_key} ---")
            local_path = os.path.join(DOWNLOAD_DIR, 
                                      os.path.basename(file_key))

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
            s3.put_object(Bucket=BUCKET_NAME, Key=encrypted_key, 
                          Body=ciphertext_blob)

            # 4. Decrypt the file content using KMS
            print("Decrypting with KMS...")
            decrypt_response = kms.decrypt(
                CiphertextBlob=ciphertext_blob
            )
            decrypted_plaintext = decrypt_response['Plaintext']

            # 5. Upload the decrypted file to S3 to verify
            decrypted_key = f"{file_key}.decrypted"
            print(f"Uploading decrypted file to {decrypted_key}...")
            s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_key, 
                          Body=decrypted_plaintext)

            print(f"Successfully completed cycle for {file_key}.")

    except ClientError as e:
        print(f"An error occurred: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    encrypt_decrypt_cycle()
```

#### Explanation:

This script demonstrates KMS-based encryption and decryption workflows:

- **Managed Encryption**: KMS handles all cryptographic operations server-side, eliminating the need for local key management and ensuring encryption keys never leave the AWS environment.
- **Ciphertext Blob Handling**: The `encrypt()` method returns a `CiphertextBlob` containing both encrypted data and metadata, which KMS uses to identify the correct key during decryption without requiring explicit key specification.
- **S3 Integration**: The workflow of download → encrypt → upload → download → decrypt → upload demonstrates a complete cloud-based encryption cycle, showing how KMS integrates with other AWS services.
- **Key Reference**: Using the key alias instead of the key ID in encrypt operations provides flexibility - if the alias is updated to point to a different key, the application continues working without code changes.

#### **Result:**

The script created new `.encrypted` and `.decrypted` versions of each original file in the S3 bucket.

![image-20250828111838732](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250828111838732.png) 

![image-20250828111908807](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250828111908807.png) 

### [5] Apply `pycryptodome` for encryption/decryption

For comparison, I used the `pycryptodome` library to process the encryption and decryption. This time, the encryption happened locally on my machine. 

To use the library, I ran the `pip3` command to install the package:

```bash
pip3 install pycryptodome
```

Then, I edited the following script which handles the local encryption and decryption:

#### Code:

```python
import boto3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# --- Configuration ---
STUDENT_NUMBER = "24745401"
BUCKET_NAME = f"{STUDENT_NUMBER}-lab4-bucket"
PASSWORD = "my-secret-password" 
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
            original_object = s3.get_object(Bucket=BUCKET_NAME, 
                                            Key=file_key)
            plaintext = original_object['Body'].read()

            # Encrypt using the dedicated function
            encrypted_blob = encrypt(plaintext, PASSWORD)
            
            # Upload encrypted file
            encrypted_key = f"{file_key}.localencrypted"
            s3.put_object(Bucket=BUCKET_NAME, Key=encrypted_key, 
                          Body=encrypted_blob)
            print(f"Uploaded encrypted file to {encrypted_key}")

            # Download encrypted file for decryption
            encrypted_object_from_s3 = s3.get_object(Bucket=BUCKET_NAME, 
                                                     Key=encrypted_key)
            encrypted_data_from_s3 = 
            encrypted_object_from_s3['Body'].read()

            # Decrypt using the dedicated function
            decrypted_text = decrypt(encrypted_data_from_s3, PASSWORD)

            # Upload decrypted file for verification
            decrypted_key = f"{file_key}.localdecrypted"
            s3.put_object(Bucket=BUCKET_NAME, Key=decrypted_key, 
                          Body=decrypted_text)
            print(f"Uploaded decrypted file to {decrypted_key}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    local_encrypt_decrypt_cycle()
```

#### Explanation:

This script implements local encryption using the pycryptodome library:

- **Key Derivation**: PBKDF2 (Password-Based Key Derivation Function 2) with 1,000,000 iterations and a random salt creates a strong encryption key from a password, making brute-force attacks computationally expensive.
- **AES CBC Mode**: The Advanced Encryption Standard in Cipher Block Chaining mode provides secure symmetric encryption, with each block depending on the previous block, preventing pattern recognition in encrypted data.
- **Initialization Vector (IV)**: Each encryption operation generates a random IV, ensuring that identical plaintext produces different ciphertext each time, preventing cryptographic attacks based on pattern analysis.
- **Padding Management**: The manual padding with null bytes (`\0`) and subsequent stripping ensures plaintext fits AES block size requirements (16 bytes), while the `rstrip()` operation safely removes padding during decryption.
- **Data Structure**: Concatenating salt, IV, and ciphertext into a single blob creates a self-contained encrypted package that includes all information needed for decryption, simplifying storage and transmission.

#### **Result:**

This script also ran successfully, creating new `.localencrypted` and `.localdecrypted` files in the S3 bucket.

![image-20250829203250755](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250829203250755.png) 

![image-20250829203321980](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250829203321980.png) 



## Answer the following question 

### *What* is the performance difference between using KMS and using the custom *solution?*

The **local `pycryptodome` solution is faster** for raw cryptographic operations.

This performance difference is almost entirely due to **network latency**. The KMS solution requires a network API call to an AWS service for every encryption and decryption request, which adds overhead. In contrast, the `pycryptodome` solution performs these operations using the local machine's CPU, which is much faster.

However, the choice involves a trade-off: the raw speed of local encryption versus the superior **security, management, and auditing capabilities** of a managed service like AWS KMS.

<div style="page-break-after: always;"></div

# Lab 5

This lab focused on cloud networking principles, specifically the configuration of an Application Load Balancer (ALB) to distribute traffic across multiple EC2 instances for high availability and scalability.

## Application Load Balancer

### [1] Create 2 EC2 instances

Unlike previous labs where I just wrote the relevant functions and code, this time, considering the reusability of the code, I first integrated some EC2-related functions into a single module, `ec2_manager.py`, located in the `utils` directory. The code is shown below:

#### Code:

```python
# ec2_manager.py
# A reusable module with generic functions for managing EC2 resources.

import boto3
from botocore.exceptions import ClientError
import os
from . import config 

# Initialize the client using the region from our config file
ec2 = boto3.client('ec2', region_name=config.REGION_NAME)

def create_key_pair(key_name):
    """Creates an EC2 key pair if it doesn't exist and saves the .pem file."""
    pem_file_path = f"{key_name}.pem"
    if os.path.exists(pem_file_path):
        print(f"Existed key pair: {pem_file_path}")
        return
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        with open(pem_file_path, "w") as f:
            f.write(key_pair['KeyMaterial'])
        os.chmod(pem_file_path, 0o400)
        print(f"Created and saved key pair: {pem_file_path}")
    except ClientError as e:
        if e.response['Error']['Code'] != 'InvalidKeyPair.Duplicate':
            raise

def create_security_group(sg_name, description, rules):
    """Creates a security group with specified inbound rules."""
    try:
        sg_response = ec2.create_security_group(
            GroupName=sg_name, 
            Description=description
        )
        group_id = sg_response['GroupId']
        
        # Authorize SSH Ingress
        ec2.authorize_security_group_ingress(
            GroupId=group_id, 
            IpPermissions=rules
        )
        print(f"Created security group '{sg_name}' with ID: {group_id}")
        return group_id
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
            response = ec2.describe_security_groups(GroupNames=[sg_name])
            group_id = response['SecurityGroups'][0]['GroupId']
            print(f"Existed security group '{sg_name}' with ID: {group_id}")
            return group_id
        else:
            raise

def setup_instance(name,ami_id, instance_type, key_name, sg_id, az):
    """
    Ensures an instance with a specific name is running in a specific AZ.
    """
    # This filter checks for BOTH name and availability zone.
    filters = [
        {'Name': 'tag:Name', 'Values': [name]},
        {'Name': 'availability-zone', 'Values': [az]}
    ]
    response = ec2.describe_instances(Filters=filters)

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']
            instance_id = instance['InstanceId']

            if state in ['running', 'pending']:
                print(f"Existed Instance '{name}' is {state}.")
                return instance_id
            elif state == 'stopped':
                print(f"Existed Instance '{name}' is {state}. Starting it...")
                ec2.start_instances(InstanceIds=[instance_id])
                return instance_id
            
    print(f"Launch request sent for {name} in {az}.")
    return _launch_instance(name, ami_id, instance_type, key_name, sg_id, az)

def _launch_instance(name, ami_id, instance_type, key_name, sg_id, az):
    """Launches a single, tagged EC2 instance."""
    response = ec2.run_instances(
        ImageId=ami_id, 
        InstanceType=instance_type, 
        KeyName=key_name,
        SecurityGroupIds=[sg_id], 
        Placement={'AvailabilityZone': az},
        MinCount=1, MaxCount=1,
        TagSpecifications=[
            {'ResourceType': 'instance', 
             'Tags': [{'Key': 'Name', 'Value': name}]}
        ]
    )
    return response['Instances'][0]['InstanceId']

def get_instance_ip(instance_id):
    """Waits for an instance and returns its public IP."""
    waiter = ec2.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[instance_id])
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')

def get_availability_zones():
    """Returns a list of availability zone names in the configured region."""
    response = ec2.describe_availability_zones()
    return [az['ZoneName'] for az in response['AvailabilityZones']]


    """Finds running or pending instances that match a list of 'Name' tags."""
    if not instance_names: return {}
    
    instances_found = {}
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': instance_names},
            {'Name': 'instance-state-name', 'Values': ['running', 'pending']}
        ]
    )
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_name = [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0]
            instances_found[instance_name] = instance['InstanceId']
    return instances_found

def get_all_subnet_ids():
    """Returns a list of all subnet IDs in the default VPC."""
    response = ec2.describe_subnets()
    return [subnet['SubnetId'] for subnet in response['Subnets']]
```

#### **Explanation:** 

This module provides reusable functions for EC2 instance management:

- **Idempotent Design**: The `setup_instance()` function implements check-first logic, querying existing instances by name tag and availability zone before creating new resources, preventing duplicate resource errors on script re-runs.
- **State Management**: The function handles different instance states (`running`, `pending`, `stopped`) appropriately, reusing running instances, waiting for pending ones, and restarting stopped instances to achieve the desired state.
- **Resource Distribution**: Using modulo operation (`zones[i % len(zones)]`) distributes instances across multiple availability zones, ensuring high availability and fault tolerance in the deployment architecture.
- **Configuration Separation**: Centralizing configuration in a separate module (`config.py`) follows software engineering best practices, making the code maintainable and allowing easy modification of deployment parameters.

Next, to make the code more organized and easier to manage, I created a central configuration file and wrote the main script which uses the `ec2_manager.py` module to perform the actual instance creation.

#### Code:

```python
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

```

```python
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
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': 
             [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': 
             [{'CidrIp': '0.0.0.0/0'}]}
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
        

    except ClientError as e:
        print(f"\nAn AWS error occurred: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

```

#### **Explanation:**

This main script sets up the EC2 instances by calling functions from the `ec2_manager` module. Its key features are:

- **Modular Design**: The script calls functions from the `ec2_manager` module to handle complex tasks. This keeps the main script's logic clean and easy to follow.
- **Logical Order**: It follows a sensible creation order: preparing the key pair and security group first, then launching the instances, which ensures a stable setup process.
- **High Availability**: The script uses a modulo operator (`zones[i % len(zones)]`) to automatically distribute the instances across different Availability Zones. This is a simple but effective way to prevent a single point of failure.
- **Separated Configuration**: Key settings like instance type and key name are loaded from the `config.py` file. This allows for easy updates to the configuration without changing the main script's code.

#### Result:

The script successfully created both EC2 instances in different Availability Zones and outputted their public IP addresses and the necessary SSH commands for connection.

![image-20250904033655569](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904033655569.png) 

![image-20250904033736431](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904033736431.png) 

### [2] Create an Application Load Balancer

With the EC2 instances prepared, the next step was to create an Application Load Balancer (ALB) to distribute traffic between them. Following the modular approach, I created a new module, `utils/elb_manager.py`, to handle all load balancer-related tasks.

#### Code:

```python
# utils/elb_manager.py
# A reusable module for managing Application Load Balancers.

import boto3
from botocore.exceptions import ClientError
from . import config

elbv2 = boto3.client('elbv2', region_name=config.REGION_NAME)
ec2 = boto3.client('ec2', region_name=config.REGION_NAME)

def setup_load_balancer(alb_name, security_group_id, subnet_ids, instance_ids):
    """
    Ensures a complete ALB setup exists, creating components as needed.
    """
    # 1. Ensure Load Balancer exists
    alb_arn, alb_dns_name = _create_load_balancer(alb_name, security_group_id, subnet_ids)
    
    # 2. Ensure Target Group exists
    tg_name = f"{alb_name}-tg"
    target_group_arn = _create_target_group(tg_name)
    
    # 3. Register targets 
    print("Registering instances with Target Group...")
    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[{'Id': instance_id} for instance_id in instance_ids]
    )
    
    # 4. Ensure Listener exists
    _create_listener(alb_arn, target_group_arn)
    
    return alb_dns_name

def _create_load_balancer(alb_name, security_group_id, subnet_ids):
    """Creates a new Application Load Balancer."""
    try:
        vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
        lb_response = elbv2.create_load_balancer(
            Name=alb_name, Subnets=subnet_ids, SecurityGroups=[security_group_id],
            Scheme='internet-facing', Type='application'
        )
        alb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
        alb_dns = lb_response['LoadBalancers'][0]['DNSName']
        print(f"Created Load Balancer '{alb_name}'.")
        return alb_arn, alb_dns
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateLoadBalancerName':
            response = elbv2.describe_load_balancers(Names=[alb_name])
            alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
            alb_dns = response['LoadBalancers'][0]['DNSName']
            print(f"Existed Load Balancer '{alb_name}'.")
            return alb_arn, alb_dns
        else:
            raise

def _create_target_group(tg_name):
    """Creates a new Target Group."""
    try:
        vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
        tg_response = elbv2.create_target_group(
            Name=tg_name, Protocol='HTTP', Port=80, VpcId=vpc_id,
            HealthCheckProtocol='HTTP', HealthCheckPath='/',
            TargetType='instance'
        )
        tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
        print(f"Created Target Group '{tg_name}'.")
        return tg_arn
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateTargetGroupName':
            response = elbv2.describe_target_groups(Names=[tg_name])
            tg_arn = response['TargetGroups'][0]['TargetGroupArn']
            print(f"Existed Target Group '{tg_name}'.")
            return tg_arn
        else:
            raise

def _create_listener(alb_arn, tg_arn):
    """Creates a Listener for the ALB."""
    try:
        elbv2.create_listener(
            LoadBalancerArn=alb_arn, Protocol='HTTP', Port=80,
            DefaultActions=[{'Type': 'forward', 'TargetGroupArn': tg_arn}]
        )
        print("Created Listener for the Load Balancer.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateListener':
            print("Existed Listener for the Load Balancer.")
        else:
            raise


```

#### **Explanation:**

This module handles Application Load Balancer creation and configuration:

- **Component Coordination**: The `setup_load_balancer()` function manages the creation sequence of ALB components (load balancer → target group → instance registration → listener), ensuring proper dependency relationships.
- **Subnet Requirements**: The function requires multiple subnet IDs because ALBs must span at least two availability zones for high availability, demonstrating AWS's built-in redundancy requirements.
- **Target Group Health Checks**: The target group configuration includes HTTP health checks on port 80 with path `/`, allowing the ALB to automatically route traffic only to healthy instances.
- **Listener Configuration**: Creating a listener with `Type: forward` action establishes the traffic routing rule that directs incoming HTTP requests to the registered EC2 instances in the target group.

Finally, the main script, `lab5_main.py`, was updated to call the `setup_load_balancer` function after the instances are confirmed to be running.

#### Code:

```python
# lab5_main.py (ALB Creation Part)

from utils import elb_manager

# ... (previous code for EC2 setup) ...
        
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

```

#### Explanation:

After the EC2 instances are ready, this part of the script creates and configures the Application Load Balancer (ALB).

- **Network Preparation and Checks**: Before creating the load balancer, the script gets all available subnet IDs and confirms there are at least two. This check enforces AWS's high-availability requirement from the start and prevents common setup errors.
- **Resource Integration**: The script passes the complex job of creating the ALB to the `elb_manager` module. It provides all the necessary, previously created resources—like the security group ID, instance IDs, and subnet IDs—to the module's function, ensuring all components are correctly linked together.

#### **Result:**

The script successfully created the Application Load Balancer and all its related components, outputting the public DNS name required for testing.

![image-20250904041531970](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904041531970.png) 

![image-20250904041650283](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904041650283.png) 



### [3] Test the Application Load Balancer

With the infrastructure deployed, the final step was to configure the EC2 instances and test the load balancer. This involved installing a web server on each instance and customizing their homepages to verify that the ALB was distributing traffic correctly.

#### Command:

- I opened two separate terminal sessions and connected to the two instances using `ssh`

  ```bash
  ssh -i 24745401-key-lab5.pem ubuntu@51.20.131.174
  ssh -i 24745401-key-lab5.pem ubuntu@13.60.74.9
  ```

- In each terminal, I ran the following commands to install the Apache2 web server:

  ```bash
  sudo apt-get update
  sudo apt install apache2 -y
  ```

To visually confirm which server was handling a request, I overwrote the default `index.html` file on each instance with a unique message.

- On `24745401-vm1`:

  ```bash
  echo "<h1>Hello from 24745401-vm1</h1>" | sudo tee /var/www/html/index.html
  ```

- On `24745401-vm2`:

  ```bash
  echo "<h1>Hello from 24745401-vm2</h1>" | sudo tee /var/www/html/index.html
  ```

#### **Explanation:** 

This command line is a powerful combination of three tools:

- **`echo "..."`**: This simply prints the specified string (`<h1>...</h1>`) to standard output.
- **`|` (Pipe)**: This is a core Linux concept that redirects the standard output of the command on its left (`echo`) to be used as the standard input for the command on its right (`sudo tee`).
- **`sudo tee ...`**: The `tee` command reads from standard input and writes it to both standard output (the screen) and one or more files. It is used here with `sudo` because the target file `/var/www/html/index.html` is owned by the `root` user and requires elevated permissions to modify, which a standard output redirection (`>`) would not have.



After configuring the servers, I performed two tests. First, I navigated directly to the public IP address of each instance in my browser to confirm their individual web servers were functioning. Next, I navigated to the public DNS name of the Application Load Balancer and refreshed the page several times to observe the traffic distribution.

#### Result:

The direct access tests were successful; each instance's IP address correctly returned its unique "Hello from..." message:

![image-20250904043838656](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904043838656.png) ![image-20250904043903658](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904043903658.png)  

The test of the Application Load Balancer also succeeded. Upon refreshing the browser, the content switched between "Hello from 24745401-vm1" and "Hello from 24745401-vm2". This confirmed that the load balancer was healthy and was successfully distributing traffic across both instances as intended.

![image-20250904044008882](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904044008882.png) ![image-20250904044029375](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250904044029375.png) 
