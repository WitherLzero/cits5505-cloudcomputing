

<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;">


  <h2>Labs 6-9</h2>

  <p>Student ID: 24745401</p>
  <p>Student Name: Xinqi Lin</p>

</div>

# Lab 6

## Set up an EC2 instance

### [1] Create an EC2 micro instance with Ubuntu and SSH into it. 

First, I reused my `ec2_manager.py` module created in lab5 to create an EC2 micro instance. The logic is shown below: 

#### Code:

```python
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

    except ClientError as e:
        print(f"\nAn AWS error occurred: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
```

After the script ran successfully and outputted the `ssh` command to connect my newly created EC2 instance, I copied the following command in the bash:

```bash
ssh -i 24745401-key-lab6.pem ubuntu@MY-EC2-IPADDRESS
```

### [2] Install the Python 3 virtual environment package. 

After connecting to the lab6 EC2 instance with `ssh` , I ran the commands below to install the Python3 virtual environment package:

#### Command:

To make it convenient, I operated the bash as sudo: 

```bash
sudo bash
```

Then installed the package:

```bash
apt-get update
apt-get upgrade
apt-get install python3-venv
```

### [3] Access a directory 

Next, I created the required directory structure as specified in the lab instructions. I needed to create a directory with the path `/opt/wwc/mysites` and navigate into it.

#### Command:

```bash
mkdir -p /opt/wwc/mysites
cd /opt/wwc/mysites
```

### [4] Set up a virtual environment

With the directory structure in place, I proceeded to set up a Python virtual environment to isolate the Django project dependencies from the system Python installation.

#### Command:

```bash
python3 -m venv myvenv		
```

#### Explanation:

This command demonstrates Python's modular execution approach:

- **`-m venv`**: The `-m` flag tells Python to run a library module as a script. In this case, it runs the built-in `venv` module, which is Python's standard tool for creating virtual environments
- **`myvenv`**: Specifies the name of the directory where the virtual environment will be created

#### Result:

The virtual environment was successfully created, as evidenced by the appearance of the `myvenv` directory containing the virtual environment files.

![image-20250922082138231](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922082138231.png) 

### [5] Activate the virtual environment

To begin working within the isolated Python environment, I activated the virtual environment and installed the necessary packages.

#### Command:

```bash
source myvenv/bin/activate
pip install django
django-admin startproject lab
cd lab
python3 manage.py startapp polls
```

#### Explanation:

These commands perform several critical setup tasks:

- **`source myvenv/bin/activate`**: Activates the virtual environment, modifying the shell's PATH to use the virtual environment's Python interpreter and pip
- **`django-admin startproject lab`**: Creates a new Django project with the directory structure and configuration files
- **`python3 manage.py startapp polls`**: Creates a new Django application named "polls" within the project

#### Result:

The Django project structure was successfully created with the necessary files and directories for both the main project and the polls application.

![image-20250922082435101](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922082435101.png) 

![image-20250922082446892](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922082446892.png) 

### [6] Install nginx

The next step was to install nginx, which will serve as a reverse proxy server to forward HTTP requests from port 80 to the Django development server running on port 8000.

#### Command:

```bash
apt install nginx
```

### [7] Configure nginx

To enable nginx to proxy requests to the Django application, I needed to modify the default nginx configuration file.

#### Command:

I edited the nginx configuration file using nano:

```bash
nano /etc/nginx/sites-enabled/default
```

I replaced the entire contents with:

```nginx
server {
  listen 80 default_server;
  listen [::]:80 default_server;

  location / {
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Real-IP $remote_addr;

    proxy_pass http://127.0.0.1:8000;
  }
}
```

#### Explanation:

This nginx configuration creates a reverse proxy setup:

- `listen 80 default_server`: Configures nginx to listen on port 80 for HTTP requests
- `proxy_set_header X-Forwarded-Host $host`: Preserves the original host header for the backend application
- `proxy_set_header X-Real-IP $remote_addr`: Forwards the client's real IP address to Django
- `proxy_pass http://127.0.0.1:8000`: Routes all requests to the Django development server on localhost port 8000

### [8] Restart nginx

After modifying the configuration, I restarted the nginx service to apply the changes.

#### Command:

```bash
service nginx restart
```

### [9] Access the EC2 instance

With the nginx configuration in place, I started the Django development server to test the complete setup.

#### Command:

In the Django project directory (`/opt/wwc/mysites/lab`), I ran:

```bash
python3 manage.py runserver 8000
```

Then I opened a browser and navigated to the IP address of my EC2 instance.

#### Result:

The browser successfully displayed the default Django welcome page, confirming that the nginx proxy configuration was working correctly and that requests were being forwarded to the Django development server.

![image-20250922083152234](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922083152234.png) 



## Set up Django inside the created EC2 instance

### [1] Edit the following files (create them if not exist)

I needed to create and edit several Python files to establish the URL routing and view logic for the Django application. I edited these files directly on the EC2 instance using the nano text editor.

#### Command:

I used `nano` to edit polls application's view file, its URL configuration and the main project's URL configuration:

```bash
nano /opt/wwc/mysites/lab/polls/views.py
nano /opt/wwc/mysites/lab/polls/urls.py
nano /opt/wwc/mysites/lab/lab/urls.py
```

And I replaced the contents with:

#### Code:

```python
# polls/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```

```python
# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

```python
# lab/urls.py
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

#### Explanation:

This implementation demonstrates Django's URL routing architecture:

- **views.py**: Contains the view functions that handle HTTP requests and return responses. The `index` function processes incoming requests and returns an HttpResponse object containing "Hello, world."
- **polls/urls.py**: Defines URL patterns specific to the polls application. The `path('', views.index, name='index')` maps the root path of the polls app to the index view function
- **lab/urls.py**: The main project URL configuration that includes the polls URLs under the '/polls/' path. The `include('polls.urls')` function delegates URL resolution to the polls application's URL configuration
- **URL Resolution Process**: When a request comes to '/polls/', Django first matches it in the main urls.py file, then forwards the remaining URL path to polls.urls for further processing

### [2] Run the web server again

After updating the Django files in the EC2 instance, I restarted the Django development server to load the new configuration.

#### Command:

```bash
python3 manage.py runserver 8000
```

### [3] Access the EC2 instance

With the Django server running and the URL configurations in place, I tested the application by accessing the polls endpoint. I navigated to the URL:`http://MY-EC2-IPADDRESS/polls/` in my browser.

#### Result:

The browser successfully displayed "Hello, world." 

![image-20250922084633027](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922084633027.png)  



## Set up an ALB

### [1] Create an application load balancer

I extended my existing Lab 6 main script to include ALB creation functionality, utilizing the reusable ELB manager module developed in Lab 5 with specific modifications for this lab's health check requirements.

#### Code:

```python
# extended lab6_main.py
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
```

#### Explanation:

This implementation demonstrates several key Application Load Balancer concepts:

- **Subnet Distribution**: The ALB requires at least two subnets across different Availability Zones to ensure high availability and fault tolerance
- **Target Group Configuration**: The target group acts as a logical grouping of targets that receive traffic from the load balancer, with health checks configured to monitor target health
- **Health Check Customization**: The `health_check_path='/polls/'` parameter ensures the ALB checks the specific endpoint that contains our Django application, rather than the default root path
- **Listener Configuration**: The listener checks for connection requests on port 80 and forwards them to registered targets in the target group
- **Security Group Integration**: The same security group used for the EC2 instance is applied to the ALB, allowing HTTP traffic on port 80

### [2] Health check

The health check configuration required modifications to the existing ELB manager module to support custom health check paths and intervals specific to Lab 6 requirements.

#### Code:

I updated the `elb_manager.py` module to support custom health check configurations:

```python
# modified setup_load_balancer function
def setup_load_balancer(alb_name, security_group_id, subnet_ids, instance_ids, health_check_path='/'):
    """
    Ensures a complete ALB setup exists, creating components as needed.
    """
    # 1. Ensure Load Balancer exists
    alb_arn, alb_dns_name = _create_load_balancer(alb_name, security_group_id, subnet_ids)
    
    # 2. Ensure Target Group exists
    tg_name = f"{alb_name}-tg"
    target_group_arn = _create_target_group(tg_name, health_check_path)
    
    # 3. Register targets 
    print("Registering instances with Target Group...")
    elbv2.register_targets(
        TargetGroupArn=target_group_arn,
        Targets=[{'Id': instance_id} for instance_id in instance_ids]
    )
    
    # 4. Ensure Listener exists
    _create_listener(alb_arn, target_group_arn)
    
    return alb_dns_name
```

```python
# modified _create_target_group function
def _create_target_group(tg_name, health_check_path='/'):
    """Creates a new Target Group with custom health check path."""
    try:
        vpc_id = ec2.describe_vpcs()['Vpcs'][0]['VpcId']
        tg_response = elbv2.create_target_group(
            Name=tg_name, Protocol='HTTP', Port=80, VpcId=vpc_id,
            HealthCheckProtocol='HTTP', HealthCheckPath=health_check_path,
            HealthCheckIntervalSeconds=30,  # Check every 30 seconds as per 											  worksheet
            TargetType='instance'
        )
        tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
        print(f"Created Target Group '{tg_name}' with health check path '{health_check_path}'.")
        return tg_arn
    except ClientError as e:
        if e.response['Error']['Code'] == 'DuplicateTargetGroupName':
            response = elbv2.describe_target_groups(Names=[tg_name])
            tg_arn = response['TargetGroups'][0]['TargetGroupArn']
            print(f"Existed Target Group '{tg_name}'.")
            return tg_arn
        else:
            raise
```

#### Explanation:

The health check implementation demonstrates several key AWS ELB concepts:

- **Health Check Path Parameter**: The `health_check_path` parameter allows customization of the endpoint used for health checks, enabling the ALB to verify application-specific functionality rather than just server availability
- **Health Check Interval Configuration**: The `HealthCheckIntervalSeconds=30` parameter sets the frequency of health checks as specified in the worksheet requirements
- **Target Group Integration**: The health check configuration is embedded within the target group creation, ensuring that health monitoring is established before targets are registered
- **Protocol Matching**: Using `HealthCheckProtocol='HTTP'` ensures the health checks use the same protocol as the application traffic

#### Result:

The ALB performs health checks by sending HTTP GET requests to `http://[instance-ip]:80/polls/` every 30 seconds. The instance is considered healthy if it returns a 200 OK response, and unhealthy if it fails to respond or returns error codes.

![image-20250922175813975](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922175813975.png) 

### [3] Access

With the ALB fully configured and operational, I tested access through the load balancer to verify the complete request routing pipeline.

I accessed the ALB using the DNS name provided by the creation script: `http://24745401-alb-lab6-1210742212.eu-north-1.elb.amazonaws.com/polls/` 

#### Request Flow Analysis:

The complete request flow demonstrates the multi-tier architecture:

1. **Client Request**: Browser sends HTTP request to ALB DNS name
2. **Load Balancer Processing**: ALB receives request on port 80 and determines target based on health checks and routing algorithms
3. **Target Forwarding**: ALB forwards request to healthy EC2 instance on port 80
4. **Nginx Proxy**: nginx on EC2 instance receives request and proxies it to Django on port 8000
5. **Django Processing**: Django application processes `/polls/` URL and returns "Hello, world." response
6. **Response Chain**: Response travels back through nginx → ALB → client browser

#### Result:

The browser successfully displayed "Hello, world." when accessing the ALB URL：

![image-20250922180206312](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922180206312.png) 



## Web interface for CloudStorage application

### [1] Create AWS DynamoDB table and copy data from local DynamoDB

The first step required setting up an AWS DynamoDB table and populating it with the metadata from the local DynamoDB table created in Lab 3. I needed to ensure that my local DynamoDB server from Lab 3 was running before copying the data.

#### Command:

First, I started the local DynamoDB server (if not already running):

```bash
cd ~/dynamodb
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

Then I created and ran the table creation script:

#### Code:

```python
import boto3
from botocore.exceptions import ClientError

