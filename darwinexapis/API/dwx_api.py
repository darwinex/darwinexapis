# -*- coding: utf-8 -*-
"""
    DWX_API - Superclass for all sub-APIs
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 29, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

# Do some imports:
import os, requests, json, time
from darwinexapis.API.DWX_API_Auth import DWX_API_AUTHENTICATION
import logging
logger = logging.getLogger()

class Decorators():

    @staticmethod
    def refreshTokenDecorator_APIs(func_to_be_decorated):

        '''Example use > put the decorator upfront the method that will make request:

        @refreshTokenDecorator
        def someRequest(self):
            # make our API request
            pass'''

        # The function that is used to check the TOKEN and refresh if necessary
        def wrapper_of_the_func(self, *args, **kwargs):

            # If the time is greater that the time + the expires in > issue refresh:
            if time.time() > self.AUTHENTICATION.expires_in:

                logger.warning('\n[DECORATOR] - The expiration time has REACHED > ¡Generate TOKENS!')
                # Generate new credentials:
                self.AUTHENTICATION._get_access_refresh_tokens_wrapper()

                # Call the function after getting new creds:
                # NOTE: no need to call the function here > The decorator will call it after.
                #self._Call_API_(*args, **kwargs)
                
            else:
                logger.warning('\n[DECORATOR] - The expiration time has NOT reached yet > Continue...')

            return func_to_be_decorated(self, *args,**kwargs)

        # Return the decorated function > Something like: <function refreshTokenDecorator.<locals>.wrapper at 0x7f3c5dfd42f0>
        return wrapper_of_the_func

class DWX_API(object):
    
    def __init__(self,
                 _auth_creds='',
                 _api_url='https://api.darwinex.com',
                 _api_name='darwininfo',
                 _version=1.5,
                 _demo=False):
        
        # Create the auth object:
        self.AUTHENTICATION = DWX_API_AUTHENTICATION(_auth_creds)
        
        # Construct main production url for tagging endpoints
        self._url = '{}/{}/{}'.format(_api_url, _api_name, _version)

    def _construct_auth_post_headers(self):

        # Will be called after the new access token is retrieved.

        # Construct authorization header for all requests
        self._auth_headers = {'Authorization': f'Bearer {self.AUTHENTICATION._auth_creds["access_token"]}'}
        
        # Construct headers for POST requests
        self._post_headers = {**self._auth_headers,
                              **{'Content-type':'application/json',
                                 'Accept':'application/json'}}

    @Decorators.refreshTokenDecorator_APIs
    def _Call_API_(self, _endpoint, _type, _data, _json=True, _stream=False):
        
        """Call any endpoint provided in the Darwinex API documentation, and get JSON."""

        # Construct the headers:
        self._construct_auth_post_headers()

        if _type not in ['GET','POST','PUT', 'DELETE']:
            logger.warning('Bad request type')
            return None
        
        try:
            
            if _type == 'GET':
                _ret = requests.get(self._url + _endpoint,
                                    headers=self._auth_headers,
                                    verify=True)
                logger.warning(f'**** FULL URL ENDPOINT ****: {_ret.url}')
            elif _type == 'PUT':
                _ret = requests.put(self._url + _endpoint,
                                    headers=self._post_headers,
                                    data=_data,
                                    verify=True)
                logger.warning(f'**** FULL URL ENDPOINT ****: {_ret.url}')
            elif _type == 'DELETE':
                _ret = requests.delete(self._url + _endpoint,
                                       headers=self._auth_headers,
                                       #data=_data,
                                       verify=True)
                logger.warning(f'**** FULL URL ENDPOINT ****: {_ret.url}')
            else:
                if len(_data) == 0:
                    logger.warning('Data is empty..')
                    return None
                
                # For DARWIN Quotes API
                if _stream:
                    
                    # Add POST header for streaming quotes        
                    self._post_headers['connection'] = 'keep-alive'
                    return requests.Request('POST',
                                           self._url + _endpoint,
                                           headers=self._post_headers,
                                           data=_data)
                else:
                    _ret = requests.post(self._url + _endpoint,
                                         data=_data,
                                         headers = self._post_headers,
                                         verify=True)
        
            # Log the response:
            logger.warning(_ret)
            logger.warning(_ret.text)

            # Check for JSON conversion:
            if _json:
                return _ret.json()
            else:
                return _ret
        
        except Exception as ex:

            # When the response is not converted to JSON, we will enter here.
            # When invalid credentials, the response is not JSON, so we will enter here.

            logger.warning('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            logger.warning(f'Response request code: {_ret.status_code}')
            logger.warning(f'Response request URL: {_ret.url}')
            logger.warning(f'Response request Data: {_ret.text}')

            # Return the response to handle it:
            return _ret.text
            
    ##########################################################################
