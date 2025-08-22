from tableaudocumentapi.datasource_dependency import DatasourceDependency
from tableaudocumentapi.filter import Filter

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
        """Return the worksheet rows"""
        return self._cols
    
    @property
    def id(self):
        """Return the worksheet rows"""
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
        for filter in filter_elements:
            filters.append(Filter(filter))
        return filters    
    
    def _parse_rows_cols(self, type):
        """Function that will parse the rows and columns in the worksheet"""
        element_list = []
        if type == "rows":
            if self._xml.find('table/rows').text:
                element_list = self._xml.find('table/rows').text[1:-1].split(' / ')
        else:
            if self._xml.find('table/cols').text:
                element_list = self._xml.find('table/cols').text[1:-1].split(' / ')
        return element_list