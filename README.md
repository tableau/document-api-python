# document-api-python
[![As-Is](https://img.shields.io/badge/Support%20Level-As--Is-e8762c.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)


Document API
---------------
This repo contains Python source and example files for the Tableau Document API. 
The Document API provides a useful but *unsupported* way to programmatically make updates to Tableau workbook and data source files. If you've been making changes to these file types by directly updating the XML--that is, by XML hacking--this SDK is for you :) Get help from other users on the [Tableau Community Forums](https://community.tableau.com/s/topic/0TO4T000000SF3sWAG/document-api).

Features include:
- Support for TWB, TWBX, TDE and TDSX files starting roughly back to Tableau 9.x
- Getting connection information from data sources and workbooks
  - Server Name
  - Username
  - Database Name
  - Authentication Type
  - Connection Type
- Updating connection information in workbooks and data sources
  - Server Name
  - Username
  - Database Name
- Getting Field information from data sources and workbooks
  - Get all fields in a data source
  - Get all fields in use by certain sheets in a workbook

- It *doesn't* support creating files from scratch, adding extracts into workbooks or data sources, or updating field information. As of 2021, this SDK no longer supports Python 2.

For Hyper files, take a look at the [Tableau Hyper API](https://help.tableau.com/current/api/hyper_api/en-us/index.html).

For more information, see the [Document API documentation](https://tableau.github.io/document-api-python)

