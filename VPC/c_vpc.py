import boto3
import time

region = 'us-east-1'
instance_id = input("Enter Instance Id: ")
ec2 = boto3.client('ec2', region_name=region)
ec21=boto3.resource('ec2', region_name=region)

#starting our instances
ec2.start_instances(InstanceIds=[instance_id])
print('started your instances: ' + instance_id)

vpc = ec21.create_vpc(CidrBlock='10.0.0.0/16')
vpc.create_tags(Tags=[{"Key":"Name", "Value":"DontDelete-yogi-VPC"}])
vpc.wait_until_available()
print(vpc.id)

subnet1 = ec21.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc.id)
subnet2 = ec21.create_subnet(CidrBlock='10.0.2.0/24', VpcId=vpc.id)
subnet3 = ec21.create_subnet(CidrBlock='10.0.3.0/24', VpcId=vpc.id)
subnet4 = ec21.create_subnet(CidrBlock='10.0.4.0/24', VpcId=vpc.id)
print(subnet1.id)
print(subnet2.id)
print(subnet3.id)
print(subnet4.id)

#Internet Gateway
ig = ec21.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

#creating a route table and a public route
route_table = vpc.create_route_table()
route = route_table.create_route(
   DestinationCidrBlock='0.0.0.0/0',
   GatewayId=ig.id
)
print(route_table.id)

#2 public subnets
route_table.associate_with_subnet(SubnetId=subnet1.id)
route_table.associate_with_subnet(SubnetId=subnet2.id)

#NAT Gateway
addr = ec2.allocate_address(Domain='vpc')
c = addr['AllocationId']
   
nat_gw = ec2.create_nat_gateway(SubnetId=subnet1.id,AllocationId=c)
print(nat_gw)
time.sleep(100)

#A route table to route to NAT
route_table2 = vpc.create_route_table()
route = route_table2.create_route(
   DestinationCidrBlock='0.0.0.0/0',
   GatewayId=nat_gw['NatGateway']['NatGatewayId']
)
print(route_table2.id)
route_table2.associate_with_subnet(SubnetId=subnet3.id)
route_table2.associate_with_subnet(SubnetId=subnet4.id)