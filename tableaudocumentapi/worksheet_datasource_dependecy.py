from tableaudocumentapi.column import Column
from tableaudocumentapi.columnInstance import ColumnInstance

class DatasourceDependency(object):
    """A class to describe datasource dependency of a worksheet."""

    def __init__(self, datasourcedependencyxmlelement):
        """Initializes datasource dependency element."""

        self._dependencyXML = datasourcedependencyxmlelement
        self._dependency_datasource_name = self._dependencyXML.get('datasource')
        self._columns = list(map(Column, self._dependencyXML.findall('column')))
        self._columnInstances = list(map(ColumnInstance, self._dependencyXML.findall('column-instance')))

    
    @property
    def dependency_datasource_name(self):
        return self._dependency_datasource_name
    
    @property
    def columns(self):
        return self._columns

    @property
    def columnInstances(self):
        return self._columnInstances
