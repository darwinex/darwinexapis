### Do some imports:
import os, pprint, json, base64, requests, time
import pandas as pd
import logging
logger = logging.getLogger()

class DWX_API_AUTHENTICATION(object):

    '''This class will handle the neccesary work for refreshing the access
    token. The post response back will be like (access token and refresh token will change):
    
    {'access_token': '63ca7671-cf30-3e4d-a13e-0ae789183d73',
     'expires_in': 3600,
     'id_token': '...eyJ4NXQi...',
     'refresh_token': '827c785e-f5ed-33bc-87e5-fb9854fe1f80',
     'scope': 'openid',
     'token_type': 'Bearer'}'''

    def __init__(self, _auth_creds):

        '''_auth_creds is a dictionary with all the credentials:

        Ex:

        {'access_token': '63ca7671-cf30-3e4d-a13e-0ae789183d73',
         'consumer_key': '827c785e-f5ed-33bc-87e5-fb9854',
         'consumer_secret': '827c785e-f5ed-33bc-87e5-fb9854',
         'refresh_token': '827c785e-f5ed-33bc-87e5-fb9854fe1f80'}'''
 
        logger.warning(f'[INIT] - Creating AUTH creds...')
        self._auth_creds = _auth_creds

        # Put 60 seconds to request the new one and start from there:
        self.expires_in = time.time() + 60
        logger.warning(f'[INIT] - Access token will be created again at {self.expires_in} UNIX timestamp')
 
    def _get_access_refresh_tokens_wrapper(self):

        # Wrap the get tokens method to be called:
        try:
            self.access_token, self.expires_in, self.refresh_token = self._get_access_refresh_tokens_(self._auth_creds['consumer_key'], 
                                                                                                      self._auth_creds['consumer_secret'], 
                                                                                                      self._auth_creds['refresh_token'])

            # The access token is None > Raise exception.
            if self.access_token is None:

                raise Exception("[REFRESH_INIT] - Request for access token failed > No access_token returned in the response")

            #logger.warning(f'[REFRESH] - New access_token > {self.access_token}')
            logger.warning(f'[REFRESH] - New expires_in > {self.expires_in}')
            #logger.warning(f'[REFRESH] - New refresh_token > {self.refresh_token}')

            logger.warning("[REFRESH_INIT] - Will sleep for some secs...")
            time.sleep(3)

        except Exception as ex:
            logger.warning(ex)

        else:
            # It is useful for code that must be executed if the try clause does not raise an exception.
            logger.warning("[REFRESH_ELSE] - Will RESET the expires_in variable...")
            self.expires_in = time.time() + (self.expires_in - 300)

            # Put new credentials:
            logger.warning("[REFRESH_ELSE] - Will add the new access_token and refresh_token to the dictionary")
            self._auth_creds['access_token'] = self.access_token
            self._auth_creds['refresh_token'] = self.refresh_token
            #logger.warning(f"[REFRESH_ELSE] - NEW CREDS: {self._auth_creds}")

    def _get_access_refresh_tokens_(self, client_id, client_secret, refresh_token, token_url='https://api.darwinex.com/token'):

        # Refs: https://auth0.com/docs/tokens/guides/use-refresh-tokens
        # Refs: https://help.darwinex.com/api-walkthrough
        # Refs: https://help.darwinex.com/
    
        header_data = {'client_id': client_id, # Consumer key in the Darwinex web
                       'client_secret': client_secret} # Consumer secret in the Darwinex web

        data = {'grant_type': 'refresh_token',
                'refresh_token': refresh_token}
    
        headers = {'Authorization': 'Basic {}'.format(base64.b64encode(bytes('{}:{}'.format(header_data['client_id'], header_data['client_secret']).encode('utf-8'))).decode('utf-8'))}

        try:
            _response = requests.post(token_url, headers=headers, data=data, verify=True, allow_redirects=False)
            
            # Optional: Raise an exception if a request is unsuccessful:
            _response.raise_for_status()

            logger.warning('[GET_TOKENS] - Access & Refresh Tokens Retrieved Successfully')
            
            response_json = json.loads(_response.text)
            #logger.warning(f'[GET_TOKENS] - RETURNED RESPONSE IN TEXT: {response_json}')
            return response_json['access_token'], response_json['expires_in'], response_json['refresh_token']
            
        except Exception as ex:

            logger.warning('[GET_TOKENS] - Access & Refresh Tokens ***NOT*** Retrieved Successfully')
            logger.warning('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            return None, None, None
