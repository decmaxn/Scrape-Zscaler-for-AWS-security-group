#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
from ZscalerCity import get_cidrs
from ModifySecurityGroup import add_loc_cidr_sg

# 设置AWS配置文件
PROFILE = "it"
SESSION = boto3.session.Session(profile_name=PROFILE)
EC2 = SESSION.client('ec2')
RESOURCE = SESSION.resource('ec2')

# 定义办公室城市和CIDR
OFFICE_CITIES = ['Toronto II', 'London III', 'Dallas I']
OFFICE_CITIES_CIDRS = get_cidrs(OFFICE_CITIES)

# 定义Incapsula的CIDR
INCAPSULA_CIDRS = {'Incapsula IP1': '1.1.1.0/21', 'Incapsula IP2': '2.1.1.0/19', \
                   'Incapsula IP3': '3.1.1.0/21'}
MY_CITIES_CIDRS = {**OFFICE_CITIES_CIDRS, **INCAPSULA_CIDRS}
MY_FROM_TO_PORTS = [[443, 443]]

# 定义VPC ID和安全组属性
MY_VPC_IDs = ['vpc-11111111']
MY_GROUP_NAME = "SomeWhitelist"
MY_GROUP_DESC = "Holds Incapsula/Zscalar IPs to be whitelisted"
MY_GROUP_TAGS = [{'Key': 'Environment', 'Value': 'UAT'}, {'Key': 'Name', 'Value': MY_GROUP_NAME}]

# 创建安全组的函数
def create_sg(vpcid, groupname, desc, tags):
    try:
        response = EC2.create_security_group(
            #DryRun=True,
            Description=desc,
            GroupName=groupname,
            VpcId=vpcid
        )
        security_group = RESOURCE.SecurityGroup(response['GroupId'])
        tags = security_group.create_tags(
            #DryRun=True,
            Tags=tags
        )
        return response
    except ClientError as err:
        print(err)

# 创建安全组并存储其ID
MY_GROUP_IDS = []
for vpc_id in MY_VPC_IDs:
    MY_GROUP_IDS.append(create_sg(vpc_id, MY_GROUP_NAME, MY_GROUP_DESC, MY_GROUP_TAGS)['GroupId'])
print('The following security groups are created: ')
print(MY_GROUP_IDS)

# 将城市的CIDR添加到安全组中
for city, cidr in MY_CITIES_CIDRS.items():
    for group_id in MY_GROUP_IDS:
        for from_to_ports in MY_FROM_TO_PORTS:
            add_loc_cidr_sg(city, cidr, group_id, from_to_ports)
print('The following Cidrs are whitelisted: ')
print(MY_CITIES_CIDRS)
