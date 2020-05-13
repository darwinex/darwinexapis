# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 17:24:20 2018
Script: dwx_tickdata_download.py (Python 3)
--
Downloads tick data from the Darwinex tick data server. This code demonstrates
how to download data for one specific date/hour combination, but can be 
extended easily to downloading entire assets over user-specified start/end 
datetime ranges.
Requirements: Your Darwinex FTP credentials.
Result: Dictionary of pandas DataFrame objects by date/hour.
        (columns: float([ask, size]), index: millisecond timestamp)
        
Example code:
    > td = DWX_Tick_Data(dwx_ftp_user='very_secure_username', 
                         dwx_ftp_pass='extremely_secure_password',
                         dwx_ftp_hostname='mystery_ftp.server.com', 
                         dwx_ftp_port=21)
    
    > td._download_one_hour_data_ask(_asset='EURNOK', _date='2018-10-22', _hour='00')
    
    > td._asset_db['EURNOK-2018-10-22-00']
    
                                           ask       size
     2018-10-22 00:00:07.097000+00:00  9.47202  1000000.0
     2018-10-22 00:00:07.449000+00:00  9.47188   750000.0
     2018-10-22 00:01:08.123000+00:00  9.47201   250000.0
     2018-10-22 00:01:10.576000+00:00  9.47202  1000000.0
                                  ...        ...
