# Version 012 Enhancements

This document outlines the new features and functionality added in version 012 fork of the Tableau Document API.

## New Classes

### Dashboard
Represents a Tableau dashboard within a workbook.

**Properties:**
- `name` - Dashboard name
- `xml` - Raw XML element 
- `worksheets` - List of worksheet names contained in dashboard
- `datasource_dependencies` - List of DatasourceDependency objects

**Usage:**
```python
wb = Workbook('file.twbx')
for dashboard_name, dashboard in wb.dashboard_objects.items():
    print(f"Dashboard: {dashboard.name}")
    print(f"Contains worksheets: {dashboard.worksheets}")
```

### Worksheet  
Represents a Tableau worksheet within a workbook.

**Properties:**
- `name` - Worksheet name
- `xml` - Raw XML element
- `id` - Worksheet UUID (cleaned of curly braces)
- `datasource_dependencies` - List of DatasourceDependency objects
- `filters` - List of Filter objects
- `rows` - List of cleaned field references used in rows
- `cols` - List of cleaned field references used in columns

**Usage:**
```python
wb = Workbook('file.twbx')
for worksheet_name, worksheet in wb.worksheet_objects.items():
    print(f"Worksheet: {worksheet.name} (ID: {worksheet.id})")
    print(f"Rows: {worksheet.rows}")
    print(f"Filters: {len(worksheet.filters)}")
```

### DatasourceDependency
Represents datasource dependencies within dashboards or worksheets.

**Properties:**
- `datasource` - Name of the datasource
- `xml` - Raw XML element
- `columns` - List of column names
- `column_instances` - Dictionary mapping column references to their attributes

**Usage:**
```python
for dep in worksheet.datasource_dependencies:
    print(f"Datasource: {dep.datasource}")
    print(f"Columns: {dep.columns}")
    for col_ref, attrs in dep.column_instances.items():
        print(f"  {col_ref}: {attrs['type']}")
```

### Filter
Represents filters applied to datasources or worksheets

**Properties:**
- `filter_class` - Filter type (categorical, quantitative, etc.)
- `xml` - Raw XML element
- `column` - Cleaned field reference being filtered
- `datasource` - Name of the datasource for the filtered column
- `groupfilters` - List of nested groupfilter dictionaries

**Usage:**
```python
for filter_obj in worksheet.filters:
    print(f"Filter class: {filter_obj.filter_class}")
    print(f"Column: {filter_obj.column}")
    print(f"Groupfilters: {len(filter_obj.groupfilters)}")

for filter_obj2 in datasource.filters:
    print(f"Filter class: {filter_obj2.filter_class}")
    print(f"Column: {filter_obj2.column}")
    print(f"Groupfilters: {len(filter_obj2.groupfilters)}")
```

### Query
Provides high-level querying capabilities across the workbook.

**Methods:**
- `get_worksheet_dependencies()` - Returns flattened list of all dependencies with metadata
- `get_worksheet_filters()` - Returns flattened list of all filters with metadata and normalized groupfilters
- `get_worksheet_rows()` - Returns all row field references from worksheets with datasource mapping
- `get_worksheet_cols()` - Returns all column field references from worksheets with datasource mapping
- `normalize_groupfilter(filter_json)` - Flattens nested groupfilter structures into tabular format with parent-child relationships
- `get_field_objects(column, datasource_name)` - Links column references to Field objects from datasources
- `get_workbook_fields()` - Returns all workbook fields and their attributes (calculation, datatype, default aggregation)
- `get_workbook_parameters()` - Returns all workbook parameters and their attributes (aliases, members, value)
- `get_workbook_metadata_table()` - Generates comprehensive data table combining all workbook metadata for diff analysis
- `compare_diffs(wb1_filename, wb2_filename, wb1_twb_string, wb2_twb_string)` - Static method to compare two workbooks and return differences

