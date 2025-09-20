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