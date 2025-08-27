from tableaudocumentapi.datasource_dependency import DatasourceDependency
from tableaudocumentapi.filter import Filter
from tableaudocumentapi.utils import _clean_aggregated_column_name
import re
class Worksheet(object):
    """A class representing a Worksheet in a Tableau workbook file """
    
    def __init__(self, worksheet_xml):
        """Initialize the Worksheet from XML element representing it"""
        self._xml = worksheet_xml
        self._name = worksheet_xml.attrib['name']
        self._datasource_dependencies = self._parse_datasource_dependencies()
        self._filters = self._parse_filters()
        self._rows = self._parse_rows_cols('rows')
        self._cols = self._parse_rows_cols('cols')
        self._id = worksheet_xml.find('simple-id').get('uuid').replace("{", "").replace("}","")
        
    @property
    def xml(self):
        """Return the xml of the worksheet"""
        return self._xml
    
    @property
    def name(self):
        """Return the name of the worksheet"""
        return self._name
    
    @property
    def datasource_dependencies(self):
        """Return the worksheet datsource dependencies"""
        return self._datasource_dependencies
    
    @property
    def filters(self):
        """Return the worksheet filters"""
        return self._filters
    
    @property
    def rows(self):
        """Return the worksheet rows"""
        return self._rows
    
    @property
    def cols(self):
        """Return the worksheet cols"""
        return self._cols
    
    @property
    def id(self):
        """Return the worksheet id"""
        return self._id
    
    def _parse_datasource_dependencies(self):
        """Function that will parse the datsource dependencies under the worksheet"""
        datasource_dependencies = []
        datasource_dependency_elements = self._xml.findall('table/view/datasource-dependencies')
        for dependency in datasource_dependency_elements:
            if dependency.get("datasource"):
                datasource_dependencies.append(DatasourceDependency(dependency))
        return datasource_dependencies    
    
    def _parse_filters(self):
        """Function that will parse the filters under the worksheet"""
        filters = []
        filter_elements = self._xml.findall('table/view/filter')
        for filter_element in filter_elements:
            filters.append(Filter(filter_element))
        return filters    
    

    def _parse_rows_cols(self, row_or_col):
        """Function that will parse the rows and columns in the worksheet"""
        if row_or_col not in ["rows", "cols"]:
            raise ValueError("row_or_col must be 'rows' or 'cols'")

        path = f"table/{row_or_col}"
        text = self._xml.findtext(path, default='').strip()
        if not text:
            return []

        return _clean_aggregated_column_name(text)