**Usage:**
```python
wb = Workbook('file.twbx')

# Get worksheet dependencies
dependencies = wb.query.get_worksheet_dependencies()
for dep in dependencies:
    print(f"{dep['Worksheet']} uses {dep['Column_instance']} from {dep['Datasource']}")

# Get worksheet filters with normalized groupfilters
filters = wb.query.get_worksheet_filters()
for f in filters:
    print(f"{f['Worksheet']} filters {f['Column']} ({f['Filter_class']})")
    if 'groupfilter_function' in f:
        print(f"  Groupfilter: {f['groupfilter_function']} at depth {f.get('groupfilter_depth', 0)}")

# Get row and column field references
rows = wb.query.get_worksheet_rows()
cols = wb.query.get_worksheet_cols()
print(f"Found {len(rows)} row references and {len(cols)} column references")

# Get parameters
parameters = wb.query.get_workbook_parameters()
for p in parameters:
    print(f"Parameter: {p['Name']} (Type: {p['Datatype']})")
    print(f"  Value: {p['Value']}, Domain Type: {p['Parameter_Domain_Type']}")
    print(f"  Used in: {p['Worksheets']}")
```


## Workbook Comparison and Diff Analysis

Version 012 introduces powerful workbook comparison capabilities to track changes between different versions of Tableau workbooks.

### Comparing Two Workbooks
Use the `Query.compare_diffs()` static method to compare two Tableau workbooks:

```python
from tableaudocumentapi.query import Query

# Compare two workbook files
df_diff = Query.compare_diffs(
    wb1_filename="samples/show_workbook_diff/Workbook_v1.twbx",
    wb2_filename="samples/show_workbook_diff/Workbook_v2.twbx"
)

# Compare workbooks from XML strings (e.g., from Tableau Server)
df_diff = Query.compare_diffs(
    wb1_twb_string=xml_content_v1,
    wb2_twb_string=xml_content_v2
)

# Analyze the differences
print(f"Total differences: {len(df_diff)}")
added_items = df_diff[df_diff['Workbook_Source'] == 'wb2']
removed_items = df_diff[df_diff['Workbook_Source'] == 'wb1']
unchanged_items = df_diff[df_diff['Workbook_Source'] == 'both']
```

### Comprehensive Workbook Metadata Table
The `get_workbook_metadata_table()` method generates a complete metadata table by merging:
- Worksheet dependencies
- Filters with normalized groupfilters
- Row and column field references
- Field definitions and attributes
- Dashboard-worksheet mappings

```python
wb = Workbook('file.twbx')
metadata_table = wb.query.get_workbook_metadata_table()

# Export for external analysis or version comparison
metadata_table.to_csv("workbook_complete_analysis.csv", index=False)
```

### Sample Implementation
The repository includes a complete example in `samples/show_workbook_diff/`:

**show_diff.py** - Demonstrates comparing two workbook versions:
```python
from tableaudocumentapi.query import Query

# Compare two versions of a Tableau workbook
df_diff = Query.compare_diffs(
    wb1_filename="samples/show_workbook_diff/Workbook_v1.twbx",
    wb2_filename="samples/show_workbook_diff/Workbook_v2.twbx"
)

# Output the diff to CSV
df_diff.to_csv("samples/show_workbook_diff/Data/df_diff.csv", index=False)
```

**Additional Sample Files:**
- `Workbook_v1.twbx` and `Workbook_v2.twbx` - Example workbook versions for comparison
- `diff_dashboard.twb` - Tableau dashboard for visualizing comparison results
- `Data/df_diff.csv` - Generated diff output for analysis


## Enhanced Classes
### Workbook Class
#### New Workbook Properties
- `dashboard_objects` - Dictionary mapping dashboard names to Dashboard objects
- `worksheet_objects` - Dictionary mapping worksheet names to Worksheet objects  
- `query` - Query object for advanced workbook analysis

