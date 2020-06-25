# Do some imports:
import os, pandas as pd
import logging
logger = logging.getLogger()

# Import the class:
from darwinexapis.API.DarwinDataAnalyticsAPI.DWX_Data_Analytics_API import DWX_Darwin_Data_Analytics_API

# Create the object:
FTP_CRED = {"username": "your_alpha_username",
            "password": "your_alpha_password",
            "server": "darwindata.darwinex.com",
            "port": 21}

ANALYZER = DWX_Darwin_Data_Analytics_API(dwx_ftp_user=FTP_CRED['username'], 
                                         dwx_ftp_pass=FTP_CRED['password'],
                                         dwx_ftp_hostname=FTP_CRED['server'],
                                         dwx_ftp_port=FTP_CRED['port'])

# Download data of certain analytics variable:
dataFrameReturned = ANALYZER.get_analytics(darwin='LVS', data_type='RETURN_DIVERGENCE')
ANALYZER.save_data_to_csv(dataFrameReturned, which_path=os.path.expandvars('${HOME}/Desktop/darwinexapis/darwinexapis/EXAMPLE_DATA/'), filename='LVS_AVG_LEVERAGE')
logger.warning(dataFrameReturned)

# Get quote date for DARWINs:
# This call will get all the data and will take some time to execute.
quotes = ANALYZER.get_quotes_from_ftp(darwin='PLF',
                                      suffix='3.1',
                                      monthly=False, # If set to False, month/year used > If True ALL data available
                                      month='05',
                                      year='2018', 
                                      former_or_new='former')
ANALYZER.save_data_to_csv(quotes, which_path=os.path.expandvars('${HOME}/Desktop/darwinexapis/darwinexapis/EXAMPLE_DATA/'), filename='PLF_Quotes')
logger.warning(quotes.head())                                      