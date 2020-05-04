DARWIN Data Analytics API
=============================================

In this API you will find many methods that will allow you to research all the **Dαrwin** universe,
taking the data from the **Dαrwin FTP server** and being able to analyze it in memory or in raw files.

Prerequisites
=============

    * Python **v3.6+**
    * FTP access to the raw **Dαrwin** data repository. To request it, please visit: `Darwin Data <https://www.darwinex.com/data/darwin-data>`_
    * Once obtained, please place your credentials inside **FTP_DARWIN_Access_Credentials.cfg** where the contents of the file should be:

.. code-block:: python

    username=YOUR-DARWINEX-USERNAME
    password=YOUR-DARWIN-DATA-FTP-PASSWORD
    server=darwindata.darwinex.com
    port=21

Example Usage & Tutorials
=========================

.. code-block:: python

    # Do some imports:
    import os, pandas as pd

    # Import the class:
    from darwinexapis.API.DarwinDataAnalyticsAPI.DWX_Data_Analytics_API import DWX_Darwin_Data_Analytics_API

    # Create the object:
    CONFIG_PATH = os.path.expandvars('${HOME}/FTP_DARWIN_Access_Credentials.cfg')
    ANALYZER = DWX_DARWIN_DATA_ANALYTICS_API(config=CONFIG_PATH)

    # Download data of certain analytics variable:
    dataFrameReturned = ANALYZER.get_analytics(darwin='LVS', data_type='RETURN_DIVERGENCE')
    ANALYZER.save_data_to_csv(dataFrameReturned, 
                              which_path=os.path.expandvars('${HOME}/darwinexapis/EXAMPLE_DATA/'), 
                              filename='LVS_AVG_LEVERAGE')
    print(dataFrameReturned)

    # Get quote date for DARWINs:
    # This call will get all the data and will take some time to execute.
    quotes = ANALYZER.get_quotes_from_ftp(darwin='PLF',
                                          suffix='4.1',
                                          monthly=False, # If False, month/year used > If True ALL data
                                          month='01',
                                          year='2019')
    ANALYZER.save_data_to_csv(quotes, 
                              which_path=os.path.expandvars('${HOME}/darwinexapis/EXAMPLE_DATA/'), 
                              filename='LVS_Quotes')
    print(quotes.head()) 

YouTube Playlist
================

`Click here to watch the dedicated YouTube Playlist <https://www.youtube.com/playlist?list=PLv-cA-4O3y971GdF958WoidF3HISpAiTf>`_
