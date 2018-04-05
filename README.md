# What
Scrape Zscaler IP listing webpage and add/remove the cidrs to a list of security groups
It can be done by cities or continents


# Environment
pip install --requirement python_requirements.txt
*beautifulsoup4==4.6.0
*boto3==1.6.16
*bs4==0.0.1
*lxml==4.2.1
*requests==2.18.4

# How 
Modify PROFILE, GroupId, FromPort/ToPort and location/city lists in Zscaler_whatever.py and run it.
