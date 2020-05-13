
import json, base64, requests, pprint
import logging
logger = logging.getLogger()

class DWX_OAuth2():
    
    def __init__(self):
        
        pass
    
    ##########################################################################

    def _get_tokens_(self, token_url='https://api.darwinex.com/token'):

        # Refs: https://auth0.com/docs/tokens/guides/use-refresh-tokens
        # https://help.darwinex.com/api-walkthrough
        # https://help.darwinex.com/
    
        header_data = {'client_id': '', ## Consumer key in the Darwinex web
                       'client_secret': ''} ## Consumer secret in the Darwinex web

        data = {'grant_type': 'refresh_token',
                'refresh_token': ''}
    
        headers = {'Authorization': 'Basic {}'.format(base64.b64encode(bytes('{}:{}'.format(header_data['client_id'], header_data['client_secret']).encode('utf-8'))).decode('utf-8'))}

        try:
            _response = requests.post(token_url, headers=headers, data=data, verify=True, allow_redirects=False)
            
            logger.warning('[KERNEL] Access & Refresh Tokens Retrieved Successfully')
            
            response_json = json.loads(_response.text)
            #return response_json
            return response_json['access_token'], response_json['expires_in'], response_json['refresh_token']
            
        except Exception as ex:
            logger.warning('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            return None
    
    ##########################################################################

if __name__ == "__main__":

    '''Example response:
    
    {'access_token': '63ca7671-cf30-3e4d-a13e-0ae78781183d73',
     'expires_in': 3600,
     'id_token': '...',
     'refresh_token': '827c785e-f5ed-33bc-87e5-fb91354fe1f80',
     'scope': 'openid',
     'token_type': 'Bearer'}'''

    a = DWX_OAuth2()
    tokens = a._get_tokens_()

    pprint.pprint(tokens)