#### XML String Input Support
The Workbook constructor now accepts TWB XML as a string input, enabling integration with Tableau [Server Client](https://tableau.github.io/server-client-python/) and [Rest API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm)

```python
# Create workbook from file (existing functionality)
wb1 = Workbook('file.twbx')

# Create workbook from XML string (new functionality)
xml_content = "<workbook>...</workbook>"
wb2 = Workbook(twb_xml_string=xml_content)

# Note: Workbooks created from strings cannot use save(), only save_as()
wb2.save_as('new_file.twb')
```
### Field Class
#### New Field Properties
Field objects now include parameter-specific properties:

**New Properties:**
- `table` - The datasource table the column belongs to (not applicable to calculations, parameters)
- `value` - The default value for parameters
- `param_domain_type` - Parameter domain type (range, list, etc.)
- `members` - List of member values (improved extraction from XML)

```python
for ds in wb.datasources:
    # Access parameter-specific field properties
    if ds.name == "Parameters":
        for field_name, field in ds.fields.items():
            print(f"Parameter: {field.caption}")
            print(f"  Value: {field.value}")
            print(f"  Domain Type: {field.param_domain_type}")
            print(f"  Members: {field.members}")
    else:
        # Get the table in the datasource a column belongs to
        print(f"Table: {field.table})
```

#### Backwards Compatibility
All existing properties (`dashboards`, `worksheets`, `datasources`) continue to work unchanged.



## Open Issues Addressed by the Fork

### [#138 – Datasource-dependencies columns being passed as fields](https://github.com/tableau/document-api-python/issues/138)  
✅ **Resolved in v012**: Introduced a `DatasourceDependency` class and extended each `Worksheet` with a `.datasource_dependencies` property.  
- Dependencies now expose their own **columns** and **column instances**, separate from `Datasource.fields`, allowing for distinction

---

### [#33 – Datasource Filters](https://github.com/tableau/document-api-python/issues/33)  
✅ **Resolved in v012**: Added a `Filter` class that provides direct access to worksheet-level and datasource-level filters.  
- Exposes filter class, target column(s), and nested `groupfilter` structures.  

**Example:**
```python
workbook.datasources[3].filters
# Output: [<tableaudocumentapi.filter.Filter at 0x104765600>]
```
### [#164 – Expose all child objects of Workbook/Worksheet](https://github.com/tableau/document-api-python/issues/164)
**✅ Resolved in v012:** Added a Worksheet class that exposes structured child elements and objects, including:
- Datasource Dependencies
- Filters
- Rows
- Columns
- Column Instances
- Worksheet ID (UUID)

### [#246 – Missing attributes for meta-data records](https://github.com/tableau/document-api-python/issues/246)
**✅ Resolved in v012**: Extended support for column instances at the worksheet level.
- Each column instance now exposes contextual attributes (derivation, pivot type, etc.).

### [#129 – Retrieve all fields used in a workbook](https://github.com/tableau/document-api-python/issues/129)
**✅ Resolved in v012**: Added a Query object that supports high-level traversal of XML for cross-workbook analysis.
- Query.get_workbook_dependencies() generates a tabular usage report of all fields across dashboards and worksheets.


```python
workbook.query.get_workbook_dependencies()
# Outputs a tabular field usage report for every Dashboard and Worksheet
workbook.query.get_workbook_fields()
# Outputs a tabular attribute report for all fields in a workbook
```


## Migration Notes

Version 012 is fully backwards compatible. Existing code will continue to work without modification. New functionality is accessed through new properties:

```python
# Existing (still works)
for dashboard_name in wb.dashboards:
    print(dashboard_name)

# New (additional functionality)  
for dashboard_name, dashboard_obj in wb.dashboard_objects.items():
    print(f"{dashboard_name} contains {len(dashboard_obj.worksheets)} worksheets")
```

The new object-oriented approach provides significantly more functionality while maintaining the simplicity of the original API for basic use cases.