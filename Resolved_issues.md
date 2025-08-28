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
