# document-api-python
[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)

This repo contains Python source and example files for the Tableau Document API. 

For more information, see the documentation:

<https://tableau.github.io/document-api-python>

Document API
---------------
The Document API provides a supported way to programmatically make updates to Tableau workbook and data source files. If you've been making changes to these file types by directly updating the XML--that is, by XML hacking--this SDK is for you :)

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

For Hyper files, take a look at the [Tableau Hyper API](https://help.tableau.com/current/api/hyper_api/en-us/index.html).

We don't support creating files from scratch, adding extracts into workbooks or data sources, or updating field information

As of 2021, this SDK no longer supports Python 2.
