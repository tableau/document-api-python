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

**Properties:**

`self.worksheets:` Returns a list of worksheets found in the workbook.

`self.datasources:` Returns a list of Datasource objects found in the workbook.

`self.filename:` Returns the filename of the workbook.

`self.shapes` Returns a list of strings with the names of shapes found in the workbook.

`self.dashboards:` Returns a list of strings with the names of the dashboards found in the workbook  

## Datasources
```python
class Datasource(dsxml, filename=None)
```
A class representing Tableau Data Sources, embedded in workbook files or in TDS files.

**Params:**

**Raises:**

**Methods:**

`Datasource.save(self)` Saves any changes to the datasource to the existing file.

`Datasource.save_as(self)` Saves any changes to the datasource to a new file specified by the `new_file` parameter.

`Datasource.add_field(self, name, datatype, role, field_type, caption)` Adds a base field object with the given values.

`Datasource.remove_field(self, field)` Remove a given field.

`Datasource.add_calculation(self, caption, formula, datatype, role, type)` Adds a calculated field with the given values.

**Properties:**

`self.name` Returns string with the name of datasource.

`self.version` Returns string of daatasource's version.

`self.caption` Returns string of user defined name of datasource if exists.

`self.connections` Returns list of connections used in workbook.

`self.fields` Returns key-value result of field name and their attributes.

`self.calculations` Returns calculated field of the workbook.

## Connections
```python
class Connection(connxml)
```

The Connection class represents a tableau data connection. It can be from any type of connection found in `dbclass.py` via `is_valid_dbclass`

**Params:**

**Raises:**

**Methods:**

**Properties:**

`self.server:` Returns a string containing the server.

`self.dbname:` Returns a string containing the database name.

`self.username:` Returns a string containing the username.

`self.dbclass:` Returns a string containing the database class.

`self.port:` Returns a string containing the port.

`self.query_band:` Returns a string containing the query band.

`self.initial_sql:` Returns a string containing the initial sql.

## Fields
```python
class Field(column_xml=None, metadata_xml=None)
```

Represents a field in a datasource

**Raises:**

**Methods:**
`Field.create_field_xml()` Create field from scratch.

`Field.add_alias(self, key, value)` Add an alias for a given display value.

**Properties:**

`self.name` Returns a string providing a nice name for the field which is derived from the alias, caption, or the id.

`self.id` Returns a string with name of the field as specified in the file, usually surrounded by [ ].

`self.xml` Returns a ElementTree object which represents an XML of the field.

`self.caption` Returns a string with the name of the field as displayed in Tableau unless an aliases is defined.

`self.alias` Returns a string with the name of the field as displayed in Tableau if the default name isn't wanted.

`self.datatype` Returns a string with the type of the field within Tableau (string, integer, etc).

`self.role` Returns a string which identify field as a Dimension or Measure.

`self.type` Returns a string with type of field (quantitative, ordinal, nominal).

`self.aliases` Returns Key-value mappings of all aliases that are registered under this field.

`self.is_quantitative` Returns a boolean if field is quantitative.

`self.is_ordinal` Returns a boolean if field is categorical that has a specific order.

`self.is_nominal` Returns a boolean if field is categorical that does not have a specific order.

`self.calculation` Returns a string with the formula if this field is a calculated field.

`self.default_aggregation` Returns a string with he default type of aggregation on the field (e.g Sum, Avg).

`self.description` Returns a string with contents of the <desc> tag on a field.

`self.worksheets` Returns a list of strings with the worksheet's names uses this field.
