#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
from ZscalerCity import get_cidrs
from ModifySecurityGroup import add_loc_cidr_sg

PROFILE = "it"
SESSION = boto3.session.Session(profile_name=PROFILE)
EC2 = SESSION.client('ec2')
RESOURCE = SESSION.resource('ec2')

OFFICE_CITIES = ['Toronto II', 'London III', 'Dallas I']
OFFICE_CITIES_CIDRS = get_cidrs(OFFICE_CITIES)

INCAPSULA_CIDRS = {'Incapsula IP1': '1.1.1.0/21', 'Incapsula IP2': '2.1.1.0/19', 'Incapsula IP3': '3.1.1.0/21'}
MY_CITIES_CIDRS = {**OFFICE_CITIES_CIDRS, **INCAPSULA_CIDRS}
MY_FROM_TO_PORTS = [[443, 443]]

MY_VPC_IDs = ['vpc-11111111']
MY_GROUP_NAME = "SomeWhitelist"
MY_GROUP_DESC = "Holds Incapsula/Zscalar IPs to be whitelisted"

def create_sg(vpcid, groupname, desc):
    try:
        response = EC2.create_security_group(
            #DryRun=True,
            Description=desc,
            GroupName=groupname,
            VpcId=vpcid           
        )
        return(response)
    except ClientError as err:
        print(err)


# there is no way to get groupid programtically, not using this function
#def del_sg(groupid, desc):
#    try:
#        response = RESOURCE.SecurityGroup(sg_id).revoke_ingress(
#            DryRun=True,
#            GroupId=groupid,
#            GroupName=groupid
#            
#        )
#        print(response)
#    except ClientError as err:
#        print(err)


MY_GROUP_IDS = []
for vpc_id in MY_VPC_IDs:
    MY_GROUP_IDS.append(create_sg(vpc_id, MY_GROUP_NAME, MY_GROUP_DESC)['GroupId'])
print('The following security groups are created: ')
print(MY_GROUP_IDS)

for city, cidr in MY_CITIES_CIDRS.items():
    for group_id in MY_GROUP_IDS:
        for from_to_ports in MY_FROM_TO_PORTS:
            add_loc_cidr_sg(city, cidr, group_id, from_to_ports)
print('The following Cidrs are whitelisted: ')
print(MY_CITIES_CIDRS)
