#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

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

OFFICE_CITIES_CIDRS = get_cidrs(MY_CITIES)
