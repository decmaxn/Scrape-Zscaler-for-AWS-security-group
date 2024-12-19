#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

# 定义城市列表
MY_CITIES = ['Toronto II', 'London III', 'Dallas I']
URL = "https://ips.zscaler.net/cenr"

# 获取网页内容
HTML = requests.get(URL)
BS = BeautifulSoup(HTML.content, "lxml")

# 获取城市CIDR的函数
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

# 获取办公室城市的CIDR
OFFICE_CITIES_CIDRS = get_cidrs(MY_CITIES)

# print(OFFICE_CITIES_CIDRS)