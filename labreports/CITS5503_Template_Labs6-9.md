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

<div style="page-break-after: always;"></div>

# Lab 8

<div style="page-break-after: always;"></div>

# Lab 9