# Configuration
STUDENT_ID = '24745401'
REGION = 'eu-north-1'
TABLE_NAME = 'UserFiles'  # Using the table name from Lab 6 instructions

def create_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb', 
        region_name=REGION
    )
    
    print(f"Creating DynamoDB table '{TABLE_NAME}' in AWS cloud...")
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
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
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

def copy_data_from_local_to_aws():
    # Connect to local DynamoDB
    source_dynamodb = boto3.resource(
        'dynamodb', 
        endpoint_url='http://localhost:8000',  # Local DynamoDB endpoint
        region_name='eu-north-1',  # Using the same region as AWS
        aws_access_key_id='dummy',  # Dummy credentials for local
        aws_secret_access_key='dummy'
    )
    source_table = source_dynamodb.Table('CloudFiles')  # Your local table name
    
    # Connect to AWS DynamoDB
    dest_dynamodb = boto3.resource(
        'dynamodb', 
        region_name=REGION,
   )
    dest_table = dest_dynamodb.Table(TABLE_NAME)
    
    # Scan all items from local table
    try:
        response = source_table.scan()
        items = response.get('Items', [])
        
        print(f"Found {len(items)} items in local DynamoDB")
        
        # Copy each item to AWS table
        for item in items:
            dest_table.put_item(Item=item)
            print(f"Copied item: {item.get('fileName', 'unknown')}")
            
        print(f"Successfully copied {len(items)} items to AWS DynamoDB table {TABLE_NAME}")
    except Exception as e:
        print(f"Error copying data: {e}")

if __name__ == "__main__":
    table = create_dynamodb_table()
    if table:
        copy_data_from_local_to_aws()
```

#### Explanation:

This script demonstrates the data migration process from local to cloud infrastructure:

- **Dual DynamoDB Connection**: The script establishes connections to both local DynamoDB (using `endpoint_url='http://localhost:8000'`) and AWS DynamoDB (using default AWS credentials)
- **Table Schema Consistency**: The AWS table maintains the same schema as the local table with `userId` as partition key and `fileName` as sort key
- **Data Transfer Process**: The script scans all items from the local `CloudFiles` table and copies them to the AWS `UserFiles` table
- **Error Handling**: Proper exception handling ensures the script can handle existing tables and connection issues gracefully

#### Result:

The script successfully created the AWS DynamoDB table and copied all file metadata from the local Lab 3 DynamoDB to the cloud-based table, establishing the foundation for the web interface.

![image-20250922181541467](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922181541467.png) 

### [2] Configure Django settings and install dependencies

Before implementing the DynamoDB integration, I needed to configure Django settings and install the required AWS SDK.

#### Command:

On the EC2 instance, I installed the boto3 package:

```bash
pip install boto3
```

I also needed to configure AWS credentials. I updated the Django settings to include the necessary template directory:

```bash
nano /opt/wwc/mysites/lab/lab/settings.py
```

Add to the TEMPLATES section:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'polls/templates/'
        ],
```

### [3] Create HTML template for file display

I created an HTML template to display the file metadata in a formatted web page.

#### Command:

```
mkdir -p /opt/wwc/mysites/lab/polls/templates
nano /opt/wwc/mysites/lab/polls/templates/files.html
```

#### Code:

```html
<html>
<head>
    <title>Files</title>
</head>
<body>
    <h1>Files </h1>

    <ul>
        {% for item in items %}
          <li>{{ item.fileName }}</li>
	{% endfor %}
    </ul>

</body>
</html>
```

#### Explanation:

This Django template demonstrates the framework's template system:

- **Template Inheritance**: The HTML structure provides a basic layout for displaying file information
- **Django Template Tags**: The `{% for item in items %}` loop iterates through the items passed from the view
- **Variable Rendering**: The `{{ item.fileName }}` syntax renders the fileName attribute from each DynamoDB item
- **Template Context**: The template expects an `items` variable containing the file metadata from DynamoDB

### [4] Update Django views to integrate with DynamoDB

The final step involved modifying the Django views to connect to AWS DynamoDB, scan the UserFiles table, and render the results using the template.

#### Code:

```python
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def index(request):
    template = loader.get_template('files.html')

    dynamodb = boto3.resource('dynamodb', region_name='eu-north-1',
                              aws_access_key_id='AKIA············',
                              aws_secret_access_key='jpLi········')

    table = dynamodb.Table("UserFiles")

    items = []
    try:
        response = table.scan()

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:    
        context = {'items': response['Items'] }

        return HttpResponse(template.render(context, request))
```

#### Explanation:

This Django view implementation demonstrates cloud-database integration:

- **AWS SDK Integration**: The `boto3.resource('dynamodb')` creates a connection to AWS DynamoDB using the provided credentials
- **Table Connection**: The `dynamodb.Table("UserFiles")` establishes a connection to the specific table created in step [1]
- **Data Retrieval**: The `table.scan()` operation retrieves all items from the DynamoDB table
- **Template Rendering**: The `template.render(context, request)` method combines the retrieved data with the HTML template
- **Error Handling**: The try-except block handles potential DynamoDB connection or query errors gracefully
- **Context Passing**: The `context = {'items': response['Items']}` passes the DynamoDB results to the template for rendering

#### Command:

```bash
python3 manage.py runserver 8000
```

#### Result:

The Django application successfully connected to AWS DynamoDB, retrieved the file metadata, and displayed it through the web interface.

![image-20250922182128224](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250922182128224.png) 

<div style="page-break-after: always;"></div>

#  Lab 7

## Create an EC2 instance

### [1] Run Lab 7 EC2 setup script

Similarly to what I did in Lab 5 and Lab 6, I reused my existing EC2 management infrastructure to create the instance needed for Lab 7.

#### Code:

```python
# lab7_main.py
# Main script to set up the infrastructure for Lab 7.

import sys
import os

# Add project root to the path to allow importing from 'utils'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils import config
from utils import ec2_manager
from botocore.exceptions import ClientError

if __name__ == "__main__":
    try:
        print("--- Starting Lab 7 Infrastructure Setup ---")

        # Create the key pair
        ec2_manager.create_key_pair(config.LAB7_KEY_NAME)
        print(f"Ensured key pair '{config.LAB7_KEY_NAME}' is available.")

        # Define security rules (SSH + HTTP + Django dev server)
        lab7_sg_rules = [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        ]
        sg_id = ec2_manager.create_security_group(
            config.LAB7_SECURITY_GROUP_NAME,
            "Security Group for Lab 7 DevOps",
            lab7_sg_rules
        )

        # Launch instance
        print("\nLaunching instance...")
        instance_name = f"{config.STUDENT_NUMBER}-vm-lab7"
        instance_id = ec2_manager.setup_instance(
            name=instance_name,
            ami_id=config.AMI_ID,
            instance_type=config.LAB7_INSTANCE_TYPE,
            key_name=config.LAB7_KEY_NAME,
            sg_id=sg_id
        )

        # Get IP and print connection info
        print("\nWaiting for instance to initialize...")
        ip = ec2_manager.get_instance_ip(instance_id)
        print(f"-> {instance_name} is running at Public IP: {ip}")
        print(f"-> SSH command: ssh -i {config.LAB7_KEY_NAME}.pem ubuntu@{ip}")

        print("\n--- EC2 Setup Complete ---")

    except Exception as e:
        print(f"\nError occurred: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
```

#### Result:

The script successfully created the Lab 7 EC2 infrastructure with the public IP address that will be used for Fabric automation.

![image-20250923225224605](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225224605.png) 



## Install and configure Fabric

### [1] Install Fabric locally

I installed Fabric using Python's package manager to enable remote server automation capabilities.

#### Command:

```bash
pip install fabric
```

#### Explanation:

Fabric is a Python library designed for streamlining remote server administration and deployment automation via SSH connections. It provides a high-level interface for executing shell commands remotely, managing SSH connections, and automating complex deployment workflows. Fabric abstracts away the complexity of SSH operations while maintaining the flexibility to execute arbitrary commands on remote servers.

### [2] Create SSH configuration

To enable seamless SSH connectivity to the EC2 instance, I configured SSH settings with a host alias for easier connection management.

#### Command:

```bash
mkdir -p ~/.ssh
cp /root/_codes/cits5503/lab7/24745401-key-lab7.pem ~/.ssh/
chmod 600 ~/.ssh/24745401-key-lab7.pem
nano ~/.ssh/config
```

#### Code:

```
Host 24745401-vm-lab7
	Hostname 51.20.37.169
	User ubuntu
	UserKnownHostsFile /dev/null
	StrictHostKeyChecking no
	PasswordAuthentication no
	IdentityFile ~/.ssh/24745401-key-lab7.pem
```


### [3] Test Fabric connection

Last I verified that Fabric could successfully connect to the EC2 instance and execute remote commands.

#### Command:

```bash
python3 -c "from fabric import Connection; c = Connection('24745401-vm-lab7'); result = c.run('uname -s'); print('Connection test result:', result.stdout.strip())"
```

#### Result:

The connection test successfully returned "Linux", confirming that Fabric could connect to the EC2 instance and execute remote commands.

![image-20250923225314504](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225314504.png) 



## Use Fabric for automation

### [1] Create Fabric deployment manager

To implement comprehensive automation for Django deployment, I developed an enhanced Fabric deployment manager that provides complete application lifecycle management with service-like operations.

#### Code:

```python
# fabric_manager.py - Main deployment manager class
from fabric import Connection
import sys
import time
import argparse

class DjangoDeploymentManager:
    def __init__(self, host):
        self.host = host
        self.c = Connection(host)
        self.app_dir = '/opt/wwc/mysites/lab'
        self.venv_dir = '/opt/wwc/mysites/myvenv'
        self.log_file = '/opt/wwc/mysites/lab/django.log'
```

#### Explanation:

This class establishes the foundation for automated Django deployment management:

- **Connection Management**: The `Connection(host)` object manages SSH connectivity to the remote EC2 instance, handling authentication and session management automatically
- **Path Configuration**: Critical directory paths are centralized as class attributes, ensuring consistency across all deployment operations and matching the Lab 6 directory structure
- **Service Architecture**: The class design follows service-oriented principles, encapsulating all deployment logic within a single manageable interface

#### Code:

```python
# Environment checking and status reporting functions
def check_environment(self):
    """Check what components are already installed/configured"""
    status = {
        'system_packages': False,
        'venv_exists': False,
        'django_project': False,
        'nginx_configured': False,
        'django_running': False
    }

    # Check system packages
    result = self.c.run('which python3 && which nginx', warn=True)
    status['system_packages'] = result.return_code == 0

    # Check virtual environment
    result = self.c.run(f'test -d {self.venv_dir}', warn=True)
    status['venv_exists'] = result.return_code == 0

    # Check Django project
    result = self.c.run(f'test -f {self.app_dir}/manage.py', warn=True)
    status['django_project'] = result.return_code == 0

    # Check nginx configuration
    result = self.c.run('grep -q "proxy_pass.*8000" /etc/nginx/sites-enabled/default', warn=True)
    status['nginx_configured'] = result.return_code == 0

    # Check if Django is running
    result = self.c.run('ps aux | grep "manage.py runserver" | grep -v grep', warn=True)
    status['django_running'] = result.return_code == 0

    return status

def status(self):
    """Show deployment status"""
    print("📊 Deployment Status:")
    status = self.check_environment()

    # Format status in a clean table
    status_items = [
        ("System Packages", status['system_packages']),
        ("Virtual Environment", status['venv_exists']),
        ("Django Project", status['django_project']),
        ("Nginx Configured", status['nginx_configured']),
        ("Django Running", status['django_running'])
    ]

    for item, is_ok in status_items:
        status_icon = '✅' if is_ok else '❌'
        print(f"   {item:<20} {status_icon}")

    if status['django_running']:
        print(f"   🌐 Access: http://{self.c.host}/polls/")

    return status
```

#### Explanation:

These functions implement environment monitoring and status reporting:

- **Idempotent Checking**: The `check_environment()` function verifies deployment components without making changes
- **Status Presentation**: The `status()` function provides clean output with visual indicators (✅/❌)
- **Access Information**: Automatically displays the access URL when Django server is running

#### Code:

```python
# System setup and environment preparation functions
def install_system_packages(self):
    """Install system packages only if needed"""
    print("📦 Checking system packages...")

    # Check what's missing
    missing_packages = []
    packages = ['python3', 'python3-pip', 'python3-venv', 'nginx', 'git']

    for package in packages:
        result = self.c.run(f'dpkg -l | grep -q "^ii.*{package}"', warn=True)
        if result.return_code != 0:
            missing_packages.append(package)

    if missing_packages:
        print(f"   Installing missing packages: {', '.join(missing_packages)}")
        self.c.sudo('apt update')
        self.c.sudo(f'apt install -y {" ".join(missing_packages)}')
    else:
        print("   ✅ All system packages already installed")

def setup_environment(self):
    """Set up directory structure and virtual environment"""
    print("🏗️  Setting up environment...")

    # Create directory structure
    self.c.sudo('mkdir -p /opt/wwc/mysites')
    self.c.sudo('chown ubuntu:ubuntu /opt/wwc/mysites')

    # Check if virtual environment exists
    if not self.c.run(f'test -d {self.venv_dir}', warn=True).return_code == 0:
        print("   Creating virtual environment...")
        self.c.run(f'cd /opt/wwc/mysites && python3 -m venv myvenv')
        self.c.run(f'cd /opt/wwc/mysites && source myvenv/bin/activate && pip install django boto3')
    else:
        print("   ✅ Virtual environment already exists")
        # Ensure packages are installed
        self.c.run(f'cd /opt/wwc/mysites && source myvenv/bin/activate && pip install --quiet django boto3')
```

#### Explanation:

These functions demonstrate intelligent package management and environment setup:

- **Smart Package Installation**: Only installs missing packages, making repeated runs efficient
- **Directory Structure**: Creates the Lab 6-compatible `/opt/wwc/mysites` structure
- **Virtual Environment**: Sets up Python isolation with Django and boto3 dependencies

#### Code:

```python
# Django application deployment and configuration
def deploy_django_app(self, force_recreate=False):
    """Deploy Django application (idempotent)"""
    print("🚀 Deploying Django application...")

    # Check if Django project exists
    project_exists = self.c.run(f'test -f {self.app_dir}/manage.py', warn=True).return_code == 0

    if project_exists and not force_recreate:
        print("   ✅ Django project already exists, updating code only...")
        self._update_django_code()
    else:
        if project_exists:
            print("   🔄 Force recreating Django project...")
            self.c.run(f'rm -rf {self.app_dir}', warn=True)

        print("   Creating new Django project...")
        self._create_django_project()

    # Always run migrations (safe to run multiple times)
    print("   Running Django migrations...")
    self.c.run(f'cd {self.app_dir} && source ../myvenv/bin/activate && python3 manage.py migrate')

def _create_django_project(self):
    """Create fresh Django project with all configurations"""
    # Create Django project
    self.c.run('cd /opt/wwc/mysites && source myvenv/bin/activate && django-admin startproject lab')
    self.c.run(f'cd {self.app_dir} && source ../myvenv/bin/activate && python3 manage.py startapp polls')

    # Create templates directory
    self.c.run(f'mkdir -p {self.app_dir}/polls/templates')

    # Deploy all configurations
    self._update_django_code()
```

#### Explanation:

The Django deployment functions implement smart project management:

- **Project Detection**: Checks for existing Django projects to avoid unnecessary recreation
- **Force Recreation**: Supports complete project rebuild when needed with `--force` flag
- **Modular Design**: Separates project creation from code updates for flexibility

#### Code:

```python
# Django code deployment and nginx configuration
def _update_django_code(self):
    """Update Django code (views, templates, settings)"""
    # Update Django settings with Lab 7 configuration
    # ... settings content including ALLOWED_HOSTS, INSTALLED_APPS, etc. ...
    self.c.run(f'cat > {self.app_dir}/lab/settings.py << "EOF"\n{settings_content}\nEOF')

    # Create enhanced HTML template with professional styling
    # ... template content with CSS styling and Django template tags ...
    self.c.run(f'cat > {self.app_dir}/polls/templates/files.html << "EOF"\n{template_content}\nEOF')

    # Update views with DynamoDB integration
    views_content = '''from django.template import loader
from django.http import HttpResponse
import boto3
from botocore.exceptions import ClientError

def index(request):
    template = loader.get_template('files.html')
    try:
        # Use default credentials (from ~/.aws/credentials or environment variables)
        dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        table = dynamodb.Table("UserFiles")
        response = table.scan()
        items = response.get('Items', [])
        context = {'items': items}
        return HttpResponse(template.render(context, request))
    except ClientError as e:
        # ... error handling ...
'''
        self.c.run(f'cat > {self.app_dir}/polls/views.py << "EOF"\n{views_content}\nEOF')

    # Update URL configurations for polls and main project
    # ... polls/urls.py and lab/urls.py content ...

def configure_nginx(self):
    """Configure nginx (idempotent)"""
    print("🌐 Configuring nginx...")

    # Check if already configured
    result = self.c.run('grep -q "proxy_pass.*8000" /etc/nginx/sites-enabled/default', warn=True)
    if result.return_code == 0:
        print("   ✅ Nginx already configured")
        return

    nginx_config = '''server {
  listen 80 default_server;
  listen [::]:80 default_server;
  location / {
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_pass http://127.0.0.1:8000;
  }
}'''
    self.c.run(f"echo '{nginx_config}' > /tmp/nginx_default")
    self.c.sudo('cp /tmp/nginx_default /etc/nginx/sites-enabled/default')
    self.c.sudo('systemctl restart nginx')
    print("   ✅ Nginx configured and restarted")
```

#### Explanation:

These functions handle the core application configuration and web server setup:

- **Django Configuration**: Updates settings, templates, and views to recreate the Lab 6 cloud storage interface with DynamoDB integration
- **Enhanced Styling**: Implements professional CSS styling for the file display interface
- **Nginx Reverse Proxy**: Configures nginx to proxy requests from port 80 to Django on port 8000, enabling standard web access

#### Code:

```python
# Service management functions
def start_django(self):
    """Start Django server (only if not running)"""
    print("🚀 Starting Django server...")

    # Check if already running
    result = self.c.run('ps aux | grep "manage.py runserver" | grep -v grep', warn=True)
    if result.return_code == 0:
        print("   ✅ Django server already running")
        return True

    # Start Django server using setsid to properly detach
    start_cmd = f'cd {self.app_dir} && source ../myvenv/bin/activate && python3 manage.py runserver 0.0.0.0:8000 > {self.log_file} 2>&1'
    self.c.run(f'setsid bash -c "{start_cmd}" < /dev/null > /dev/null 2>&1 &', warn=True)

    # Wait and verify
    time.sleep(3)
    result = self.c.run('ps aux | grep "manage.py runserver" | grep -v grep', warn=True)
    if result.return_code == 0:
        print("   ✅ Django server started successfully")
        return True
    else:
        print("   ❌ Failed to start Django server")
        return False

def stop_django(self):
    """Stop Django server"""
    print("🛑 Stopping Django server...")
    result = self.c.run('pkill -f "manage.py runserver"', warn=True)
    if result.return_code == 0:
        print("   ✅ Django server stopped")
    else:
        print("   ℹ️  No Django server was running")
    time.sleep(2)

def restart_django(self):
    """Restart Django server"""
    self.stop_django()
    time.sleep(1)
    return self.start_django()
```

#### Explanation:

These service management functions provide standard lifecycle operations:

- **Process Detachment**: Uses `setsid` to properly detach Django processes from Fabric session
- **Status Checking**: Verifies server state before attempting start/stop operations
- **Service Lifecycle**: Implements standard start, stop, and restart operations like system services

#### Code:

```python
# Main deployment orchestration
def deploy(self, force_recreate=False):
    """Full deployment process (idempotent)"""
    print(f"🚀 Starting deployment to {self.host}...")

    try:
        self.install_system_packages()
        self.setup_environment()
        self.deploy_django_app(force_recreate)
        self.configure_nginx()

        if self.start_django():
            print(f"\n🎉 Deployment successful!")
            print(f"🌐 Access: http://{self.c.host}/polls/")
            return True
        else:
            print(f"\n❌ Deployment failed!")
            return False

    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        return False

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description='Django Deployment Manager')
    parser.add_argument('action', choices=['deploy', 'start', 'stop', 'restart', 'status', 'logs'],
                       help='Action to perform')
    parser.add_argument('--force', action='store_true',
                       help='Force recreate Django project (for deploy action)')
    parser.add_argument('--host', default='24745401-vm-lab7',
                       help='SSH host to connect to')

    args = parser.parse_args()
    manager = DjangoDeploymentManager(args.host)

    if args.action == 'deploy':
        manager.deploy(force_recreate=args.force)
    elif args.action == 'start':
        manager.start_django()
    elif args.action == 'stop':
        manager.stop_django()
    elif args.action == 'restart':
        manager.restart_django()
    elif args.action == 'status':
        manager.status()

if __name__ == "__main__":
    main()
```

#### Explanation:

The main deployment orchestration provides complete automation:

- **Sequential Deployment**: Coordinates all deployment steps in correct order
- **Command-line Interface**: Enables service manager functionality with argparse
- **Error Handling**: Provides comprehensive exception handling and status reporting

### [2] Execute automated deployment

I executed the complete Django deployment automation using the Fabric deployment manager.

#### Command:

```bash
python3 fabric_manager.py deploy
```

#### Result:

The script executed successfully, completing all deployment steps including system package installation, virtual environment setup, Django project creation, nginx configuration, and server startup. The deployment process was fully automated and the Django cloud storage application was ready for access.

![image-20250923225428076](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225428076.png) 

![image-20250923225443215](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225443215.png) 

### [3] Verify deployed application

After successful deployment, I accessed to my web app and verified that the cloud storage application was functioning correctly and displaying data from the DynamoDB table.

#### Result

The application successfully displayed the cloud storage interface with files retrieved from the UserFiles DynamoDB table, featuring enhanced CSS styling and proper error handling.

![image-20250923225557074](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225557074.png) 

### [4] Test service management capabilities

I tested the enhanced deployment manager's service lifecycle operations to verify complete functionality.

#### Command:

```bash
python3 fabric_manager.py status
```

#### Result:

The status command displayed a clean overview of all deployment components with proper alignment and visual indicators.

![image-20250923225747518](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225747518.png) 

#### Command:

```bash
python3 fabric_manager.py stop
```

#### Result:

The stop command successfully terminated the Django server processes and confirmed the shutdown.

![image-20250923225824925](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225824925.png) 

![image-20250923225845340](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225845340.png) 

#### Command:

```bash
python3 fabric_manager.py start
```

#### Result:

The start command launched the Django server and verified it was running properly without hanging the Fabric session.

![image-20250923225927871](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225927871.png) 

![image-20250923225949336](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923225949336.png) 

#### Command:

```bash
python3 fabric_manager.py restart
```

#### Result:

The restart command performed a clean stop followed by start operation, demonstrating complete service lifecycle management.

![image-20250923230042341](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20250923230042341.png) 

<div style="page-break-after: always;"></div>

# Lab 8

## Create a Dockerfile and build a Docker image

### [1] Create and build the Dockerfile

First, I created a `Dockerfile` as specified in the lab worksheet to containerize the Jupyter environment with all necessary dependencies for the SageMaker task.

#### Code:

```dockerfile
FROM python:3.10

RUN pip install jupyter boto3 sagemaker awscli
RUN mkdir /notebook

# Use a sample access token
ENV JUPYTER_ENABLE_LAB=yes
ENV JUPYTER_TOKEN="CITS5503"

# Allow access from ALL IPs
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py

# Copy the ipynb file
RUN wget -P /notebook https://raw.githubusercontent.com/zhangzhics/CITS5503_Sem2/master/Labs/src/LabAI.ipynb

WORKDIR /notebook
EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

#### Explanation:

This Dockerfile sets up a complete, portable environment for our AI task:
- **`FROM python:3.10`**: Starts with a standard Python 3.10 base image.
- **`RUN pip install ...`**: Installs all required Python libraries, including `jupyter` for the notebook, `boto3` and `sagemaker` for AWS interaction, and the `awscli`.
- **`ENV JUPYTER_TOKEN="CITS5503"`**: Sets a static token for accessing the Jupyter notebook, simplifying access.
- **`RUN echo "c.NotebookApp.ip = '0.0.0.0'"`**: Configures Jupyter to accept connections from any IP address, which is essential for accessing it when it's running in an ECS container.
- **`RUN wget ...`**: Downloads the `LabAI.ipynb` notebook directly into the container, ensuring it's available on startup.
- **`EXPOSE 8888`**: Documents that the container will listen on port 8888.
- **`CMD [...]`**: Specifies the default command to run when the container starts, launching the Jupyter notebook server.

#### Command:

I then built the Docker image from the Dockerfile.

```bash
docker build -t 24745401-lab8 .
```

### [2] Test the Docker image locally

To verify the image was built correctly, I ran it locally.

#### Command:

```bash
docker run -p 8888:8888 24745401-lab8
```

#### Result:

The container started successfully, and I was able to access the Jupyter notebook by navigating to `http://127.0.0.1:8888` in my browser. This confirmed the environment was set up correctly and the notebook was present.

![image_2025-10-06_06-51-21](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image_2025-10-06_06-51-21.png) 

## Prepare ECR via Boto3 scripts

### [1] Create ECR repository

Next, I used a Python script to programmatically create an Amazon Elastic Container Registry (ECR) repository to store my Docker image.

#### Code:

```python
# prepare_ecr.py
import boto3
import base64

def create_or_check_repository(repository_name):
    ecr_client = boto3.client('ecr')
    try:
        response = ecr_client.describe_repositories(repositoryNames=[repository_name])
        repository_uri = response['repositories'][0]['repositoryUri']
    except ecr_client.exceptions.RepositoryNotFoundException:
        response = ecr_client.create_repository(repositoryName=repository_name)
        repository_uri = response['repository']['repositoryUri']
    return repository_uri

def get_docker_login_cmd():
    ecr_client = boto3.client('ecr')
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    registry = token['authorizationData'][0]['proxyEndpoint']
    return f"docker login -u {username} -p {password} {registry}"

if __name__ == "__main__":
    repository_name = '24745401_ecr_repo'
    repository_uri = create_or_check_repository(repository_name)
    print("ECR URI:", repository_uri)
    print(get_docker_login_cmd())
```

#### Explanation:

This script automates the ECR setup:
- **`create_or_check_repository`**: This function is idempotent. It first checks if an ECR repository with the specified name already exists. If not, it creates one. It then returns the repository URI, which is needed for tagging and pushing the image.
- **`get_docker_login_cmd`**: This function retrieves a temporary authorization token from ECR and constructs the `docker login` command needed to authenticate my local Docker client with the AWS registry.

#### Result:

Running the script outputted the ECR repository URI and the `docker login` command.

![image_2025-10-06_06-54-08](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image_2025-10-06_06-54-08.png)

### [2] Authenticate Docker to ECR

I ran the outputted command in my terminal to authenticate.

#### Result:

The command returned a "Login Succeeded" message, confirming my Docker client could now push images to my ECR repository.



## Push a local Docker image onto ECR

### [1] Tag and Push the image

With authentication complete, I tagged my local image with the ECR repository URI and pushed it to AWS.

#### Command:

```bash
docker tag 24745401-lab8:latest 489389878001.dkr.ecr.eu-north-1.amazonaws.com/24745401_ecr_repo:latest
docker push 489389878001.dkr.ecr.eu-north-1.amazonaws.com/24745401_ecr_repo:latest
```

#### Result:

The Docker image was successfully uploaded to the ECR repository. I could see the image listed in the AWS ECR console.

![image_2025-10-06_06-56-23](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image_2025-10-06_06-56-23.png) 

![image-20251007093822381](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20251007093822381.png) 

## Deploy your Docker image onto ECS

### [1] Create ECS Cluster, Task Definition, and Service

I created a single script, `deploy_ecs.py`, to handle the entire ECS deployment process, leveraging my reusable `ecs_manager.py` and `ec2_manager.py` modules.

#### Code:

```python
# deploy_ecs.py
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils import config
from utils import ecs_manager
from utils import ec2_manager
import boto3

if __name__ == "__main__":
    ecs_client = boto3.client('ecs')

    ecr_uri = '489389878001.dkr.ecr.eu-north-1.amazonaws.com/24745401_ecr_repo:latest'

    # Create Task Definition
    task_definition_response = ecs_manager.create_ecs_task_definition(
        ecs_client,
        image_uri=ecr_uri,
        account_id=config.ACCOUNT_ID,
        task_role_name='SageMakerRole',
        execution_role_name='ecsTaskExecutionRole',
        student_id=config.STUDENT_NUMBER,
        log_group='/ecs/lab8-service', 
        log_region=config.REGION_NAME,
        port=8888
    )
    task_definition_arn = task_definition_response['taskDefinition']['taskDefinitionArn']
    print(f"Task Definition ARN: {task_definition_arn}")

    # Create Cluster
    cluster_name = f'{config.STUDENT_NUMBER}-cluster'
    ecs_manager.create_ecs_cluster(ecs_client, cluster_name)
    print(f"ECS Cluster: {cluster_name}")

    # Get Subnets and Security Group
    subnet_ids = ec2_manager.get_all_subnet_ids()
    lab8_sg_rules = [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 8888, 'ToPort': 8888, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    sg_id = ec2_manager.create_security_group(
        config.MY_SECURITY_GROUP_NAME, 
        "Security Group for general use", 
        lab8_sg_rules
    )

    # Create Service
    service_name = f'{config.STUDENT_NUMBER}-service'
    service_response = ecs_manager.create_ecs_service(
        ecs_client, 
        cluster_name, 
        service_name, 
        task_definition_arn, 
        subnet_ids, 
        [sg_id]
    )
    print(f'ECS Service created: {service_response["service"]["serviceArn"]}')

    print(f'Waiting for service {service_name} to become stable...')
    ecs_manager.wait_for_service_stability(ecs_client, cluster_name, service_name)
    print(f'Service {service_name} is now stable.')
```

#### Explanation:

This script orchestrates the entire deployment on ECS Fargate:
1.  **Task Definition**: It first defines the task using `create_ecs_task_definition`. This is the blueprint for our application, specifying the Docker image (`ecr_uri`), required IAM roles (`SageMakerRole`, `ecsTaskExecutionRole`), and container settings like port mappings.
2.  **Cluster Creation**: It ensures an ECS cluster named `{student_id}-cluster` exists using `create_ecs_cluster`.
3.  **Networking**: It fetches all available subnet IDs and creates a new security group that allows inbound traffic on port 8888 (for Jupyter) and 22 (for SSH).
4.  **Service Creation**: It creates an ECS service (`create_ecs_service`) which is responsible for running and maintaining the specified number of instances of the task definition. It's configured to use Fargate for serverless execution, assigns a public IP, and connects it to the correct subnets and security group.
5.  **Wait for Stability**: Finally, it uses a waiter (`wait_for_service_stability`) to pause the script until the ECS service is fully deployed and stable.

#### Result:

The script ran successfully, creating all the necessary AWS resources and deploying the container.

![image-20251007093941713](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20251007093941713.png) 

### [2] Get Public IP and Access the Notebook

After the service was stable, I used the AWS CLI to find the public IP address of the running Fargate task.

#### Command:

```bash
aws ecs describe-tasks \
    --cluster 24745401-cluster \
    --tasks $(aws ecs list-tasks --cluster 24745401-cluster --service-name 24745401-service --query 'taskArns[0]' --output text) \
    --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' \
    --output text | xargs -I {} aws ec2 describe-network-interfaces \
    --network-interface-ids {} \
    --query 'NetworkInterfaces[0].Association.PublicIp' \
    --output text
```

#### Result:

This command chain retrieved the public IP of my running container. I accessed the Jupyter notebook at `http://16.16.75.95:8888` and again entered our jupyter notebook deployed on the ECS.

![image_2025-10-06_08-06-54](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image_2025-10-06_08-06-54.png)

![image-20251007094416827](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image-20251007094416827.png)

## Run Hyperparameter Tuning Jobs

Inside the Jupyter notebook running on ECS, I performed the steps to train a model and find the best hyperparameters using Amazon SageMaker.

### [1] Setup and Data Preparation

First, I entered my AWS credentials to allow the notebook to interact with AWS services. The provided notebook expected an S3 bucket to be present, but since previous lab resources were deleted, I updated the notebook to include logic that programmatically creates the required S3 bucket if it doesn't already exist. This addition makes the notebook more robust and self-contained.

#### Code:

```python
# Prepare a SageMaker session and ensure S3 bucket exists
import sagemaker
import numpy as np
import pandas as pd
from time import gmtime, strftime
from botocore.exceptions import ClientError
import logging

smclient = boto3.Session().client("sagemaker")
sagemaker_role = "arn:aws:iam::489389878001:role/SageMakerRole"
region = os.environ['AWS_DEFAULT_REGION']
student_id = "24745401"
bucket = "24745401-lab8"
prefix = f"sagemaker/{student_id}-hpo-xgboost-dm"

s3_client = boto3.client("s3")

def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, 
                             CreateBucketConfiguration=location)
        print("Bucket created successfully")

    except ClientError as e:
        logging.error(e)
        return False
    return True

# Check if bucket exists, if not create it
try:
    s3_client.head_bucket(Bucket=bucket)
    print("Bucket %s already exists" % bucket)
except ClientError as e:
    if e.response['Error']['Code'] == '404':
        print("Bucket %s does not exist. Creating it..." % bucket)
        create_bucket(bucket, region)
    else:
        logging.error(e)
        exit()

# Create a folder (prefix) in the bucket
try:
    s3_client.put_object(Bucket=bucket, Key=f"{prefix}/")
    print(f"Folder {prefix}/ created successfully")
except Exception as e:
    print(f"Error creating folder: {e}")
```

### [2] Data Download and Preprocessing

I downloaded the bank marketing dataset, loaded it into a pandas DataFrame, and performed preprocessing to convert categorical features into a numerical format suitable for the model.

#### Code:

```python
# Download and unzip data
!wget -N https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip
!unzip -o bank-additional.zip

# Read into pandas
data = pd.read_csv("./bank-additional/bank-additional-full.csv", sep=";")

# Feature engineering and conversion to dummy variables
data["no_previous_contact"] = np.where(data["pdays"] == 999, 1, 0)
data["not_working"] = np.where(np.in1d(data["job"], ["student", "retired", "unemployed"]), 1, 0)
model_data = pd.get_dummies(data)
model_data = model_data.drop(
    ["duration", "emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"],
    axis=1,
)
```

### [3] Data Splitting and Uploading to S3

I split the data into training (70%), validation (20%), and test (10%) sets. Then, I formatted them as CSV files with the target variable in the first column and uploaded the training and validation sets to the S3 bucket.

#### Code:

```python
# Split data
train_data, validation_data, test_data = np.split(
    model_data.sample(frac=1, random_state=1729),
    [int(0.7 * len(model_data)), int(0.9 * len(model_data))],
)

# Save to CSV and upload to S3
pd.concat([train_data["y_yes"], train_data.drop(["y_no", "y_yes"], axis=1)], axis=1).to_csv(
    "train.csv", index=False, header=False
)
pd.concat(
    [validation_data["y_yes"], validation_data.drop(["y_no", "y_yes"], axis=1)], axis=1
).to_csv("validation.csv", index=False, header=False)

boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "train/train.csv")
).upload_file("train.csv")
boto3.Session().resource("s3").Bucket(bucket).Object(
    os.path.join(prefix, "validation/validation.csv")
).upload_file("validation.csv")
```

