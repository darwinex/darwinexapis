# -*- coding: utf-8 -*-
"""
    DWX WebSocket API - Subclass of DWX_API for Quotes Streaming
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 25, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

# Do some imports:
import os, time, sys
import logging
logger = logging.getLogger()

from darwinexapis.API.dwx_api import DWX_API
import websockets, json, asyncio

class DWX_WebSocket_API(DWX_API):
    
    def __init__(self, _auth_creds='', _api_url='ws://api.darwinex.com/quotewebsocket/1.0.0', _api_name='', _version=0.0):
        
        # Set to WebSocket URL and other variables:
        self._api_url = _api_url
        self._auth_creds = _auth_creds
        self._api_name = _api_name
        self._version = _version

        # Initialize the DWX_API class:
        super().__init__(self._auth_creds, self._api_url, self._api_name, self._version)

        # We need to call this because the WSS API doesn't go via the _Call_API_ method.
        self._construct_auth_post_headers()
        
        # If false, stop polling data from websocket
        self._active = True
        self._websocket = None
    
    async def subscribe(self, _symbols=['DWZ.4.7','DWC.4.20','LVS.4.20','SYO.4.24','YZZ.4.20']):
        
        #logger.warning(f'[SUBSCRIBE_UP] - AUTH_HEADERS: {self._auth_headers}')

        # Connect:
        ws = await websockets.connect(self._api_url, extra_headers=self._auth_headers)

        # Subscribe to symbols
        await ws.send(json.dumps({ 'op': 'subscribe', 'productNames' :_symbols}))
        logger.warning('[SUBSCRIBE] - CONNECTED to WS Server!')
           
        # If _active is True, process data received.
        while self._active:
               
            # Check for connection:
            if not ws.open:

                # Reconnect:
                try:
                    # Connect:
                    ws = await websockets.connect(self._api_url, extra_headers=self._auth_headers)

                    # Subscribe to symbols
                    await ws.send(json.dumps({ 'op': 'subscribe', 'productNames' :_symbols}))
                    logger.warning('[SUBSCRIBE] - ¡RECONNECTED to WS Server!')

                except Exception:
                    logger.warning('[SUBSCRIBE] - Unable to reconnect, trying again...')

            # While active, do work:
            try:
                # If the time is greater that the time + the expires in > issue refresh:
                if time.time() > self.AUTHENTICATION.expires_in:

                    logger.warning('[SUBSCRIBE] - The expiration time has REACHED > ¡Generate TOKENS!')
                    # Generate new token:
                    self.AUTHENTICATION._get_access_refresh_tokens_wrapper()

                    # Re-run the loop:
                    logger.warning('[SUBSCRIBE] - Need to re-run the loop with new TOKENS...')
                    return

                else:
                    logger.warning('[SUBSCRIBE] - The expiration time has NOT reached yet > Continue...')

                # Keep returning:
                self._ret = await ws.recv()
               
                ###################### Insert your Quote handling logic here ######################
                # {"op":"hb","timestamp":1587838905842} > Heartbeats.
                # Reference: https://api.darwinex.com/store/site/pages/doc-viewer.jag?docName=Product%20Quotes%20WebSocket%20subscription%20walkthroughname=QuoteWebSocket& version=1.0.0&provider=admin&
                logger.warning(f'[SUBSCRIBE] - RETURNED MESSAGE: {self._ret}')
                ###################### Insert your Quote handling logic here ######################
            
            except Exception as ex:
                logger.warning(f'[SUBSCRIBE] - Ex: {ex}')

    def run(self, _symbols=['DWZ.4.7','DWC.4.20','LVS.4.20','SYO.4.24','YZZ.4.20']):
        
        self._symbols = _symbols
        self.event_loop = asyncio.get_event_loop()
        
        try:
            self.event_loop.run_until_complete(self.subscribe(_symbols))

        except RuntimeError as ex:

            logger.warning(f'[RUNTIME ERROR] > {ex}')
            
        except KeyboardInterrupt:

            logger.warning('[EXCEPTION] > ¡KeyboardInterrupt Exception!')

        else:

            # Re-run the loop and stop it:
            logger.warning('[RUN_ELSE] - Tokens generated > We will re-run the loop and start the WS connection again')

            # Cancel all tasks:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            logger.warning('[RUN_ELSE] - All tasks cancelled')

            # Stop the loop to clean:
            self.stop_and_close()

    def stop_and_close(self):
        
        """Stop and close loop"""

        self.event_loop.stop()
        self.event_loop.close()
        logger.warning('[CLOSE] - Loop stopped and closed')

        # Launch:
        self.launch_loop_again()

    def launch_loop_again(self):

        # We need to call this because the WSS API doesn't go via the _Call_API_ method.
        self._construct_auth_post_headers()

        # Create it and assign it:
        asyncio.set_event_loop(asyncio.new_event_loop())
        logger.warning('[LAUNCH] - New event loop set and assigned > Will run the coroutine again..')
        self.run(_symbols=self._symbols)
