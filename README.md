# What
-   Scrape Zscaler IP listing webpage by cities or continents.
-   Create security groups, and add/remove the Zscaler/Incapsula Cidrs as rules
-   Modify existing security group with Zscaler and your costomized Cidrs as rules


# Environment
pip install --requirement python_requirements.txt
-   beautifulsoup4==4.6.0
-   boto3==1.6.16
-   bs4==0.0.1
-   lxml==4.2.1
-   requests==2.18.4

# How 
- Zscaler_whatever.py will scrape Zscaler web site to get list, modify location/city list and run.
- Others.py can be run by itself, also imported as module, modify PROFILE, VPC_Id, GroupId, FromPort/ToPort before run. 

# To Do
- python_requirements.txt update versions so all of them could be installed with python3
- ZscalerCity.py need to be updated to work with the latest Zscaler node range page
