from tableaudocumentapi.datasource_dependency import DatasourceDependency
class Dashboard(object):
    """ A class representing a Tableau Dashboard in a workbook file. """
    
    def __init__(self, dashboard_xml):
        """Initialize the Dashboard from XML element representing it."""
        self._xml = dashboard_xml
        self._name = dashboard_xml.attrib['name']
        self._worksheets = self._parse_worksheets()
        self._datasource_dependencies = self._parse_datasource_dependencies()
        
    @property
    def xml(self):
        """Return the xml of the dashboard."""
        return self._xml
    
    @property
    def name(self):
        """Return the name of the dashboard."""
        return self._name
    
    @property
    def worksheets(self):
        """Return the worksheets """
        return self._worksheets
    
    @property
    def datasource_dependencies(self):
        """ Return the dashboard datasource dependencies """
        return self._datasource_dependencies
    
    def _parse_worksheets(self):
        """Function that will parse all the worksheets under dashboard """
        worksheets = []
        for zone in self.xml.find('zones').findall(".//zone"):
            if 'name' in zone.attrib:
                worksheets.append(zone.attrib['name'])
        return worksheets       
        
    def _parse_datasource_dependencies(self):
        """Get all the datasource dependencies under the dashboard"""
        datasource_dependencies = []
        datasource_dependency_elements = self._xml.findall('datasource-dependencies')
        for dependency in datasource_dependency_elements:
            if dependency.get("datasource"):
                datasource_dependencies.append(DatasourceDependency(dependency))
        return datasource_dependencies