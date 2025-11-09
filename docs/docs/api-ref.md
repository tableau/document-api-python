---
title: API reference
layout: docs
---

* TOC
{:toc}

## Workbooks
```python
class Workbook(filename=None, twb_xml_string=None):
```

The Workbook class represents a tableau workbook. It may be either a TWB or TWBX, and the library will handle packaging and unpackaging automatically. *(Enhanced in v012 to support XML string input)*

**Params:**

`filename` *(optional)* - String representing the path to the workbook file.

`twb_xml_string` *(optional, added in v012)* - String representing the TWB XML content. Enables integration with Tableau Server Client and REST API.

**Note:** Either `filename` or `twb_xml_string` must be provided, but not both.

**Raises:**

`TableauVersionNotSupportedException` if the workbook is not a supported version.
`TableauInvalidFileException` if the file is not a valid tableau workbook file.

**Methods:**

`Workbook.save(self):`
Saves any changes to the workbook to the existing file. *(Note: Raises exception for workbooks created from XML strings)*

`Workbook.save_as(self, new_filename):`
Saves any changes to the workbook to a new file specified by the `new_filename` parameter.

**Properties:**

`self.worksheets:` Returns a list of worksheets found in the workbook.

`self.datasources:` Returns a list of Datasource objects found in the workbook.

`self.filename:` Returns the filename of the workbook.

`self.shapes` Returns a list of strings with the names of shapes found in the workbook.

`self.dashboards:` Returns a list of strings with the names of the dashboards found in the workbook

`self.dashboard_objects:` Returns a dictionary mapping dashboard names to Dashboard objects *(added in v012)*

`self.worksheet_objects:` Returns a dictionary mapping worksheet names to Worksheet objects *(added in v012)*

`self.query:` Returns a Query object for advanced workbook analysis *(added in v012)*

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

`self.version` Returns string of datasource's version.

`self.caption` Returns string of user defined name of datasource if exists.

`self.connections` Returns list of connections used in workbook.

`self.fields` Returns key-value result of field name and their attributes.

`self.calculations` Returns calculated field of the workbook.

`self.filters` Returns datasource filters. *(added in v012)*



### Connections
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

### Fields
```python
class Field(column_xml=None, metadata_xml=None)
```

Represents a field in a datasource

**Raises:**

**Methods:**

`Field.create_field_xml(cls, caption, datatype, hidden, role, field_type, name, value=None, param_domain_type=None)` *(Enhanced in v012)* Create field XML from scratch. Now supports parameter-specific attributes with default values for backward compatibility.

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

`self.worksheets` Returns a list of strings with the worksheet names that use this field.

`self.value` *(added in v012)* Returns a string with the default value for a field. Applicable to parameters, not regular columns/calculations.

`self.param_domain_type` *(added in v012)* Returns a string with the parameter domain type (range, list, etc.). Applicable to parameters, not regular columns/calculations.

`self.members` *(added in v012)* Returns a list of member values extracted from the field's XML. Applicable to parameters, not regular columns/calculations.

`self.table` *(added in v012)* Returns a string with the name of the datasource table a column belongs to.

## Dashboards *(added in v012)*
```python
class Dashboard(dashboard_xml)
```

Represents a tableau dashboard within a workbook file.

**Params:**

`dashboard_xml` XML element representing the dashboard.

**Properties:**

`self.name:` Returns a string with the name of the dashboard.

`self.xml:` Returns the XML element of the dashboard.

`self.worksheets:` Returns a list of worksheet names contained in the dashboard.

`self.datasource_dependencies:` Returns a list of DatasourceDependency objects used by the dashboard.

## Worksheets *(added in v012)*
```python
class Worksheet(worksheet_xml)
```

Represents a tableau worksheet within a workbook file.

**Params:**

`worksheet_xml` XML element representing the worksheet.

**Properties:**

`self.name:` Returns a string with the name of the worksheet.

`self.xml:` Returns the XML element of the worksheet.

`self.id:` Returns a string with the worksheet UUID (cleaned of curly braces).

`self.datasource_dependencies:` Returns a list of DatasourceDependency objects used by the worksheet.

