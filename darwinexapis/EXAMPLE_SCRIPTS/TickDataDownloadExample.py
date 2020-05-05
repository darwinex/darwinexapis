# Let's make some imports:
import os, pprint
import pandas as pd

# Import the different classes:
from darwinexapis.API.TickDataAPI.DWX_TickData_Downloader_API import DWX_TickData_Downloader_API

# Let's create the access token variable:

FTP_CRED = {"username": "your_alpha_username",
            "password": "your_alpha_password",
            "server": "tickdata.darwinex.com"}

# Downloader:
# Try other assets like: GDAXIm, SPN35, XAUUSD... > Watch out with the available dates!
DOWNLOADER = DWX_TickData_Downloader_API(dwx_ftp_user=FTP_CRED['username'], 
                                         dwx_ftp_pass=FTP_CRED['password'],
                                         dwx_ftp_hostname=FTP_CRED['server'],
                                         dwx_ftp_port=FTP_CRED['port'])

# Create the path you wish to save the data:                                         
path_to_save = os.path.expandvars('${HOME}/Desktop/darwinexapis/darwinexapis/EXAMPLE_DATA/')

###################################################

# One hour data (be sure to put the hours with two characters > 0 == 00, 5 == 05, 23 ==23):
bid_hour_data = DOWNLOADER._download_one_hour_data_bid(_asset='WS30', 
                                                       _date='2018-10-01', 
                                                       _hour='22',
                                                       _verbose=True)
DOWNLOADER._save_df_to_csv(bid_hour_data, which_path=path_to_save)                                                       
DOWNLOADER._save_df_to_pickle(bid_hour_data, which_path=path_to_save)

ask_hour_data = DOWNLOADER._download_one_hour_data_ask(_asset='WS30', 
                                                       _date='2018-10-01', 
                                                       _hour='22',
                                                       _verbose=True)
DOWNLOADER._save_df_to_csv(ask_hour_data, which_path=path_to_save)                                                       
DOWNLOADER._save_df_to_pickle(ask_hour_data, which_path=path_to_save)

###################################################

# One day data (be sure to also put the dates with two characters):
bid_day_data = DOWNLOADER._download_one_day_data_bid(_asset='WS30', 
                                                     _date='2018-10-01',
                                                     _verbose=True)
DOWNLOADER._save_df_to_csv(bid_day_data, which_path=path_to_save)                                                     
DOWNLOADER._save_df_to_pickle(bid_day_data, which_path=path_to_save)                                                     

ask_day_data = DOWNLOADER._download_one_day_data_ask(_asset='WS30', 
                                                     _date='2018-10-01',
                                                     _verbose=True)
DOWNLOADER._save_df_to_csv(ask_day_data, which_path=path_to_save)                                                     
DOWNLOADER._save_df_to_pickle(ask_day_data, which_path=path_to_save)                                                     

###################################################

# Between two dates data:
bid_date_data = DOWNLOADER._download_month_data_bid(_asset='WS30', 
                                                    _start_date='2018-10-01', 
                                                    _end_date='2018-10-04', 
                                                    _verbose=True)
DOWNLOADER._save_df_to_csv(bid_date_data, which_path=path_to_save)                                                    
DOWNLOADER._save_df_to_pickle(bid_date_data, which_path=path_to_save)                                                    

ask_date_data = DOWNLOADER._download_month_data_ask(_asset='WS30', 
                                                    _start_date='2018-10-01', 
                                                    _end_date='2018-10-04', 
                                                    _verbose=True)
DOWNLOADER._save_df_to_csv(ask_date_data, which_path=path_to_save)                                                    
DOWNLOADER._save_df_to_pickle(ask_date_data, which_path=path_to_save)                                                    
