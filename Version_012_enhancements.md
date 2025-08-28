# Version 012 Enhancements

This document outlines the new features and functionality added in version 012 of the Tableau Document API.

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
- `column` - List of cleaned field references being filtered
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
- `get_workbook_dependencies()` - Returns flattened list of all dependencies with metadata
- `get_workbook_filters()` - Returns flattened list of all filters with metadata
- `get_field_objects(column)` - Links column references to Field objects from datasources

**Usage:**
```python
wb = Workbook('file.twbx')
dependencies = wb.query.get_workbook_dependencies()
for dep in dependencies:
    print(f"{dep['Dashboard']} with {dep['Worksheet']} uses {dep['Column_instance']} from {dep['Datasource']}")

filters = wb.query.get_workbook_filters()
for f in filters:
    print(f"{f['Worksheet']} filters {f['Column']} ({f['Filter_class']})")
```

### Enhanced Workbook Class

#### New Properties
- `dashboard_objects` - Dictionary mapping dashboard names to Dashboard objects
- `worksheet_objects` - Dictionary mapping worksheet names to Worksheet objects  
- `query` - Query object for advanced workbook analysis

#### Backwards Compatibility
All existing properties (`dashboards`, `worksheets`, `datasources`) continue to work unchanged.



## Open Issues Addressed by the Fork

### [#138 – Datasource-dependencies columns being passed as fields](https://github.com/tableau/document-api-python/issues/138)  
✅ **Resolved in v012**: Introduced a `DatasourceDependency` class and extended each `Worksheet` with a `.datasource_dependencies` property.  
- Dependencies now expose their own **columns** and **column instances**, separate from `Datasource.fields`.  
- This distinction allows developers to correctly differentiate between **true fields** and **dependency columns**, avoiding the ambiguity in the original API.  

---

### [#33 – Datasource Filters](https://github.com/tableau/document-api-python/issues/33)  
✅ **Resolved in v012**: Added a `Filter` class that provides direct access to worksheet-level and datasource-level filters.  
- Exposes filter class, target column(s), and nested `groupfilter` structures.  
- Eliminates the need for manual XML parsing when analyzing filters.  

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

This provides full programmatic access to worksheet internals that were previously only accessible by traversing raw XML.
### [#246 – Missing attributes for meta-data records](https://github.com/tableau/document-api-python/issues/246)
**✅ Resolved in v012**: Extended support for column instances at the worksheet level.
- Each column instance now exposes contextual attributes (derivation, pivot type, etc.).
- Previously, this metadata was only available at the datasource level in the pre-fork API.
### [#129 – Retrieve all fields used in a workbook](https://github.com/tableau/document-api-python/issues/129)
**✅ Resolved in v012**: Added a Query object that supports high-level traversal of XML for cross-workbook analysis.
- Query.get_workbook_dependencies() generates a tabular usage report of all fields across dashboards and worksheets.
- Greatly simplifies complex dependency mapping that previously required custom XML logic.

```python
workbook.query.get_workbook_dependencies()
# Outputs a tabular field usage report for every Dashboard and Worksheet
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