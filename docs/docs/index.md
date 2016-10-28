---
title: Get Started
layout: docs
---

To use this SDK, you must have Python installed. You can use either 2.7.X or 3.3 and later.

* TOC
{:toc}

### Installing the latest stable version (preferred)

```shell
pip install tableaudocumentapi
```

### Installing From Source

Download the `.zip` file that contains the SDK. Unzip the file and then run the following command:

```shell
pip install -e <directory containing setup.py>
```

### Installing the Development Version from Git

*Only do this if you know you want the development version, no guarantee that we won't break APIs during development*

```shell
pip install git+https://github.com/tableau/document-api-python.git@development
```

If you go this route, but want to switch back to the non-development version, you need to run the following command before installing the stable version:

```shell
pip uninstall tableaudocumentapi
```

## Basics
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

<div class="alert alert-info">
    <p><b>Note:</b> This call was added in version Tableau 10.3, XSDv2.5</p>
</div>

### Samples

The downloadable package contains several example scripts that show more detailed usage of the Document API.
