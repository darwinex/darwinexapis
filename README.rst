|PyVersion| |Status| |PyPiVersion| |License| |Docs| |Downloads|

Introduction
============

This is the **Dαrwinex APIs Python** package. 

With this package you will be able to access all the different APIs that Darwinex offers
and access all the functionality they actually implement.

Bear in mind that the APIs are in constant development and some things might evolve as time passes.

Be sure to take a look at the
`Darwinex API main website <https://www.darwinex.com/es/algorithmic-trading/darwin-api>`_,
and the `API docs <https://api.darwinex.com/store/>`_.

Important Notes
================

**NOTE:** This package will evolve **A LOT** going forward, so be sure to hit the **Watch** button to stay tuned
on new developments and features.

**NOTE 2:** As the package evolves, we will provide code examples that will deal with exception handling and practical use cases of it. At this point 
in time, the package is released **AS IS** and the user is responsible of handling any specific cases for their application.

API Access Tokens
==================

If you request access to all the APIs in the platform, the ``access_token`` will be valid for just a brief period of time (exactly
around 3600 seconds). However, if you request access to just the data APIs the valid token will last for around six months.

Quotes stating the same are the following:

    * Access to all the APIs: The access token will be valid for a brief period of time. New tokens can automatically be generated through Refresh Token grant or requesting access again via this page.

    * Access to the DARWIN data APIs: This token will be valid for around 6 months unless you cancel it.

If for some reason you would like to use the ``refresh_token`` to be able to generate new ``access_token`` when the expiration time reaches (i.e. the trading and Investor Accounts APIs are going to be used on a constant basis), this package implements the functionality to do so in the ``DWX_API_Auth`` module; it just checks if the expiration time has reached and it uses the ``refresh_token`` to get a new ``access_token``.

Explanation
===========

The **DARWIN API Suite** is composed of the following 5 APIs:

* **DARWIN Info API** - access the entire universe of DARWIN quotes and scores
* **DARWIN Trading API** - Buy/Sell DARWINs, set conditional SLs and TPs
* **Investor Accounts API** - Monitor the evolution of your positions in real-time
* **DARWIN Quotes API** - Stream tick-level DARWIN quotes in real-time.
* **Quote Web Socket API** - Subscribe to real-time DARWIN quotes via Web Sockets.

Alternatively, you will also find **TickData APIs** for traditional assets listed in Darwinex.

Adding to this, there is also the **Darwin Data Analytics API** and you will find more information about it
in the dedicated **README** in its own folder.

First four APIs > **REST APIs (Info, Trading; Investor Accounts, Quotes)**
=================================================================================

**REST** is acronym for **REpresentational State Transfer**. A RESTful API is an application program interface (API) that uses HTTP requests to ``GET``, ``PUT``, ``POST`` and ``DELETE`` data. In most cases, the returned response is a JSON object holding all the neccesary data. As the communication protocol is HTTP, the REST APIs can be accessed from most modern programming languages.

A **RESTful** web service request contains:

* **An Endpoint URL**: An application implementing a RESTful API will define one or more URL endpoints with a domain, port, path, and/or querystring.

* **The HTTP method**: Differing ``HTTP`` methods can be used on any endpoint which map to application create, read, update, and delete (CRUD) operations.

* **HTTP headers**: Information such as authentication tokens or cookies can be contained in the ``HTTP`` request header.

* **Body Data**: Data is normally transmitted in the ``HTTP`` body in an identical way to ``HTML`` <form> submissions or by sending a single JSON-encoded data string.

Fifth API > **WebSockets-based API**
==================================================

**WebSockets** provide a persistent connection between a client and server that both parties can use to start sending data at any time. The client establishes a WebSocket connection through a process known as the WebSocket handshake.

**WebSocket** URLs use the ``ws`` scheme. There is also ``wss`` for secure WebSocket connections which is the equivalent of ``HTTPS``.

They are mostly use for streaming data without incurring in the software/hardware costs and overheads of ``HTTP`` resquest-response mechanism.

Installation
============

The package can be installed via ``pip`` as follows:

::

    pip install darwinexapis

    # If you would like to upgrade the version:
    
    pip install -U darwinexapis 

If you want to install the package in development mode, you just need to change your working directory to the ``/darwinexapis/`` and issue:

::

    pip install -e .

Example DARWIN API Suite
========================

The below code is a complete script to start playing with the different DARWIN Suite APIs.

Prior to working with it, you should go to the Darwinex API icon in the Darwinex Platform and generate your TOKEN (the one that matters is the Access Token).

