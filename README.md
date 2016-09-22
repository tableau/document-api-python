# document-api-python

[![Build Status](https://travis-ci.org/tableau/document-api-python.svg?branch=master)](https://travis-ci.org/tableau/document-api-python)

This repo contains Python source and example files for the Tableau Document API. We're just getting started and have plans to expand what you find here. Help us by submitting feedback, issues, and pull requests!

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


###Getting Started
To use this SDK, you must have Python installed. You can use either 2.7.X or 3.3 and later.

#### Installing the latest stable version (preferred)

```text
pip install tableaudocumentapi
```

#### Installing From Source

Download the `.zip` file that contains the SDK. Unzip the file and then run the following command:

```text
pip install -e <directory containing setup.py>
```

#### Installing the Development Version from Git

*Only do this if you know you want the development version, no guarantee that we won't break APIs during development*

```text
pip install git+https://github.com/tableau/document-api-python.git@development
```

If you go this route, but want to switch back to the non-development version, you need to run the following command before installing the stable version:

```text
pip uninstall tableaudocumentapi
```

###Basics
The following example shows the basic syntax for using the Document API to update a workbook:

```python
from tableaudocumentapi import Workbook

sourceWB = Workbook('WorkbookToUpdate.twb')

sourceWB.datasources[0].connections[0].server = "MY-NEW-SERVER"
sourceWB.datasources[0].connections[0].dbname = "NEW-DATABASE"
sourceWB.datasources[0].connections[0].username = "benl"

sourceWB.save()
```

With Data Integration in Tableau 10, a data source can have multiple connections. To access the connections simply index them like you would datasources.

```python
from tableaudocumentapi import Workbook

sourceWB = Workbook('WorkbookToUpdate.twb')

sourceWB.datasources[0].connections[0].server = "MY-NEW-SERVER"
sourceWB.datasources[0].connections[0].dbname = "NEW-DATABASE"
sourceWB.datasources[0].connections[0].username = "benl"

sourceWB.datasources[0].connections[1].server = "MY-NEW-SERVER"
sourceWB.datasources[0].connections[1].dbname = "NEW-DATABASE"
sourceWB.datasources[0].connections[1].username = "benl"


sourceWB.save()
```


**Notes**

- Import the `Workbook` object from the `tableaudocumentapi` module.
- To open a workbook, instantiate a `Workbook` object and pass the file name as the first argument.
- The `Workbook` object exposes a list of `datasources` in the workbook
- Each data source object has a `connection` object that supports a `server`, `dbname`, and `username` property.
- Save changes to the workbook by calling the `save` or `save_as` method.



###[Examples](samples)

The downloadable package contains several example scripts that show more detailed usage of the Document API.
