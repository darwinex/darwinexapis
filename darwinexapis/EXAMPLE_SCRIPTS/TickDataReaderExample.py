# Let's make some imports:
import os, pprint
import pandas as pd

# Import the different classes:
from darwinexapis.API.TickDataAPI.DWX_TickData_Reader_API import DWX_TickData_Reader_API

# Reader:
bid_file_pkl = os.path.expandvars('${HOME}/Desktop/darwinexapis/darwinexapis/EXAMPLE_DATA/WS30_BID_2018-10-01_23.pkl')
ask_file_pkl = os.path.expandvars('${HOME}/Desktop/darwinexapis/darwinexapis/EXAMPLE_DATA/WS30_ASK_2018-10-01_23.pkl')
path_to_save = os.path.expandvars('${HOME}/Desktop/darwinexapis/darwinexapis/EXAMPLE_DATA/')

# Generate the object: 
READER = DWX_TickData_Reader_API(_bids_file=bid_file_pkl, 
                                 _asks_file=ask_file_pkl)

# Generate the dataframe: 
readed_dataframe = READER._get_symbol_as_dataframe_(_convert_epochs=True,
                                                    _check_integrity=True,
                                                    _calc_spread=True,
                                                    _reindex=['ask_price', 'bid_price', 'spread'],
                                                    _precision='tick')

# Save it:                                                                                                    
READER._save_df_to_csv(readed_dataframe, which_path=path_to_save)