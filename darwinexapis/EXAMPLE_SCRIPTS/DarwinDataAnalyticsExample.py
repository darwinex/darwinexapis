# Do some imports:
import os, pandas as pd

# Import the class:
from darwinexAPIs.API.DarwinDataAnalyticsAPI.DWX_Data_Analytics_API import DWX_Darwin_Data_Analytics_API

# Create the object:
CONFIG_PATH = os.path.expandvars('${HOME}/Desktop/darwinexAPIs/darwinexAPIs/API/DarwinDataAnalyticsAPI/FTP_DARWIN_Access_Credentials.cfg')
ANALYZER = DWX_Darwin_Data_Analytics_API(config=CONFIG_PATH)

# Download data of certain analytics variable:
dataFrameReturned = ANALYZER.get_analytics(darwin='LVS', data_type='RETURN_DIVERGENCE')
ANALYZER.save_data_to_csv(dataFrameReturned, which_path=os.path.expandvars('${HOME}/Desktop/darwinexAPIs/darwinexAPIs/EXAMPLE_DATA/'), filename='LVS_AVG_LEVERAGE')
print(dataFrameReturned)

# Get quote date for DARWINs:
# This call will get all the data and will take some time to execute.
quotes = ANALYZER.get_quotes_from_ftp(darwin='PLF',
                                      suffix='4.1',
                                      monthly=False, # If set to False, month/year used > If True ALL data available
                                      month='01',
                                      year='2019')
ANALYZER.save_data_to_csv(quotes, which_path=os.path.expandvars('${HOME}/Desktop/darwinexAPIs/darwinexAPIs/EXAMPLE_DATA/'), filename='LVS_Quotes')
print(quotes.head())                                      