### [4] Configure and Launch Hyperparameter Tuning Job

I defined the configuration for the SageMaker hyperparameter tuning job. This included defining the ranges for the hyperparameters I wanted to tune (`eta`, `min_child_weight`, `alpha`, `max_depth`), the objective metric (`validation:auc`), and the resource limits.

#### Code:

```python
# Define tuning job configuration
tuning_job_name = f"{student_id}-xgboost-tuningjob-01"
tuning_job_config = {
    "ParameterRanges": {
        "ContinuousParameterRanges": [
            {"MaxValue": "1", "MinValue": "0", "Name": "eta"},
            {"MaxValue": "10", "MinValue": "1", "Name": "min_child_weight"},
            {"MaxValue": "2", "MinValue": "0", "Name": "alpha"},
        ],
        "IntegerParameterRanges": [
            {"MaxValue": "10", "MinValue": "1", "Name": "max_depth"}
        ],
    },
    "ResourceLimits": {"MaxNumberOfTrainingJobs": 2, "MaxParallelTrainingJobs": 2},
    "Strategy": "Bayesian",
    "HyperParameterTuningJobObjective": {"MetricName": "validation:auc", "Type": "Maximize"},
}

# Define the training job structure
from sagemaker.image_uris import retrieve
training_image = retrieve(framework="xgboost", region=region, version="latest")
# ... training_job_definition ...

# Launch the tuning job
smclient.create_hyper_parameter_tuning_job(
    HyperParameterTuningJobName=tuning_job_name,
    HyperParameterTuningJobConfig=tuning_job_config,
    TrainingJobDefinition=training_job_definition,
)
```

#### Result:

The hyperparameter tuning job was successfully launched. I monitored its progress in the AWS SageMaker console. After a few minutes, the job completed, and SageMaker identified the combination of hyperparameters that resulted in the best model performance based on the AUC metric.

![image_2025-10-06_08-42-13](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image_2025-10-06_08-42-13.png) 

I also confirmed all the training result was successfully uploaded to my newly-created S3 bucket.