`self.filters:` Returns a list of Filter objects applied to the worksheet or datasource

`self.rows:` Returns a list of cleaned field references used in worksheet rows.

`self.cols:` Returns a list of cleaned field references used in worksheet columns.

### Datasource Dependencies *(added in v012)*
```python
class DatasourceDependency(dependency_xml)
```

Represents datasource dependencies within dashboards or worksheets.

**Params:**

`dependency_xml` XML element representing the datasource dependency.

**Properties:**

`self.datasource:` Returns a string with the name of the datasource.

`self.xml:` Returns the XML element of the dependency.

`self.columns:` Returns a list of column names referenced by the dependency.

`self.column_instances:` Returns a dictionary mapping column references to their attribute dictionaries.

### Filters *(added in v012)*
```python
class Filter(filter_xml)
```

Represents filters applied to worksheets or datasources.

**Params:**

`filter_xml` XML element representing the filter.

**Properties:**

`self.filter_class:` Returns a string with the filter type (categorical, quantitative, etc.).

`self.xml:` Returns the XML element of the filter.

`self.column:` Returns a cleaned field reference being filtered.

`self.datasource:` Returns a string with the name of the datasource for the filtered column.

`self.groupfilters:` Returns a list of nested groupfilter dictionaries representing the filter structure.

## Query *(added in v012)*
```python
class Query(workbook)
```

Provides high-level querying capabilities across the workbook.

**Params:**

`workbook` The workbook object to query.

**Methods:**

`Query.get_worksheet_dependencies(self):` Returns a flattened list of dictionaries containing all dependencies with metadata including worksheet, datasource, columns, column instances, and their attributes.

`Query.get_worksheet_filters(self):` Returns a pandas DataFrame containing all filters with metadata and normalized groupfilters including worksheet, filter class, datasource, column, and flattened groupfilter attributes.

`Query.get_worksheet_rows(self):` Returns a list of dictionaries containing all row field references from worksheets with datasource and row name mapping.

`Query.get_worksheet_cols(self):` Returns a list of dictionaries containing all column field references from worksheets with datasource and column name mapping.

`Query.normalize_groupfilter(self, filter_json):` Flattens nested groupfilter structures into tabular format with parent-child relationships. Returns a list of dictionaries with function, level, member, depth, parent_index, and attributes.

`Query.normalize_worksheet_filters(self, worksheet_filters):` Normalizes nested Groupfilters structures in worksheet filters into a flattened pandas DataFrame with exploded groupfilter attributes.

`Query.get_field_objects(self, column, datasource_name=None):` Links column references to Field objects from datasources. Returns Field object if found, None otherwise. Optionally accepts datasource name for faster lookup.

`Query.get_workbook_fields(self):` Returns a list of dictionaries containing all non-parameter workbook fields with their attributes including 'alias', 'aliases', 'calculation', 'caption', 'datatype', 'default_aggregation', 'description', 'hidden', 'id', 'is_nominal', 'is_ordinal', 'is_quantitative', 'name', 'param_domain_type', 'role', 'table', 'type', 'value', 'worksheets', and datasource information.

`Query.get_workbook_parameters(self):` Returns a list of dictionaries containing all workbook parameters with their attributes including alias, aliases, calculation, caption, datatype, name, parameter domain type, role, type, value, worksheets, and members.

`Query.get_workbook_metadata_table(self):` Generates a comprehensive pandas DataFrame combining all workbook metadata by merging worksheet dependencies, filters with normalized groupfilters, row and column field references, field definitions and attributes, and dashboard-worksheet mappings.

`Query.compare_diffs(wb1_filename, wb2_filename, wb1_twb_string=None, wb2_twb_string=None):` Static method that compares two Tableau workbooks and returns a pandas DataFrame with differences. Accepts either filenames or XML strings. The returned DataFrame includes a 'Workbook_Source' column indicating whether items are in 'wb1' (left only), 'wb2' (right only), or 'both' workbooks.

`Query.json_safe_dataframe(df):` Static method that converts pandas DataFrames containing complex types (dicts, lists, numpy arrays) to JSON-safe format by converting these types to JSON strings while leaving scalar values unchanged.
