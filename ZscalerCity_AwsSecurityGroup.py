#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import ClientError

PROFILE = "victor"
SESSION = boto3.session.Session(profile_name=PROFILE)
EC2 = SESSION.client('ec2')
RESOURCE = SESSION.resource('ec2')


MY_FROM_TO_PORTS = [[443, 443]]
MY_GROUP_IDS = ['sg-11111111']
MY_CITIES = ['Toronto II', 'London III', 'Dallas I']
URL = "https://ips.zscaler.net/cenr"

HTML = requests.get(URL)
BS = BeautifulSoup(HTML.content, "lxml")

def get_cidrs(city_list):
    cities_cidrs_dict = {}
    tables = BS.find_all('table')
    for table in tables:
        try:
            tbodies = table.find_all('tbody')
            for tbody in tbodies:
                rows = tbody.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    for col in cols:
                        if col.text in city_list:
                            cities_cidrs_dict[col.text] = row.find_all('td')[1].text
        except:
            print("no body")
    return(cities_cidrs_dict)

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
                    'Description': 'Zscaler ' + location
                },]
            },]
        )
        print(response)
    except ClientError as err:
        print(err)


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
                    'Description': 'Zscaler ' + location
                },]
            },]
        )
        print(response)
    except ClientError as err:
        print(err)




MY_CITIES_CIDRS = get_cidrs(MY_CITIES)
print(MY_CITIES_CIDRS)
for city, cidr in MY_CITIES_CIDRS.items():
    for group_id in MY_GROUP_IDS:
        for from_to_ports in MY_FROM_TO_PORTS:
            add_loc_cidr_sg(city, cidr, group_id, from_to_ports)
            #del_loc_cidr_sg(city, cidr, group_id, from_to_ports)