![image_2025-10-06_08-44-29](https://cdn.jsdelivr.net/gh/WitherLzero/myImages@main/img/image_2025-10-06_08-44-29.png)

# Lab 9

## AWS Comprehend - Natural Language Processing

### Detect Languages from Text

#### [1] Modify the code to detect different languages

The first task required modifying the provided code to detect different languages and return a user-friendly message showing the language name (not just the code) with confidence as a percentage.

#### Code:

```python
#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Language Detection
Detects the dominant language in a given text and displays confidence as percentage.
"""

import boto3
from botocore.exceptions import ClientError

# Language code to language name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'it': 'Italian',
    'de': 'German',
    'pt': 'Portuguese',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'ru': 'Russian',
}

def detect_language(text):
    """
    Detect the dominant language in the given text.
    """
    client = boto3.client('comprehend', region_name='us-east-1')

    try:
        response = client.detect_dominant_language(Text=text)

        if response['Languages']:
            top_language = response['Languages'][0]
            language_code = top_language['LanguageCode']
            confidence_score = top_language['Score']

            # Convert language code to name
            language_name = LANGUAGE_NAMES.get(language_code, language_code.upper())

            # Convert confidence to percentage
            confidence_percentage = int(confidence_score * 100)

            return language_name, confidence_percentage
        else:
            return None, 0

    except ClientError as e:
        print(f"Error: {e}")
        return None, 0
```

#### Explanation:

This implementation enhances the basic language detection code provided in the lab worksheet:

- **AWS Comprehend Client**: The `boto3.client('comprehend', region_name='ap-southeast-2')` creates a connection to AWS Comprehend service in the ap-southeast-2 region as specified in the lab requirements.

- **Language Name Mapping**: The `LANGUAGE_NAMES` dictionary converts AWS's two-letter language codes (e.g., 'en', 'es') into full language names (e.g., 'English', 'Spanish'), meeting the requirement to display language names rather than codes.

- **Confidence Score Conversion**: The confidence score returned by AWS Comprehend is a float value between 0 and 1. The code multiplies this by 100 and converts to an integer to display it as a percentage (e.g., 0.9961 becomes 99%).

- **Message Format**: The function returns both the language name and confidence percentage, which can be formatted into the required message: "<predicted_language> was detected with <xx>% confidence".

#### [2] Test the code with other languages

I tested the language detection script with all four texts provided in the lab worksheet: English, Spanish, French, and Italian.

#### Code:

```python
def main():
    """Test the language detection with sample texts."""

    # Test texts from the lab worksheet
    test_texts = {
        'English': "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",

        'Spanish': "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas. En 1615 aparecería la segunda parte del Quijote de Cervantes con el título de El ingenioso caballero don Quijote de la Mancha.",

        'French': "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",

        'Italian': "L'amor che move il sole e l'altre stelle."
    }

    print("="*60)
    print("AWS Comprehend - Language Detection Test")
    print("="*60)

    for expected_lang, text in test_texts.items():
        print(f"\n{'─'*60}")
        print(f"Expected: {expected_lang}")
        print(f"Text: {text[:80]}..." if len(text) > 80 else f"Text: {text}")
        print(f"{'─'*60}")

        language_name, confidence = detect_language(text)

        if language_name:
            print(f"✓ {language_name} was detected with {confidence}% confidence")
        else:
            print("✗ Could not detect language")

    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
```

#### Result:

After running the script, all four languages were successfully detected with high confidence:
```plaintext
root@paulyn:~/_codes/cits5503/lab9# python3 detect_languages.py 
============================================================
AWS Comprehend - Language Detection Test
============================================================

────────────────────────────────────────────────────────────
Expected: English
Text: The French Revolution was a period of social and political upheaval in France an...
────────────────────────────────────────────────────────────
✓ English was detected with 99% confidence

────────────────────────────────────────────────────────────
Expected: Spanish
Text: El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su...
────────────────────────────────────────────────────────────
✓ Spanish was detected with 99% confidence

────────────────────────────────────────────────────────────
Expected: French
Text: Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses...
────────────────────────────────────────────────────────────
✓ French was detected with 99% confidence

────────────────────────────────────────────────────────────
Expected: Italian
Text: L'amor che move il sole e l'altre stelle.
────────────────────────────────────────────────────────────
✓ Italian was detected with 99% confidence

============================================================
```



### Analyse Sentiment

Sentiment analysis (or opinion mining) uses NLP to determine whether data is positive, negative, neutral, or mixed. I created a Python script using AWS Comprehend to perform sentiment analysis on the four texts provided in the lab worksheet.

#### Code:

```python
#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Sentiment Analysis
Analyzes whether text is positive, negative, neutral, or mixed.
"""

import boto3
from botocore.exceptions import ClientError

def analyze_sentiment(text, language_code='en'):
    """
    Analyze the sentiment of a text.

    Args:
        text (str): The text to analyze
        language_code (str): Language code (e.g., 'en', 'es', 'fr')

    Returns:
        dict: Sentiment analysis results
    """
    client = boto3.client('comprehend', region_name='ap-southeast-2')

    try:
        response = client.detect_sentiment(
            Text=text,
            LanguageCode=language_code
        )

        return response

    except ClientError as e:
        print(f"Error: {e}")
        return None

def main():
    """Test sentiment analysis with sample texts."""

    # Use the same 4 texts from language detection section above
    test_texts = {
        'English': {'text': "...", 'lang': 'en'},
        'Spanish': {'text': "...", 'lang': 'es'},
        'French': {'text': "...", 'lang': 'fr'},
        'Italian': {'text': "...", 'lang': 'it'}
    }

    print("="*70)
    print("AWS Comprehend - Sentiment Analysis Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Preview: {data['text'][:80]}..." if len(data['text']) > 80 else f"Text: {data['text']}")
        print(f"{'─'*70}")

        result = analyze_sentiment(data['text'], data['lang'])

        if result:
            sentiment = result['Sentiment']
            scores = result['SentimentScore']

            print(f"✓ Overall Sentiment: {sentiment}")
            print(f"\n  Confidence Scores:")
            print(f"    Positive:  {scores['Positive']:.4f} ({scores['Positive']*100:.2f}%)")
            print(f"    Negative:  {scores['Negative']:.4f} ({scores['Negative']*100:.2f}%)")
            print(f"    Neutral:   {scores['Neutral']:.4f} ({scores['Neutral']*100:.2f}%)")
            print(f"    Mixed:     {scores['Mixed']:.4f} ({scores['Mixed']*100:.2f}%)")
        else:
            print("✗ Could not analyze sentiment")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
```

#### Explanation:

This implementation demonstrates AWS Comprehend's sentiment analysis capabilities:

- **Sentiment Detection API**: The `client.detect_sentiment(Text=text, LanguageCode=language_code)` method analyzes the emotional tone of the text and classifies it into one of four categories: POSITIVE, NEGATIVE, NEUTRAL, or MIXED.

- **Language Code Parameter**: AWS Comprehend requires the language code to be specified for sentiment analysis. The script automatically detects and uses the appropriate language code ('en', 'es', 'fr', 'it') for each text.

- **Sentiment Score**: AWS Comprehend returns confidence scores for all four sentiment categories, with values ranging from 0 to 1. The sum of all four scores equals 1.0, representing a probability distribution across the sentiment categories.

- **Multi-language Support**: The script tests sentiment analysis across four different languages, demonstrating Comprehend's multilingual sentiment analysis capabilities.

#### Result:

After running the script, the sentiment analysis successfully classified each text and provided confidence scores for all sentiment categories:
```plaintext
root@paulyn:~/_codes/cits5503/lab9# python3 analyze_sentiment.py 
======================================================================
AWS Comprehend - Sentiment Analysis Test
======================================================================

──────────────────────────────────────────────────────────────────────
Text: English
Preview: The French Revolution was a period of social and political upheaval in France an...
──────────────────────────────────────────────────────────────────────
✓ Overall Sentiment: NEUTRAL

  Confidence Scores:
    Positive:  0.0003 (0.03%)
    Negative:  0.0007 (0.07%)
    Neutral:   0.9991 (99.91%)
    Mixed:     0.0000 (0.00%)

──────────────────────────────────────────────────────────────────────
Text: Spanish
Preview: El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su...
──────────────────────────────────────────────────────────────────────
✓ Overall Sentiment: NEUTRAL

  Confidence Scores:
    Positive:  0.0475 (4.75%)
    Negative:  0.0002 (0.02%)
    Neutral:   0.9522 (95.22%)
    Mixed:     0.0001 (0.01%)

──────────────────────────────────────────────────────────────────────
Text: French
Preview: Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses...
──────────────────────────────────────────────────────────────────────
✓ Overall Sentiment: POSITIVE

  Confidence Scores:
    Positive:  0.6963 (69.63%)
    Negative:  0.2653 (26.53%)
    Neutral:   0.0102 (1.02%)
    Mixed:     0.0282 (2.82%)

──────────────────────────────────────────────────────────────────────
Text: Italian
Text: L'amor che move il sole e l'altre stelle.
──────────────────────────────────────────────────────────────────────
✓ Overall Sentiment: POSITIVE

  Confidence Scores:
    Positive:  0.9967 (99.67%)
    Negative:  0.0010 (0.10%)
    Neutral:   0.0021 (0.21%)
    Mixed:     0.0002 (0.02%)

======================================================================
```

### Detect Entities

Entity detection identifies and categorizes real-world objects or concepts mentioned in text. I created a Python script using AWS Comprehend to detect entities in the four test texts.

**Answer to the question "What are entities?":**

Entities are real-world objects or concepts that are mentioned in text, such as people, locations, organizations, dates, quantities, events, and titles. AWS Comprehend can automatically identify and categorize these entities into predefined types. For example, in the text "Amazon was founded by Jeff Bezos in Seattle", the entities would be:
- "Amazon" (ORGANIZATION)
- "Jeff Bezos" (PERSON)
- "Seattle" (LOCATION)

Unlike abstract concepts, entities refer to specific, concrete references that can be classified into standard categories. This helps in understanding the key subjects and objects discussed in a text.

#### Code:

```python
#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Entity Detection
Detects named entities (people, places, organizations, dates, etc.) in text.
"""

import boto3
from botocore.exceptions import ClientError

def detect_entities(text, language_code='en'):
    """
    Detect entities in a text.

    Args:
        text (str): The text to analyze
        language_code (str): Language code (e.g., 'en', 'es', 'fr', 'it')

    Returns:
        list: List of detected entities
    """
    client = boto3.client('comprehend', region_name='ap-southeast-2')

    try:
        response = client.detect_entities(
            Text=text,
            LanguageCode=language_code
        )

        return response['Entities']

    except ClientError as e:
        print(f"Error: {e}")
        return []

def main():
    """Test entity detection with sample texts."""

    # Use the same 4 texts from language detection section above
    test_texts = {
        'English': {'text': "...", 'lang': 'en'},
        'Spanish': {'text': "...", 'lang': 'es'},
        'French': {'text': "...", 'lang': 'fr'},
        'Italian': {'text': "...", 'lang': 'it'}
    }

    print("="*70)
    print("AWS Comprehend - Entity Detection Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Preview: {data['text'][:80]}..." if len(data['text']) > 80 else f"Full text: {data['text']}")
        print(f"{'─'*70}")

        entities = detect_entities(data['text'], data['lang'])

        if entities:
            print(f"✓ Found {len(entities)} entities:")

            # Group entities by type
            by_type = {}
            for entity in entities:
                entity_type = entity['Type']
                if entity_type not in by_type:
                    by_type[entity_type] = []
                by_type[entity_type].append(entity)

            # Display grouped entities
            for entity_type, items in sorted(by_type.items()):
                print(f"\n  {entity_type}:")
                for entity in items:
                    confidence = entity['Score'] * 100
                    print(f"    • '{entity['Text']}' (Confidence: {confidence:.2f}%)")
        else:
            print("✗ No entities detected")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
```

#### Explanation:

This implementation demonstrates AWS Comprehend's entity detection capabilities:

- **Entity Detection API**: The `client.detect_entities(Text=text, LanguageCode=language_code)` method identifies and extracts entities from the text, categorizing them into types such as PERSON, LOCATION, ORGANIZATION, DATE, QUANTITY, EVENT, and TITLE.

- **Entity Grouping**: The script groups detected entities by their type for better readability, making it easier to understand what categories of information are present in the text.

- **Confidence Scores**: Each detected entity comes with a confidence score indicating how certain AWS Comprehend is about the entity type classification. Higher scores indicate greater confidence in the detection.

- **Multilingual Entity Detection**: The script processes texts in four different languages (English, Spanish, French, Italian), demonstrating Comprehend's ability to recognize entities across multiple languages.

#### Result:

After running the script, entities were successfully detected and categorized in each text:

```plaintext
root@paulyn:~/_codes/cits5503/lab9# python3 detect_entities.py 
======================================================================
AWS Comprehend - Entity Detection Test
======================================================================

──────────────────────────────────────────────────────────────────────
Text: English
Preview: The French Revolution was a period of social and political upheaval in France an...
──────────────────────────────────────────────────────────────────────
✓ Found 4 entities:

  DATE:
    • '1789' (Confidence: 99.80%)
    • '1799' (Confidence: 99.87%)

  EVENT:
    • 'French Revolution' (Confidence: 98.60%)

  LOCATION:
    • 'France' (Confidence: 98.98%)

──────────────────────────────────────────────────────────────────────
Text: Spanish
Preview: El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su...
──────────────────────────────────────────────────────────────────────
✓ Found 12 entities:

  DATE:
    • '1605' (Confidence: 79.77%)
    • '1615' (Confidence: 98.81%)

  OTHER:
    • 'española' (Confidence: 98.65%)

  PERSON:
    • 'Miguel de Cervantes Saavedra' (Confidence: 99.93%)

  QUANTITY:
    • 'primera parte' (Confidence: 86.64%)
    • 'una de' (Confidence: 59.71%)
    • 'una de las más' (Confidence: 63.20%)
    • 'segunda parte' (Confidence: 88.87%)

  TITLE:
    • 'El Quijote' (Confidence: 96.96%)
    • 'El ingenioso hidalgo don Quijote de la Mancha' (Confidence: 87.85%)
    • 'Quijote de Cervantes' (Confidence: 74.33%)
    • 'El ingenioso caballero don Quijote de la Mancha' (Confidence: 91.13%)

──────────────────────────────────────────────────────────────────────
Text: French
Preview: Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses...
──────────────────────────────────────────────────────────────────────
✓ Found 2 entities:

  DATE:
    • 'aujourd'hui' (Confidence: 98.08%)

  QUANTITY:
    • 'Tout ce qu'' (Confidence: 66.27%)

──────────────────────────────────────────────────────────────────────
Text: Italian
Full text: L'amor che move il sole e l'altre stelle.
──────────────────────────────────────────────────────────────────────
✗ No entities detected

======================================================================
```

### Detect Keyphrases

Keyphrase detection extracts the main topics or important phrases from text. I created a Python script using AWS Comprehend to detect keyphrases in the four test texts.

**Answer to the question "What are keyphrases?":**

Keyphrases are the main topics or important phrases in a text that capture its essential meaning and core concepts. They are typically noun phrases that represent key ideas being discussed. Unlike entities (which must be specific real-world objects like "Jeff Bezos" or "Seattle"), keyphrases can be broader concepts or topics. For example, in the text "The new smartphone features advanced camera technology", the keyphrases would be:
- "new smartphone"
- "advanced camera technology"

Keyphrases help in understanding what a text is about at a high level, making them useful for document summarization, content categorization, and topic extraction.

#### Code:

```python
#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Keyphrase Detection
Detects key phrases (main topics and important concepts) in text.
"""

import boto3
from botocore.exceptions import ClientError

def detect_keyphrases(text, language_code='en'):
    """
    Detect key phrases in a text.
    """
    client = boto3.client('comprehend', region_name='ap-southeast-2')

    try:
        response = client.detect_key_phrases(
            Text=text,
            LanguageCode=language_code
        )

        return response['KeyPhrases']

    except ClientError as e:
        print(f"Error: {e}")
        return []

def main():
    """Test keyphrase detection with sample texts."""

    # Use the same 4 texts from language detection section above
    test_texts = {
        'English': {'text': "...", 'lang': 'en'},
        'Spanish': {'text': "...", 'lang': 'es'},
        'French': {'text': "...", 'lang': 'fr'},
        'Italian': {'text': "...", 'lang': 'it'}
    }

    print("="*70)
    print("AWS Comprehend - Keyphrase Detection Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Preview: {data['text'][:80]}..." if len(data['text']) > 80 else f"Full text: {data['text']}")
        print(f"{'─'*70}")

        keyphrases = detect_keyphrases(data['text'], data['lang'])

        if keyphrases:
            print(f"✓ Found {len(keyphrases)} keyphrases:")

            # Sort by confidence (highest first)
            sorted_keyphrases = sorted(keyphrases, key=lambda x: x['Score'], reverse=True)

            for i, phrase in enumerate(sorted_keyphrases, 1):
                confidence = phrase['Score'] * 100
                print(f"  {i}. '{phrase['Text']}' (Confidence: {confidence:.2f}%)")
        else:
            print("✗ No keyphrases detected")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
```

#### Explanation:

This implementation demonstrates AWS Comprehend's keyphrase detection capabilities:

- **Keyphrase Detection API**: The `client.detect_key_phrases(Text=text, LanguageCode=language_code)` method identifies important noun phrases that represent the main topics and concepts in the text.

- **Confidence Sorting**: The script sorts keyphrases by confidence score in descending order, placing the most confidently detected keyphrases at the top of the list, making it easier to identify the most relevant topics.

- **Keyphrase Score**: Each keyphrase comes with a confidence score indicating how certain AWS Comprehend is that this phrase represents a key topic in the text. Higher scores indicate greater confidence.

- **Topic Extraction**: Unlike entity detection which focuses on concrete real-world objects, keyphrase detection identifies broader themes and important concepts, making it useful for understanding the overall subject matter of a text.

#### Result:

After running the script, keyphrases were successfully extracted from each text, showing the main topics and concepts:

```plaintext
root@paulyn:~/_codes/cits5503/lab9# python3 detect_keyphrases.py 
======================================================================
AWS Comprehend - Keyphrase Detection Test
======================================================================

──────────────────────────────────────────────────────────────────────
Text: English
Preview: The French Revolution was a period of social and political upheaval in France an...
──────────────────────────────────────────────────────────────────────
✓ Found 7 keyphrases:
  1. 'The French Revolution' (Confidence: 100.00%)
  2. 'its colonies' (Confidence: 100.00%)
  3. 'a period' (Confidence: 100.00%)
  4. '1789' (Confidence: 100.00%)
  5. 'social and political upheaval' (Confidence: 100.00%)
  6. 'France' (Confidence: 99.99%)
  7. '1799' (Confidence: 99.99%)

──────────────────────────────────────────────────────────────────────
Text: Spanish
Preview: El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su...
──────────────────────────────────────────────────────────────────────
✓ Found 18 keyphrases:
  1. 'el título' (Confidence: 100.00%)
  2. 'la segunda parte' (Confidence: 100.00%)
  3. 'Miguel de Cervantes Saavedra' (Confidence: 100.00%)
  4. 'las obras' (Confidence: 100.00%)
  5. 'la literatura española' (Confidence: 100.00%)
  6. 'la obra' (Confidence: 100.00%)
  7. 'el título' (Confidence: 99.99%)
  8. 'la literatura universal' (Confidence: 99.99%)
  9. 'Quijote de Cervantes' (Confidence: 99.99%)
  10. 'su primera parte' (Confidence: 99.99%)
  11. 'más destacadas' (Confidence: 99.99%)
  12. 'comienzos' (Confidence: 99.98%)
  13. 'las más traducidas' (Confidence: 99.95%)
  14. 'El Quijote' (Confidence: 99.95%)
  15. 'más conocida' (Confidence: 99.88%)
  16. '1605' (Confidence: 99.62%)
  17. 'El ingenioso hidalgo don Quijote de la Mancha' (Confidence: 95.61%)
  18. 'ingenioso caballero don Quijote de la Mancha' (Confidence: 93.65%)

──────────────────────────────────────────────────────────────────────
Text: French
Preview: Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses...
──────────────────────────────────────────────────────────────────────
✓ Found 18 keyphrases:
  1. 'l'' (Confidence: 99.99%)
  2. 'Je' (Confidence: 99.99%)
  3. 'Moi' (Confidence: 99.99%)
  4. 'Je' (Confidence: 99.99%)
  5. 'l'' (Confidence: 99.98%)
  6. 'Elle' (Confidence: 99.98%)
  7. 'vous' (Confidence: 99.97%)
  8. 'Vous' (Confidence: 99.90%)
  9. 'il' (Confidence: 99.86%)
  10. 'L'espace de ses bras' (Confidence: 99.47%)
  11. 'Tout ce' (Confidence: 98.28%)
  12. 'qu'' (Confidence: 96.47%)
  13. 'tout' (Confidence: 96.25%)
  14. 'n'étais rien' (Confidence: 95.63%)
  15. 'je' (Confidence: 95.50%)
  16. 'aujourd'hui' (Confidence: 94.90%)
  17. 'Je suis le gardien Du sommeil de ses nuits' (Confidence: 94.12%)
  18. 'tout' (Confidence: 89.33%)

──────────────────────────────────────────────────────────────────────
Text: Italian
Full text: L'amor che move il sole e l'altre stelle.
──────────────────────────────────────────────────────────────────────
✓ Found 4 keyphrases:
  1. 'il sole' (Confidence: 100.00%)
  2. 'l'altre stelle' (Confidence: 99.99%)
  3. 'L'amor' (Confidence: 99.99%)
  4. 'che' (Confidence: 99.98%)

======================================================================
```

### Detect Syntaxes

Syntax detection analyzes the grammatical structure of text by identifying parts of speech for each word. I created a Python script using AWS Comprehend to detect syntax in the four test texts.

**Answer to the question "What is syntax?":**

Syntax refers to the grammatical structure of text, specifically the parts of speech (POS) and how words function within sentences. Syntax detection identifies each word's grammatical role and how it relates to other words in the sentence. For example, in the sentence "The cat runs quickly":
- "The" = DETERMINER (DET)
- "cat" = NOUN
- "runs" = VERB
- "quickly" = ADVERB (ADV)

Understanding syntax helps in analyzing sentence structure, grammar checking, text-to-speech systems, and understanding how words relate to each other grammatically.

#### Code:

```python
#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Syntax Detection
Detects parts of speech (grammatical structure) in text.
"""

import boto3
from botocore.exceptions import ClientError

def detect_syntax(text, language_code='en'):
    """
    Detect syntax (parts of speech) in a text.
    """
    client = boto3.client('comprehend', region_name='ap-southeast-2')

    try:
        response = client.detect_syntax(
            Text=text,
            LanguageCode=language_code
        )

        return response['SyntaxTokens']

    except ClientError as e:
        print(f"Error: {e}")
        return []

def main():
    """Test syntax detection with sample texts."""

    # Use first sentence of each text for clarity
    test_texts = {
        'English': {
            'text': "The French Revolution was a period of social and political upheaval in France.",
            'lang': 'en'
        },
        'Spanish': {
            'text': "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra.",
            'lang': 'es'
        },
        'French': {
            'text': "Je suis le gardien du sommeil de ses nuits.",
            'lang': 'fr'
        },
        'Italian': {
            'text': "L'amor che move il sole e l'altre stelle.",
            'lang': 'it'
        }
    }

    print("="*70)
    print("AWS Comprehend - Syntax Detection Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Sentence: {data['text']}")
        print(f"{'─'*70}")

        syntax_tokens = detect_syntax(data['text'], data['lang'])

        if syntax_tokens:
            print(f"✓ Found {len(syntax_tokens)} tokens:\n")

            # Display in a table format
            print(f"  {'#':<4} {'Word':<20} {'POS':<8} {'Confidence':<12}")
            print(f"  {'-'*4} {'-'*20} {'-'*8} {'-'*12}")

            for i, token in enumerate(syntax_tokens, 1):
                word = token['Text']
                pos_tag = token['PartOfSpeech']['Tag']
                confidence = token['PartOfSpeech']['Score'] * 100

                print(f"  {i:<4} {word:<20} {pos_tag:<8} {confidence:>6.2f}%")

            # Summary of POS types
            pos_counts = {}
            for token in syntax_tokens:
                pos = token['PartOfSpeech']['Tag']
                pos_counts[pos] = pos_counts.get(pos, 0) + 1

            print(f"\n  Summary:")
            for pos, count in sorted(pos_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"    {pos}: {count}")

        else:
            print("✗ Syntax detection not supported for this language")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
```

#### Explanation:

This implementation demonstrates AWS Comprehend's syntax detection capabilities:

- **Syntax Detection API**: The `client.detect_syntax(Text=text, LanguageCode=language_code)` method analyzes each word in the text and assigns it a part of speech tag (e.g., NOUN, VERB, ADJ, DET, ADP).

- **Token Analysis**: Each word (token) is analyzed individually, with AWS Comprehend identifying its grammatical function and providing a confidence score for the classification.

- **POS Tags**: Common part of speech tags include NOUN (nouns), VERB (verbs), ADJ (adjectives), ADV (adverbs), DET (determiners like "the", "a"), ADP (prepositions), PRON (pronouns), and others.

- **Tabular Display**: The script formats the output in a table showing each token's position, the word itself, its POS tag, and the confidence score, making it easy to understand the grammatical structure of the sentence.

- **Summary Statistics**: A summary section groups and counts tokens by their POS type, providing an overview of the grammatical composition of the text.

#### Result:

After running the script, the syntax analysis successfully identified parts of speech for each word:

```plaintext
root@paulyn:~/_codes/cits5503/lab9# python3 detect_syntax.py 
======================================================================
AWS Comprehend - Syntax Detection Test
======================================================================

──────────────────────────────────────────────────────────────────────
Text: English
Sentence: The French Revolution was a period of social and political upheaval in France.
──────────────────────────────────────────────────────────────────────
✓ Found 14 tokens:

  #    Word                 POS      Confidence  
  ---- -------------------- -------- ------------
  1    The                  DET      100.00%
  2    French               PROPN    100.00%
  3    Revolution           PROPN    100.00%
  4    was                  VERB     100.00%
  5    a                    DET      100.00%
  6    period               NOUN     100.00%
  7    of                   ADP      100.00%
  8    social               ADJ      100.00%
  9    and                  CCONJ    100.00%
  10   political            ADJ      100.00%
  11   upheaval             NOUN     100.00%
  12   in                   ADP      100.00%
  13   France               PROPN    100.00%
  14   .                    PUNCT    100.00%

  Summary:
    PROPN: 3 (Proper noun (names))
    DET: 2 (Determiner (the, a, this))
    NOUN: 2 (Noun (person, place, thing))
    ADP: 2 (Adposition (preposition))
    ADJ: 2 (Adjective (describes noun))
    VERB: 1 (Verb (action or state))
    CCONJ: 1 (Coordinating conjunction)
    PUNCT: 1 (Punctuation)

──────────────────────────────────────────────────────────────────────
Text: Spanish
Sentence: El Quijote es la obra más conocida de Miguel de Cervantes Saavedra.
──────────────────────────────────────────────────────────────────────
✓ Found 13 tokens:

  #    Word                 POS      Confidence  
  ---- -------------------- -------- ------------
  1    El                   DET      100.00%
  2    Quijote              PROPN    100.00%
  3    es                   VERB     100.00%
  4    la                   DET      100.00%
  5    obra                 NOUN     100.00%
  6    más                  ADV      100.00%
  7    conocida             ADJ       99.93%
  8    de                   ADP      100.00%
  9    Miguel               PROPN    100.00%
  10   de                   ADP      100.00%
  11   Cervantes            PROPN    100.00%
  12   Saavedra             PROPN    100.00%
  13   .                    PUNCT    100.00%

  Summary:
    PROPN: 4 (Proper noun (names))
    DET: 2 (Determiner (the, a, this))
    ADP: 2 (Adposition (preposition))
    VERB: 1 (Verb (action or state))
    NOUN: 1 (Noun (person, place, thing))
    ADV: 1 (Adverb (describes verb))
    ADJ: 1 (Adjective (describes noun))
    PUNCT: 1 (Punctuation)

──────────────────────────────────────────────────────────────────────
Text: French
Sentence: Je suis le gardien du sommeil de ses nuits.
──────────────────────────────────────────────────────────────────────
✓ Found 10 tokens:

  #    Word                 POS      Confidence  
  ---- -------------------- -------- ------------
  1    Je                   PRON     100.00%
  2    suis                 AUX      100.00%
  3    le                   DET      100.00%
  4    gardien              NOUN     100.00%
  5    du                   ADP      100.00%
  6    sommeil              NOUN     100.00%
  7    de                   ADP      100.00%
  8    ses                  DET      100.00%
  9    nuits                NOUN     100.00%
  10   .                    PUNCT    100.00%

  Summary:
    NOUN: 3 (Noun (person, place, thing))
    DET: 2 (Determiner (the, a, this))
    ADP: 2 (Adposition (preposition))
    PRON: 1 (Pronoun (replaces noun))
    AUX: 1 (Auxiliary verb (is, was, have))
    PUNCT: 1 (Punctuation)

──────────────────────────────────────────────────────────────────────
Text: Italian
Sentence: L'amor che move il sole e l'altre stelle.
──────────────────────────────────────────────────────────────────────
✓ Found 11 tokens:

  #    Word                 POS      Confidence  
  ---- -------------------- -------- ------------
  1    L'                   DET      100.00%
  2    amor                 NOUN     100.00%
  3    che                  PRON     100.00%
  4    move                 VERB     100.00%
  5    il                   DET      100.00%
  6    sole                 NOUN     100.00%
  7    e                    CCONJ    100.00%
  8    l'                   DET      100.00%
  9    altre                ADJ      100.00%
  10   stelle               NOUN     100.00%
  11   .                    PUNCT    100.00%

  Summary:
    DET: 3 (Determiner (the, a, this))
    NOUN: 3 (Noun (person, place, thing))
    PRON: 1 (Pronoun (replaces noun))
    VERB: 1 (Verb (action or state))
    CCONJ: 1 (Coordinating conjunction)
    ADJ: 1 (Adjective (describes noun))
    PUNCT: 1 (Punctuation)

======================================================================
```


## AWS Rekognition

AWS Rekognition is the service of AWS that allows us to perform machine learning tasks on images. Currently, given an image, AWS Rekognition allows:
1. **Label Recognition**: automatically label objects, concepts, scenes, and actions in your images, and provide a confidence score.
2. **Image Moderation**: automatically detect explicit or suggestive adult content, or violent content in your images, and provide confidence scores.
3. **Facial Analysis**: get a complete analysis of facial attributes, including confidence scores.
4. **Extract Text from an image**: automatically detect and extract text in your images.

### Add Images

We need to create an S3 bucket to store images for Rekognition testing. The bucket will be created in the ap-southeast-2 region (same as Rekognition service region) to avoid cross-region access issues.

**Code:**

```python
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
```

**Explanation:**

The script follows the same structure as Lab 3's cloud storage script. It provides two main functions:

1. `create_bucket()`: Creates an S3 bucket in ap-southeast-2 region. The function first checks if the bucket already exists using `head_bucket()` to make the operation idempotent. For regions other than us-east-1, it includes the `LocationConstraint` parameter.

2. `upload_file()`: Uploads a local image file to the S3 bucket using the boto3 `upload_file()` method.

The main program creates the bucket and automatically uploads all images (jpg, jpeg, png) from the `images` directory. We prepared 4 images as required: urban.jpg, beach.jpg, faces.jpg, and text.jpg.

**Result:**

```plaintext
[SCREENSHOT PLACEHOLDER - Will show bucket creation and image upload confirmation]
```

### Test AWS Rekognition

We created a comprehensive test script that uses boto3 and AWS Rekognition to test all four capabilities: label recognition, image moderation, facial analysis, and text extraction.

#### [1] Configuration and Setup

**Code:**

```python
#!/usr/bin/env python3
"""
Lab 9 - AWS Rekognition Tests
Tests label recognition, image moderation, facial analysis, and text extraction.
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils import config
import boto3
from botocore.exceptions import ClientError

# Configuration
BUCKET_NAME = f'{config.STUDENT_NUMBER}-lab9-in-ap'
BUCKET_REGION = 'ap-southeast-2'
REKOGNITION_REGION = 'ap-southeast-2'

# Initialize Rekognition client
rekognition_client = boto3.client('rekognition', region_name=REKOGNITION_REGION)
```

**Explanation:**

This section sets up the necessary imports and configuration for the Rekognition tests. We configure the bucket name and regions, ensuring both the S3 bucket and Rekognition service are in ap-southeast-2 region to avoid cross-region access issues. The Rekognition client is initialized once and reused across all test functions.

#### [2] Label Recognition Function

**Code:**

```python
def detect_labels(bucket, key, max_labels=10, min_confidence=80):
    """Detect labels (objects, scenes, concepts) in an image."""
    try:
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
        return response['Labels']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def test_label_recognition():
    """Test label recognition on all images."""
    print("\n" + "="*70)
    print("TEST 1: LABEL RECOGNITION")
    print("="*70)

    test_images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

    for image in test_images:
        print(f"\nImage: {image}")
        print("-"*70)

        labels = detect_labels(BUCKET_NAME, image)

        if labels:
            print(f"Found {len(labels)} labels:")
            for label in labels:
                print(f"  • {label['Name']}: {label['Confidence']:.2f}% confidence")
                if label.get('Parents'):
                    parents = [p['Name'] for p in label['Parents']]
                    print(f"    Categories: {', '.join(parents)}")
        else:
            print("No labels detected")
```

**Explanation:**

The label recognition function uses the `detect_labels()` API to identify objects, scenes, and concepts in images. It accepts parameters for maximum labels (10) and minimum confidence threshold (80%). The function returns labels with confidence scores and parent categories. We test all 4 images to see what objects, scenes, and concepts Rekognition can identify.

**Result:**

```plaintext
======================================================================
TEST 1: LABEL RECOGNITION
======================================================================

Image: urban.jpg
----------------------------------------------------------------------
✓ Found 10 labels:
  • Architecture: 100.00% confidence
  • Building: 100.00% confidence
    Categories: Architecture
  • Cityscape: 100.00% confidence
    Categories: Architecture, Building, Urban
  • Urban: 100.00% confidence
  • City: 100.00% confidence
  • Outdoors: 99.74% confidence
  • Road: 99.48% confidence
  • Aerial View: 91.43% confidence
    Categories: Outdoors
  • Tower: 90.73% confidence
    Categories: Architecture, Building
  • Car: 80.85% confidence
    Categories: Transportation, Vehicle

Image: beach.jpg
----------------------------------------------------------------------
✓ Found 10 labels:
  • Horizon: 99.99% confidence
    Categories: Nature, Outdoors, Sky
  • Nature: 99.99% confidence
    Categories: Outdoors
  • Outdoors: 99.99% confidence
  • Sky: 99.99% confidence
    Categories: Nature, Outdoors
  • Shorts: 99.91% confidence
    Categories: Clothing
  • Beach: 99.87% confidence
    Categories: Coast, Nature, Outdoors, Sea, Shoreline, Water
  • Sea: 99.87% confidence
    Categories: Nature, Outdoors, Water
  • Photography: 99.64% confidence
  • Person: 99.49% confidence
  • Walking: 99.44% confidence
    Categories: Person

Image: faces.jpg
----------------------------------------------------------------------
✓ Found 10 labels:
  • Face: 100.00% confidence
    Categories: Head, Person
  • Head: 100.00% confidence
    Categories: Person
  • Person: 100.00% confidence
  • Photography: 100.00% confidence
  • Portrait: 100.00% confidence
    Categories: Face, Head, Person, Photography
  • Adult: 99.80% confidence
    Categories: Person
  • Female: 99.80% confidence
    Categories: Person
  • Woman: 99.80% confidence
    Categories: Adult, Female, Person
  • Blonde: 99.40% confidence
    Categories: Hair, Person
  • Neck: 98.56% confidence
    Categories: Body Part, Face, Head, Person

Image: text.jpg
----------------------------------------------------------------------
✓ Found 6 labels:
  • Car: 97.18% confidence
    Categories: Transportation, Vehicle
  • Transportation: 97.18% confidence
  • Vehicle: 97.18% confidence
    Categories: Transportation
  • Road Sign: 80.04% confidence
    Categories: Sign, Symbol
  • Sign: 80.04% confidence
    Categories: Symbol
  • Symbol: 80.04% confidence
```

#### [3] Image Moderation Function

**Code:**

```python
def detect_moderation_labels(bucket, key, min_confidence=60):
    """Detect moderation labels (explicit or inappropriate content)."""
    try:
        response = rekognition_client.detect_moderation_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MinConfidence=min_confidence
        )
        return response['ModerationLabels']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def test_image_moderation():
    """Test image moderation on all images."""
    print("\n" + "="*70)
    print("TEST 2: IMAGE MODERATION")
    print("="*70)

    test_images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

    for image in test_images:
        print(f"\nImage: {image}")
        print("-"*70)

        labels = detect_moderation_labels(BUCKET_NAME, image)

        if labels:
            print(f"Found {len(labels)} moderation labels:")
            for label in labels:
                print(f"  • {label['Name']}: {label['Confidence']:.2f}% confidence")
                if label.get('ParentName'):
                    print(f"    Parent category: {label['ParentName']}")
        else:
            print("No inappropriate content detected")
```

**Explanation:**

The image moderation function uses the `detect_moderation_labels()` API to detect inappropriate content such as explicit or suggestive adult content and violent content. It uses a minimum confidence threshold of 60% and returns moderation labels with their parent categories. This is useful for content filtering and safety applications.

**Result:**

```plaintext
======================================================================
TEST 2: IMAGE MODERATION
======================================================================

Image: urban.jpg
----------------------------------------------------------------------
✓ No inappropriate content detected

Image: beach.jpg
----------------------------------------------------------------------
✓ No inappropriate content detected

Image: faces.jpg
----------------------------------------------------------------------
✓ No inappropriate content detected

Image: text.jpg
----------------------------------------------------------------------
✓ No inappropriate content detected
```

#### [4] Facial Analysis Function

**Code:**

```python
def detect_faces(bucket, key):
    """Detect and analyze faces in an image."""
    try:
        response = rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            Attributes=['ALL']
        )
        return response['FaceDetails']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def test_facial_analysis():
    """Test facial analysis on images with people."""
    print("\n" + "="*70)
    print("TEST 3: FACIAL ANALYSIS")
    print("="*70)

    # Test on images that likely contain faces
    face_images = ['faces.jpg', 'beach.jpg']

    for image in face_images:
        print(f"\nImage: {image}")
        print("-"*70)

        faces = detect_faces(BUCKET_NAME, image)

        if faces:
            print(f"Found {len(faces)} face(s):")
            for i, face in enumerate(faces, 1):
                print(f"\n  Face {i}:")
                print(f"    Age range: {face['AgeRange']['Low']}-{face['AgeRange']['High']} years")
                print(f"    Gender: {face['Gender']['Value']} ({face['Gender']['Confidence']:.2f}% confidence)")

                # Emotions
                emotions = sorted(face['Emotions'], key=lambda x: x['Confidence'], reverse=True)
                print(f"    Top emotion: {emotions[0]['Type']} ({emotions[0]['Confidence']:.2f}% confidence)")

                # Other attributes
                print(f"    Smile: {face['Smile']['Value']} ({face['Smile']['Confidence']:.2f}% confidence)")
                print(f"    Eyes open: {face['EyesOpen']['Value']} ({face['EyesOpen']['Confidence']:.2f}% confidence)")
                print(f"    Sunglasses: {face['Sunglasses']['Value']} ({face['Sunglasses']['Confidence']:.2f}% confidence)")
                print(f"    Beard: {face['Beard']['Value']} ({face['Beard']['Confidence']:.2f}% confidence)")
                print(f"    Mustache: {face['Mustache']['Value']} ({face['Mustache']['Confidence']:.2f}% confidence)")
        else:
            print("No faces detected")
```

**Explanation:**

The facial analysis function uses the `detect_faces()` API with `Attributes=['ALL']` to perform comprehensive facial analysis. It detects and analyzes multiple facial attributes including age range, gender, emotions, and physical features like smile, sunglasses, beard, and mustache. We test this on faces.jpg and beach.jpg which likely contain faces. The emotions are sorted by confidence to show the most likely emotion first.

**Result:**

```plaintext
======================================================================
TEST 3: FACIAL ANALYSIS
======================================================================

Image: faces.jpg
----------------------------------------------------------------------
✓ Found 1 face(s):

  Face 1:
    Age range: 13-19 years
    Gender: Female (99.78% confidence)
    Top emotion: CALM (99.86% confidence)
    Smile: False (99.87% confidence)
    Eyes open: True (99.42% confidence)
    Sunglasses: False (99.97% confidence)
    Beard: False (99.26% confidence)
    Mustache: False (99.95% confidence)

Image: beach.jpg
----------------------------------------------------------------------
✓ Found 1 face(s):

  Face 1:
    Age range: 33-41 years
    Gender: Male (99.64% confidence)
    Top emotion: ANGRY (74.22% confidence)
    Smile: False (99.40% confidence)
    Eyes open: True (97.98% confidence)
    Sunglasses: False (99.87% confidence)
    Beard: False (75.94% confidence)
    Mustache: False (99.53% confidence)
```

#### [5] Text Extraction Function

**Code:**

```python
def detect_text(bucket, key):
    """Detect and extract text from an image (OCR)."""
    try:
        response = rekognition_client.detect_text(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
        return response['TextDetections']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def test_text_extraction():
    """Test text extraction (OCR) on all images."""
    print("\n" + "="*70)
    print("TEST 4: TEXT EXTRACTION (OCR)")
    print("="*70)

    test_images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

    for image in test_images:
        print(f"\nImage: {image}")
        print("-"*70)

        text_detections = detect_text(BUCKET_NAME, image)

        if text_detections:
            # Separate WORD and LINE detections
            lines = [t for t in text_detections if t['Type'] == 'LINE']
            words = [t for t in text_detections if t['Type'] == 'WORD']

            print(f"Found {len(lines)} line(s) and {len(words)} word(s)")

            if lines:
                print("\n  Lines detected:")
                for line in lines:
                    print(f"    • '{line['DetectedText']}' ({line['Confidence']:.2f}% confidence)")

            if words and len(words) <= 20:
                print("\n  Words detected:")
                for word in words:
                    print(f"    • '{word['DetectedText']}' ({word['Confidence']:.2f}% confidence)")
            elif words:
                print(f"\n  (Showing first 20 of {len(words)} words)")
                for word in words[:20]:
                    print(f"    • '{word['DetectedText']}' ({word['Confidence']:.2f}% confidence)")
        else:
            print("No text detected")
```

**Explanation:**

The text extraction function uses the `detect_text()` API to perform OCR (Optical Character Recognition) on images. It detects and extracts text, separating LINE detections (full lines of text) from WORD detections (individual words). This is useful for extracting text from signs, documents, or any text visible in images. To keep output manageable, we limit word display to 20 words if there are many detections.

**Result:**

```plaintext
======================================================================
TEST 4: TEXT EXTRACTION (OCR)
======================================================================

Image: urban.jpg
----------------------------------------------------------------------
✓ Found 5 line(s) and 5 word(s)

  Lines detected:
    • 'the' (28.18% confidence)
    • 'NOHMI' (98.14% confidence)
    • 'MIWA' (96.60% confidence)
    • 'MIWA' (96.25% confidence)
    • 'KAMMOTO' (94.52% confidence)

  Words detected:
    • 'the' (28.18% confidence)
    • 'NOHMI' (98.14% confidence)
    • 'MIWA' (96.60% confidence)
    • 'MIWA' (96.25% confidence)
    • 'KAMMOTO' (94.52% confidence)

Image: beach.jpg
----------------------------------------------------------------------
✗ No text detected

Image: faces.jpg
----------------------------------------------------------------------
✗ No text detected

Image: text.jpg
----------------------------------------------------------------------
✓ Found 3 line(s) and 4 word(s)

  Lines detected:
    • 'AUTO' (100.00% confidence)
    • 'PRET VÃRTIEM' (94.19% confidence)
    • 'NELIKT!' (97.92% confidence)

  Words detected:
    • 'AUTO' (100.00% confidence)
    • 'PRET' (100.00% confidence)
    • 'VÃRTIEM' (88.38% confidence)
    • 'NELIKT!' (97.92% confidence)
```

#### [6] Main Execution

**Code:**

```python
def main():
    """Run all Rekognition tests."""

    print("="*70)
    print("Lab 9 - AWS Rekognition Tests")
    print(f"Bucket: {BUCKET_NAME} (Region: {BUCKET_REGION})")
    print(f"Rekognition Region: {REKOGNITION_REGION}")
    print("="*70)

    # Run all tests
    test_label_recognition()
    test_image_moderation()
    test_facial_analysis()
    test_text_extraction()

    print("\n" + "="*70)
    print("All tests completed!")
    print("="*70)

if __name__ == "__main__":
    main()
```

**Explanation:**

The main function orchestrates all four Rekognition tests, running them sequentially and displaying the configuration details at the start. We run the script with `python3 test_rekognition.py` to execute all tests on our uploaded images.
