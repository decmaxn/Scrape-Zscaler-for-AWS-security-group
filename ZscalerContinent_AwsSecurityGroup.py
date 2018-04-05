#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import boto3
import sys
from botocore.exceptions import ClientError

PROFILE = "victor"
session = boto3.session.Session(profile_name=PROFILE)
ec2 = session.client('ec2')

my_from_to_ports = [[22,22],[3389,3389],[80,81]]
my_locations = ['africa','latinamerica']
my_group_ids = ['sg-03e95f6b','sg-5cbef537']

locations = ['europe','uscanada','africa','asia','latinamerica']
url = "https://ips.zscaler.net/cenr"

html = requests.get(url)
bs = BeautifulSoup(html.content,"lxml")

def get_cidrs(location):
        location_cidrs = []
        id = 'div_' + location
        div = bs.find('div', class_="hidden", id=id)
        location_cidrs = div.text.split()
        return(location_cidrs)


def add_loc_cidr_sg(location, group_id, from_to_ports):
    for location_cidr in get_cidrs(location):
        try:
            response = ec2.authorize_security_group_ingress(
                #DryRun=True,
                GroupId=group_id,
                IpPermissions=[{
                    'FromPort': from_to_ports[0],
                    'ToPort': from_to_ports[1],        
                    'IpProtocol':'tcp',
                    'IpRanges': [{
                        'CidrIp': location_cidr,
                        'Description': 'Zscaler ' + location
                    },]
                },]
            )
            print(response)
        except ClientError as e:
            print(e)


for location in my_locations:
    for group_id in my_group_ids:
        for from_to_ports in my_from_to_ports:
            add_loc_cidr_sg(location,group_id,from_to_ports)
