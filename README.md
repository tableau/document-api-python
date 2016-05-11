# tableausdk-python

This repo contains Python source and example files for the Tableau SDK. Currently the repo contains only the Document API. We're just getting started and have plans to expand what you find here. Help us by submitting feedback, issues, and pull requests!

Document API
---------------
The Document API provides a supported way to programmatically make updates to Tableau workbook (`.twb`) and datasource (`.tds`) files. If you've been making changes to these file types by directly updating the XML--that is, by XML hacking--this SDK is for you :)

Currently only the following operations are supported:

- Modify database server
- Modify database name
- Modify database user

We don't yet support creating files from scratch. In addition, support for `.twbx` and `.tdsx` files is coming.


###Getting Started
To use this SDK, you must have Python installed. You can use either 2.7x or 3.3x. 

Download the `.zip` file that contains the SDK. Unzip the file and then run the following command:

	pip install -e <directory containing setup.py>

We plan on putting the package in PyPi to make installation easier. 


###Basics
The following example shows the basic syntax for using the Document API to update a workbook:

	from tableaudocumentapi import Workbook
	
	sourceWB = Workbook('WorkbookToUpdate.twb')
	
	sourceWB.datasources[0].connection.server = "MY-NEW-SERVER"
	sourceWB.datasources[0].connection.dbname = "NEW-DATABASE"
	sourceWB.datasources[0].connection.username = "benl"
	
	sourceWB.save()


**Notes**

- Import the `Workbook` object from the `tableaudocumentapi` module.
- To open a workbook, instantiate a `Workbook` object and pass the `.twb` file name in the constructor.
- The `Workbook` object exposes a `datasources` collection.
- Each datasource object has a `connection` object that supports a `server`, `dbname`, and `username` property. 
- Save changes to the workbook by calling the `save` or `save_as` method.    



###Examples

The downloadable package contains an example named `replicateWorkbook.py` (in the folder `\Document API\Examples\Replicate Workbook`). This example reads an existing workbook and reads a .csv file that contains a list of servers, database names, and users. For each new user in the .csv file, the code copies the original workbook, updates the `server`, `dbname`, and `username` properties, and saves the workbook under a new name.  
