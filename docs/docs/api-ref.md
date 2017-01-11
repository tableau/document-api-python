---
title: API reference
layout: docs
---

* TOC
{:toc}

## Workbooks
```python
class Workbook(filename):
```

The Workbook class represents a tableau workbook. It may be either a TWB or TWBX, and the library will handle packaging and unpackaging automatically.

**Params:**

`filename` takes a string representing the path to the workbook file.

**Raises:**

`TableauVersionNotSupportedException` if the workbook is not a supported version.
`TableauInvalidFileException` if the file is not a valid tableau workbook file.

**Methods:**

`Workbook.save(self):`
Saves any changes to the workbook to the existing file.

`Workbook.save_as(self, new_filename):`
Saves any changes to the workbook to a new file specified by the `new_file` parameter.

**Properities:**

`self.worksheets:` Returns a list of worksheets found in the workbook.

`self.datasources:` Returns a list of Datasource objects found in the workbook.

`self.filename:` Returns the filename of the workbook.

## Datasources
```python
class Datasource(dsxml, filename=None)
```

## Connections
```python
class Connection(connxml)
```

The Connection class represents a tableau data connection. It can be from any type of connection found in `dbclass.py` via `is_valid_dbclass`

**Params:**

**Raises:**

**Methods:**

**Properities:**

`self.server:` Returns a string containing the server.

`self.dbname:` Returns a string containing the database name.

`self.username:` Returns a string containing the username.

`self.dbclass:` Returns a string containing the database class.

`self.port:` Returns a string containing the port.

`self.query_band:` Returns a string containing the query band.

`self.initial_sql:` Returns a string containing the initial sql.

## Fields
```python
class Workbook(column_xml=None, metadata_xml=None)
```
