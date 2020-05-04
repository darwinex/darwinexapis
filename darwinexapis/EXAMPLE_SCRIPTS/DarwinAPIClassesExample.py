### Do some imports:
import os, pprint
import pandas as pd

### Import the different classes:
from darwinexapis.API.InfoAPI.DWX_Info_API import DWX_Info_API
from darwinexapis.API.InvestorAccountInfoAPI.DWX_AccInfo_API import DWX_AccInfo_API
from darwinexapis.API.QuotesAPI.DWX_Quotes_API import DWX_Quotes_API
from darwinexapis.API.TradingAPI.DWX_Trading_API import DWX_Trading_API
from darwinexapis.API.WebSocketAPI.DWX_WebSocket_API import DWX_WebSocket_API

### Let's create the access token variable:
AUTH_CREDS = {'access_token': 'YOUR_ALPHA_TOKEN',
              'consumer_key': 'YOUR_ALPHA_TOKEN',
              'consumer_secret': 'YOUR_ALPHA_TOKEN',
              'refresh_token': 'YOUR_ALPHA_TOKEN'}

### Let's instantiate some objects:
#darwinexInfo = DWX_Info_API(AUTH_CREDS, _version=2.0, _demo=True)
#darwinexInvestorAcc = DWX_AccInfo_API(AUTH_CREDS, _version=2.0, _demo=True)
#darwinexQuotes = DWX_Quotes_API(AUTH_CREDS, _version=1.0)
#darwinexTrading = DWX_Trading_API(AUTH_CREDS, _version=1.1, _demo=True)
darwinexWebSocket = DWX_WebSocket_API(AUTH_CREDS, _version=0.0)

### DWX_Info_API:
#darwinUniverse = darwinexInfo._Get_DARWIN_Universe_(_status='ACTIVE', _iterate=True, _perPage=50)
#pprint.pprint(darwinUniverse)
#darwinUniverse.to_csv('/home/zmlaptop/Desktop/AlphaTeamDX/DataDARWINUniverse/darwinUniverse.csv')

### DWX_AccInfo_API:
#print(darwinexInvestorAcc._Get_Accounts_())

### DWX_Quotes_API:
#darwinexQuotes._stream_quotes_()
#darwinexQuotes._process_stream_(_symbols=["ENH.4.16"], _plot=False)

### DWX_Trading_API:
#darwinexTrading._Get_Permitted_Operations_()
#darwinexTrading._Get_Account_Leverage_(_id=0)

### DWX_WebSocket_API:
darwinexWebSocket.run(_symbols=["ENH.4.16", "CIS.4.11", "CGT.4.5","CDG.4.14", "ABH.4.21", "ENO.4.13"])