.. code-block:: python

    # Let's import the different classes:
    from darwinexapis.API.InfoAPI.DWX_Info_API import DWX_Info_API
    from darwinexapis.API.InvestorAccountInfoAPI.DWX_AccInfo_API import DWX_AccInfo_API
    from darwinexapis.API.QuotesAPI.DWX_Quotes_API import DWX_Quotes_API
    from darwinexapis.API.TradingAPI.DWX_Trading_API import DWX_Trading_API
    from darwinexapis.API.WebSocketAPI.DWX_WebSocket_API import DWX_WebSocket_API

    ### Let's create the authentication dictionary:
    AUTH_CREDS = {'access_token': 'YOUR_ALPHA_TOKEN',
                  'consumer_key': 'YOUR_ALPHA_TOKEN',
                  'consumer_secret': 'YOUR_ALPHA_TOKEN',
                  'refresh_token': 'YOUR_ALPHA_TOKEN'}

    # Let's instantiate some API objects:
    darwinexInfo = DWX_Info_API(AUTH_CREDS, _version=2.0, _demo=True)
    darwinexInvestorAcc = DWX_AccInfo_API(AUTH_CREDS, _version=2.0, _demo=True)
    darwinexQuotes = DWX_Quotes_API(AUTH_CREDS, _version=1.0)
    darwinexTrading = DWX_Trading_API(AUTH_CREDS, _version=1.1, _demo=True)
    darwinexWebSocket = DWX_WebSocket_API(AUTH_CREDS, _version=0.0)

    # DWX_Info_API:
    darwinUniverse = darwinexInfo._Get_DARWIN_Universe_(_status='ACTIVE', 
                                                        _iterate=True, 
                                                        _perPage=100)
    print(darwinUniverse)

    # DWX_AccInfo_API:
    print(darwinexInvestorAcc._Get_Accounts_())

    # DWX_Quotes_API:
    darwinexQuotes._stream_quotes_()
    darwinexQuotes._process_stream_(_symbols=["ENH.4.16"], 
                                    _plot=False)

    # DWX_Trading_API:
    print(darwinexTrading._Get_Permitted_Operations_())
    print(darwinexTrading._Get_Account_Leverage_(_id=0))

    # DWX_WebSocket_API:
    darwinexWebSocket.run(_symbols=["ENH.4.16", 
                                    "CIS.4.11", 
                                    "CGT.4.5",
                                    "CDG.4.14", 
                                    "ABH.4.21", 
                                    "ENO.4.13"])

Example TickData APIs
=====================

The below code is a complete script to start playing with the different TickData APIs.

Prior to working with it, you should go to the Darwinex API icon in the Darwinex Platform and generate your TOKEN (the one that matters is the Access Token).

.. code-block:: python

    # Import the different classes:
    from darwinexapis.API.TickDataAPI.DWX_TickData_Downloader_API import \
        DWX_TickData_Downloader_API

    # Let's create the access token variable:
    FTP_CRED = {"username": "your_alpha_username",
                "password": "your_alpha_password",
                "ftpServer": "tickdata.darwinex.com"}

    # Downloader:
    # Try other assets like: GDAXIm, SPN35, XAUUSD... > Watch out with the available dates!
    DOWNLOADER = DWX_TickData_Downloader_API(dwx_ftp_user=FTP_CRED['username'], 
                                            dwx_ftp_pass=FTP_CRED['password'],
                                            dwx_ftp_hostname=FTP_CRED['ftpServer'],
                                            dwx_ftp_port=FTP_CRED['port'])

    # Create the path you wish to save the data:                                         
    path_to_save = 'EXAMPLE_DATA/'

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

.. code-block:: python

    # Import the different classes:
    from darwinexapis.API.TickDataAPI.DWX_TickData_Reader_API import DWX_TickData_Reader_API

    # Reader:
    bid_file_pkl = 'EXAMPLE_DATA/WS30_BID_2018-10-01_23.pkl'
    ask_file_pkl = 'EXAMPLE_DATA/WS30_ASK_2018-10-01_23.pkl'
    path_to_save = 'EXAMPLE_DATA/'

    # Generate the object: 
    READER = DWX_TickData_Reader_API(_bids_file=bid_file_pkl, 
                                    _asks_file=ask_file_pkl)

    # Generate the dataframe: 
    readed_dataframe = READER._get_symbol_as_dataframe_(_convert_epochs=True,
                                                        _check_integrity=True,
                                                        _calc_spread=True,
                                                        _reindex=['ask_price', 
                                                                  'bid_price', 
                                                                  'spread'],
                                                        _precision='tick')

    # Save it:                                                                                                    
    READER._save_df_to_csv(readed_dataframe, which_path=path_to_save)

Documentation
=============

You can find the complete `API documentation <https://api.darwinex.com/store/>`_ here. You will be able to understand the different exposed enpoints as well has play around with them to understand the returned JSON messages, whether they result in a succesfull request-response attempt or no.

Other helpful links:

    *  `Darwinex API FAQ and walkthrough <https://help.darwinex.com/api-walkthrough>`_
    *  `Darwinex Help Center <https://help.darwinex.com/>`_

Discussion
==========

The `Darwinex API Community Forum <https://https://community.darwinex.com/>`_ is one of the places to discuss
Darwinex API and anything related to it.

Furthermore, you can join the `Darwinex Collective Slack <https://join.slack.com/t/darwinex-collective/shared_invite/enQtNjg4MjA0ODUzODkyLWFiZWZlMDZjNGVmOGE2ZDBiZGI4ZWUxNjM5YTU0MjZkMTQ2NGZjNGIyN2QxZDY4NjUyZmVlNmU3N2E2NGE1Mjk>`_ for Q&A, debug and more.

Disclaimer
==========

The software is provided on the conditions of the BSD license that you can find inside the package.

**The αlpha's time has begun!**

:Author: Darwinex Alpha Team <content@darwinex.com>

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/darwinexapis.svg
   :alt: PyPi
   :target: https://pypi.python.org/pypi/darwinexapis

.. |PyVersion| image:: https://img.shields.io/badge/python-3.6+-blue.svg
   :alt:

.. |Status| image:: https://img.shields.io/badge/status-beta-green.svg
   :alt:

.. |License| image:: https://img.shields.io/badge/license-BSD-blue.svg
   :alt:

.. |Docs| image:: https://img.shields.io/badge/Documentation-green.svg
   :alt: Documentation
   :target: https://api.darwinex.com/store/

.. |Downloads| image:: https://pepy.tech/badge/darwinexapis
   :alt: Number of downloads
   :target: https://pepy.tech/project/darwinexapis
