#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
from ZscalerCity import get_cidrs

# 设置AWS配置文件
PROFILE = "it"
SESSION = boto3.session.Session(profile_name=PROFILE)
EC2 = SESSION.client('ec2')
RESOURCE = SESSION.resource('ec2')
    

# 添加CIDR到安全组的函数
def add_loc_cidr_sg(location, cidr_ip, sg_id, port_range):
    try:
        response = EC2.authorize_security_group_ingress(
            #DryRun=True,
            GroupId=sg_id,
            IpPermissions=[{
                'FromPort': port_range[0],
                'ToPort': port_range[1],
                'IpProtocol':'tcp',
                'IpRanges': [{
                    'CidrIp': cidr_ip,
                    'Description': location
                },]
            },]
        )
        return(response)
    except ClientError as err:
        print(err)


# 删除CIDR从安全组的函数
def del_loc_cidr_sg(location, cidr_ip, sg_id, port_range):
    try:
        response = RESOURCE.SecurityGroup(sg_id).revoke_ingress(
            #DryRun=True,
            GroupId=sg_id,
            IpPermissions=[{
                'FromPort': port_range[0],
                'ToPort': port_range[1],
                'IpProtocol':'tcp',
                'IpRanges': [{
                    'CidrIp': cidr_ip,
                    'Description': location
                },]
            },]
        )
        return(response)
    except ClientError as err:
        print(err)


if __name__ == "__main__":
    # 定义办公室城市和CIDR
    OFFICE_CITIES = ['Toronto II', 'London III', 'Dallas I']
    OFFICE_CITIES_CIDRS = get_cidrs(OFFICE_CITIES)
    CUSTOMER_CIDRS = {'Customer I': '164.225.37.0/23', 'Customer II': '164.225.81.0/22'}
    MY_CITIES_CIDRS = {**OFFICE_CITIES_CIDRS, **CUSTOMER_CIDRS}
    
    MY_FROM_TO_PORTS = [[443, 443]]
    MY_GROUP_IDS = ['sg-1234567']

    print('The following Cidrs should be whitelisted: ')
    print(MY_CITIES_CIDRS)
    print()
    for city, cidr in MY_CITIES_CIDRS.items():
        for group_id in MY_GROUP_IDS:
            for from_to_ports in MY_FROM_TO_PORTS:
                #del_loc_cidr_sg(city, cidr, group_id, from_to_ports)
                add_loc_cidr_sg(city, cidr, group_id, from_to_ports)