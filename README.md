# document-api-python
[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools) [![Build Status](https://travis-ci.org/tableau/document-api-python.svg?branch=master)](https://travis-ci.org/tableau/document-api-python)

This repo contains Python source and example files for the Tableau Document API. We're just getting started and have plans to expand what you find here. Help us by submitting feedback, issues, and pull requests!

For more information, see the documentation:

<http://tableau.github.io/document-api-python>

Document API
---------------
The Document API provides a supported way to programmatically make updates to Tableau workbook and data source files. If you've been making changes to these file types by directly updating the XML--that is, by XML hacking--this SDK is for you :)

Features include:
- Support for 9.X, and 10.X workbook and data source files
  - Including TDSX and TWBX files
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

We don't yet support creating files from scratch, adding extracts into workbooks or data sources, or updating field information