@author: Darwinex Labs
@twitter: https://twitter.com/darwinexlabs
@web: http://blog.darwinex.com/category/labs
"""

# Do some imports:
from ftplib import FTP 
from io import BytesIO
import pandas as pd
import gzip, os
from datetime import timedelta, date, datetime

import logging
logger = logging.getLogger()

class DWX_TickData_Downloader_API(object):
    
    def __init__(self, dwx_ftp_user, dwx_ftp_pass, dwx_ftp_hostname, dwx_ftp_port):
        
        # Dictionary DB to hold dictionary objects in FX/Hour format
        self._asset_db = {}
        
        self._ftpObj = FTP(dwx_ftp_hostname)                            
        self._ftpObj.login(dwx_ftp_user, dwx_ftp_pass)   

        self._virtual_dl = None
        
    ############################## DOWNLOAD DATA ##############################
    
    def _download_one_hour_data_ask(self, _asset='EURUSD', _date='2017-10-01', _hour='22', _ftp_loc_format='{}/{}_ASK_{}_{}.log.gz', _verbose=False):

        # Function: Downloads and stored currency tick data from Darwinex FTP
        #           Server. Object stores data in a dictionary, keys being of the
        #           format: CURRENCYPAIR-YYYY-MM-DD-HH
        
        _file = _ftp_loc_format.format(_asset, _asset, _date, _hour)
        self._file_name_csv = f'{_asset}_ASK_{_date}_{_hour}.csv'
        _key = '{}-{}-{}'.format(_asset, _date, _hour)
        
        self._virtual_dl = BytesIO()
        
        if _verbose is True:
            logger.warning("\n[INFO] Retrieving file \'{}\' from Darwinex Tick Data Server..".format(_file))
        
        try:
            self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)

            self._virtual_dl.seek(0)
            _log = gzip.open(self._virtual_dl)
                
            # Get bytes into local DB as list of lists
            self._asset_db[_key] = [line.strip().decode().split(',') for line in _log]
            
            # Construct DataFrame
            _temp = self._asset_db[_key]
            self._asset_db[_key] = pd.DataFrame({'ask': [l[1] for l in _temp],
                                'size': [l[2] for l in _temp]}, 
                                index=[pd.to_datetime(l[0], unit='ms', utc=True) for l in _temp])
            
            # Sanitize types
            self._asset_db[_key] = self._asset_db[_key].astype(float)
            
            if _verbose is True:
                logger.warning('\n[SUCCESS] {} tick data for {} (hour {}) stored in self._asset_db dict object.\n'.format(_asset, _date, _hour))

            # Close the file
            self._virtual_dl.close()

            # Return the data:
            return self._return_pandas_dataframe_()
        
        # Case: if file not found
        except Exception as ex:

            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            logger.warning(_msg)

    def _download_one_hour_data_bid(self, _asset='EURUSD', _date='2017-10-01', _hour='22', _ftp_loc_format='{}/{}_BID_{}_{}.log.gz', _verbose=False):

        # Function: Downloads and stored currency tick data from Darwinex FTP
        #           Server. Object stores data in a dictionary, keys being of the
        #           format: CURRENCYPAIR-YYYY-MM-DD-HH
        
        _file = _ftp_loc_format.format(_asset, _asset, _date, _hour)
        self._file_name_csv = f'{_asset}_BID_{_date}_{_hour}.csv'
        _key = '{}-{}-{}'.format(_asset, _date, _hour)
        
        self._virtual_dl = BytesIO()
        
        if _verbose is True:
            logger.warning("\n[INFO] Retrieving file \'{}\' from Darwinex Tick Data Server..".format(_file))
        
        try:
            self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)
                
            self._virtual_dl.seek(0)
            _log = gzip.open(self._virtual_dl)
                
            # Get bytes into local DB as list of lists
            self._asset_db[_key] = [line.strip().decode().split(',') for line in _log]
            
            # Construct DataFrame
            _temp = self._asset_db[_key]
            self._asset_db[_key] = pd.DataFrame({'bid': [l[1] for l in _temp],
                                'size': [l[2] for l in _temp]}, 
                                index=[pd.to_datetime(l[0], unit='ms', utc=True) for l in _temp])
            
            # Sanitize types
            self._asset_db[_key] = self._asset_db[_key].astype(float)
            
            if _verbose is True:
                logger.warning('\n[SUCCESS] {} tick data for {} (hour {}) stored in self._asset_db dict object.\n'.format(_asset, _date, _hour))

            # Close the file
            self._virtual_dl.close()

            # Return the data:
            return self._return_pandas_dataframe_()
        
        # Case: if file not found
        except Exception as ex:

            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            logger.warning(_msg)

    ##########################################################

    def _download_one_day_data_ask(self, _asset='EURUSD', _date='2017-10-01', _ftp_loc_format='{}/{}_ASK_{}_{}.log.gz', _verbose=False):

        # This method will download data for one day, all hours:
        
        full_dataframe = pd.DataFrame(columns=['ask', 'size'])

        # You can change the range parameter to alter the hours of download.
        # The final part of the csv name will have the last hour of data that was requested.
        for _hour in range(0, 24):

            _hour = str(_hour).zfill(2)

            _file = _ftp_loc_format.format(_asset, _asset, _date, _hour)
            self._file_name_csv = f'{_asset}_ASK_{_date}_{_hour}.csv'
            _key = '{}-{}-{}'.format(_asset, _date, _hour)
        
            self._virtual_dl = BytesIO()
        
            if _verbose is True:
                logger.warning("\n[INFO] Retrieving file \'{}\' from Darwinex Tick Data Server..".format(_file))
        
            try:
                self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)
                
                self._virtual_dl.seek(0)
                _log = gzip.open(self._virtual_dl)
                
                # Get bytes into local DB as list of lists
                self._asset_db[_key] = [line.strip().decode().split(',') for line in _log]
            
                # Construct DataFrame
                _temp = self._asset_db[_key]
                self._asset_db[_key] = pd.DataFrame({'ask': [l[1] for l in _temp],
                                    'size': [l[2] for l in _temp]}, 
                                    index=[pd.to_datetime(l[0], unit='ms', utc=True) for l in _temp])
            
                # Sanitize types
                self._asset_db[_key] = self._asset_db[_key].astype(float)
            
                if _verbose is True:
                    logger.warning('\n[SUCCESS] {} tick data for {} (hour {}) stored in self._asset_db dict object.\n'.format(_asset, _date, _hour))

                # Return the data:
                hour_df_data = self._return_pandas_dataframe_()
                self._asset_db = {}

                # Concat the data:
                full_dataframe = full_dataframe.append(hour_df_data)

                # Close the file
                self._virtual_dl.close()
        
            # Case: if file not found
            except Exception as ex:

                _exstr = "Exception Type {0}. Args:\n{1!r}"
                _msg = _exstr.format(type(ex).__name__, ex.args)
                logger.warning(_msg)
                logger.warning('[ERROR] - Check if the date provided is a valid trading day')

        # Return the data finally:
        self._asset_db = {}
        return full_dataframe

    def _download_one_day_data_bid(self, _asset='EURUSD', _date='2017-10-01', _ftp_loc_format='{}/{}_BID_{}_{}.log.gz', _verbose=False):

        # This method will download data for one day, all hours:
        
        full_dataframe = pd.DataFrame(columns=['bid', 'size'])

        # You can change the range parameter to alter the hours of download.
        # The final part of the csv name will have the last hour of data that was requested.
        for _hour in range(0, 24):

            _hour = str(_hour).zfill(2)

            _file = _ftp_loc_format.format(_asset, _asset, _date, _hour)
            self._file_name_csv = f'{_asset}_BID_{_date}_{_hour}.csv'
            _key = '{}-{}-{}'.format(_asset, _date, _hour)
        
            self._virtual_dl = BytesIO()
        
            if _verbose is True:
                logger.warning("\n[INFO] Retrieving file \'{}\' from Darwinex Tick Data Server..".format(_file))
        
            try:
                self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)
                
                self._virtual_dl.seek(0)
                _log = gzip.open(self._virtual_dl)
                
                # Get bytes into local DB as list of lists
                self._asset_db[_key] = [line.strip().decode().split(',') for line in _log]
            
                # Construct DataFrame
                _temp = self._asset_db[_key]
                self._asset_db[_key] = pd.DataFrame({'bid': [l[1] for l in _temp],
                                    'size': [l[2] for l in _temp]}, 
                                    index=[pd.to_datetime(l[0], unit='ms', utc=True) for l in _temp])
            
                # Sanitize types
                self._asset_db[_key] = self._asset_db[_key].astype(float)
            
                if _verbose is True:
                    logger.warning('\n[SUCCESS] {} tick data for {} (hour {}) stored in self._asset_db dict object.\n'.format(_asset, _date, _hour))

                # Return the data:
                hour_df_data = self._return_pandas_dataframe_()
                self._asset_db = {}

                # Concat the data:
                full_dataframe = full_dataframe.append(hour_df_data)

                # Close the file
                self._virtual_dl.close()
        
            # Case: if file not found
            except Exception as ex:

                _exstr = "Exception Type {0}. Args:\n{1!r}"
                _msg = _exstr.format(type(ex).__name__, ex.args)
                logger.warning(_msg)
                logger.warning('[ERROR] - Check if the date provided is a valid trading day')

        # Return the data finally:
        self._asset_db = {}
        return full_dataframe

    ##########################################################

    def date_range(self, start_date, end_date):

        # Generator method to yield the following date:

        # Parse the entry strings to date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        for each_day in range(int((end_date - start_date).days)):
            yield start_date + timedelta(each_day)

    def _download_month_data_ask(self, _asset='EURUSD', _start_date='2017-10-01', _end_date='2017-11-01', 
                                 _ftp_loc_format='{}/{}_ASK_{}_{}.log.gz', _verbose=False):

        # This method will download data for one month, all days available and all hours:
        
        full_dataframe = pd.DataFrame(columns=['ask', 'size'])

        # NOTE: For consistency with the built-in range() function this iteration stops before reaching the end_date. 
        # So for inclusive iteration use the next day, as you would with range()

        for _date in self.date_range(_start_date, _end_date):

            # Parse the date to string:
            _date = _date.strftime("%Y-%m-%d")

            # You can change the range parameter to alter the hours of download.
            # The final part of the csv name will have the last hour of data that was requested and last date.
            for _hour in range(0, 24):

                _hour = str(_hour).zfill(2)

                _file = _ftp_loc_format.format(_asset, _asset, _date, _hour)
                self._file_name_csv = f'{_asset}_ASK_{_date}_{_hour}.csv'
                _key = '{}-{}-{}'.format(_asset, _date, _hour)
        
                self._virtual_dl = BytesIO()
        
                if _verbose is True:
                    logger.warning("\n[INFO] Retrieving file \'{}\' from Darwinex Tick Data Server..".format(_file))
        
                try:
                    self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)
                
                    self._virtual_dl.seek(0)
                    _log = gzip.open(self._virtual_dl)
                
                    # Get bytes into local DB as list of lists
                    self._asset_db[_key] = [line.strip().decode().split(',') for line in _log]
            
                    # Construct DataFrame
                    _temp = self._asset_db[_key]
                    self._asset_db[_key] = pd.DataFrame({'ask': [l[1] for l in _temp],
                                        'size': [l[2] for l in _temp]}, 
                                        index=[pd.to_datetime(l[0], unit='ms', utc=True) for l in _temp])
            
                    # Sanitize types
                    self._asset_db[_key] = self._asset_db[_key].astype(float)
            
                    if _verbose is True:
                        logger.warning('\n[SUCCESS] {} tick data for {} (hour {}) stored in self._asset_db dict object.\n'.format(_asset, _date, _hour))

                    # Return the data:
                    hour_df_data = self._return_pandas_dataframe_()
                    self._asset_db = {}

                    # Concat the data:
                    full_dataframe = full_dataframe.append(hour_df_data)

                    # Close the file
                    self._virtual_dl.close()
        
                # Case: if file not found
                except Exception as ex:

                    _exstr = "Exception Type {0}. Args:\n{1!r}"
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    logger.warning(_msg)
                    logger.warning('[ERROR] - Check if the date provided is a valid trading day')

        # Return the data finally:
        self._asset_db = {}
        return full_dataframe

    def _download_month_data_bid(self, _asset='EURUSD', _start_date='2017-10-01', _end_date='2017-11-01', 
                                 _ftp_loc_format='{}/{}_BID_{}_{}.log.gz', _verbose=False):

        # This method will download data for one month, all days available and all hours:
        
        full_dataframe = pd.DataFrame(columns=['bid', 'size'])

        # NOTE: For consistency with the built-in range() function this iteration stops before reaching the end_date. 
        # So for inclusive iteration use the next day, as you would with range()

        for _date in self.date_range(_start_date, _end_date):

            # Parse the date to string:
            _date = _date.strftime("%Y-%m-%d")

            # You can change the range parameter to alter the hours of download.
            # The final part of the csv name will have the last hour of data that was requested and last date.
            for _hour in range(0, 24):

                _hour = str(_hour).zfill(2)

                _file = _ftp_loc_format.format(_asset, _asset, _date, _hour)
                self._file_name_csv = f'{_asset}_BID_{_date}_{_hour}.csv'
                _key = '{}-{}-{}'.format(_asset, _date, _hour)
        
                self._virtual_dl = BytesIO()
        
                if _verbose is True:
                    logger.warning("\n[INFO] Retrieving file \'{}\' from Darwinex Tick Data Server..".format(_file))
        
                try:
                    self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)
                
                    self._virtual_dl.seek(0)
                    _log = gzip.open(self._virtual_dl)
                
                    # Get bytes into local DB as list of lists
                    self._asset_db[_key] = [line.strip().decode().split(',') for line in _log]
            
                    # Construct DataFrame
                    _temp = self._asset_db[_key]
                    self._asset_db[_key] = pd.DataFrame({'bid': [l[1] for l in _temp],
                                        'size': [l[2] for l in _temp]}, 
                                        index=[pd.to_datetime(l[0], unit='ms', utc=True) for l in _temp])
            
                    # Sanitize types
                    self._asset_db[_key] = self._asset_db[_key].astype(float)
            
                    if _verbose is True:
                        logger.warning('\n[SUCCESS] {} tick data for {} (hour {}) stored in self._asset_db dict object.\n'.format(_asset, _date, _hour))

                    # Return the data:
                    hour_df_data = self._return_pandas_dataframe_()
                    self._asset_db = {}

                    # Concat the data:
                    full_dataframe = full_dataframe.append(hour_df_data)

                    # Close the file
                    self._virtual_dl.close()
        
                # Case: if file not found
                except Exception as ex:

                    _exstr = "Exception Type {0}. Args:\n{1!r}"
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    logger.warning(_msg)
                    logger.warning('[ERROR] - Check if the date provided is a valid trading day')

        # Return the data finally:
        self._asset_db = {}
        return full_dataframe

    ##########################################################

    def _return_pandas_dataframe_(self):

        # Transform the data to a pandas dataframe:
        dataframe_values = self._asset_db.get(list(self._asset_db.keys())[0])

        # Return it:
        self._asset_db = {}
        return dataframe_values

    ##########################################################

    def _save_df_to_csv(self, dataframe_to_save, which_path=None):

        # Save:
        if which_path:
            # It will save the data to the specified path:
            dataframe_to_save.to_csv(which_path + self._file_name_csv)
        else:
            # It will save the data in the working directory:
            dataframe_to_save.to_csv(self._file_name_csv)

    def _save_df_to_pickle(self, dataframe_to_save, which_path=None):

        # Save:
        if which_path:
            # It will save the data to the specified path:
            dataframe_to_save.to_pickle(which_path + self._file_name_csv.split('.')[0] + '.pkl')
        else:
            # It will save the data in the working directory:
            dataframe_to_save.to_pickle(self._file_name_csv.split('.')[0] + '.pkl')

    def _save_df_to_hdf(self, dataframe_to_save, which_path=None):

        # Save:
        if which_path:
            # It will save the data to the specified path:
            dataframe_to_save.to_hdf(which_path + self._file_name_csv.split('.')[0] + '.h5', key='df', mode='w')
        else:
            # It will save the data in the working directory:
            dataframe_to_save.to_csv(self._file_name_csv.split('.')[0] + '.h5')