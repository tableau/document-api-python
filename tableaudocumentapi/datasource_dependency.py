class DatasourceDependency(object):
    """ A class representing a datasource dependency in a dashboard or worksheet"""
    def __init__(self, dependency_xml):
        """ Initialize DatasourceDependency from XML Element
        
        Args:
            dependency_xml: XML element representing the datasource dependency
        """
        self._xml = dependency_xml
        self._datasource = dependency_xml.attrib['datasource']
        self._columns = self._parse_columns()
        
    @property
    def xml(self):
        """Return xml of the datsource dependency """
        return self._xml
    
    @property
    def datasource(self):
        """Return datasource name of the dependency """
        return self._datasource
    
    @property
    def columns(self):
        """Return columns of the datsource dependency """
        return self._columns
    
    def _parse_columns(self):
        columns = {}
        for column in self._xml.findall('column'):
            columns[column.attrib['name'][1:-1]]= dict(column.attrib)
        return columns
        