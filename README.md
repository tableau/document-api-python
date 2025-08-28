# document-api-python (Fork)

[![As-Is](https://img.shields.io/badge/Support%20Level-As--Is-e8762c.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)

## About This Fork
This repository is a community-maintained fork of Tableau’s [document-api-python](https://github.com/tableau/document-api-python).  
It extends the original Document API with object-oriented access to dashboards, worksheets, filters, and datasource dependencies.  
All enhancements are fully backward compatible.

If you are looking for the official Tableau Document API, see the [upstream project](https://github.com/tableau/document-api-python).

## Enhancements in Version 012
This fork introduces the following major improvements:

- **Dashboard objects** – structured representation with worksheet containment and dependency tracking  
- **Worksheet objects** – access to datasource dependencies, filters, rows, columns, and column instances  
- **Filter support** – dedicated `Filter` class, including parsing of nested `groupfilter` structures  
- **Datasource dependencies** – new `DatasourceDependency` class separating fields from dependency columns and instances  
- **Query interface** – high-level `workbook.query` API for cross-workbook analysis and dependency mapping  
- **Field reference cleaning** – normalization of Tableau’s internal field naming conventions  

Detailed descriptions, examples, and resolved issue references are available in [Version 012 Enhancements](Version_012_enhancements.md).

## Upstream Issues Resolved
Several long-standing enhancement requests in the upstream project are addressed in this fork, including:

- [#33 – Datasource Filters](https://github.com/tableau/document-api-python/issues/33)  
- [#138 – Datasource-dependencies columns passed as fields](https://github.com/tableau/document-api-python/issues/138)  
- [#164 – Expose all child objects of Workbook/Worksheet](https://github.com/tableau/document-api-python/issues/164)  
- [#246 – Missing attributes for meta-data records](https://github.com/tableau/document-api-python/issues/246)  
- [#129 – Retrieve all fields used in a workbook](https://github.com/tableau/document-api-python/issues/129)  

For a full explanation, see the “Resolved Upstream Issues” section in [Version 012 Enhancements](Version_012_enhancements.md).

## Original Features
All original capabilities of the Tableau Document API are preserved, including:

- Support for TWB, TWBX, TDE and TDSX files  
- Access to connection information (server, username, database, authentication type, connection type)  
- Updating connection details in workbooks and datasources  
- Extracting field information from datasources and workbooks  

For Hyper files, refer to the [Tableau Hyper API](https://help.tableau.com/current/api/hyper_api/en-us/index.html).  
For more information on the original API, see the [Tableau API documentation](https://tableau.github.io/document-api-python).
