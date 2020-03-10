class Relation(object):
    """A class representing relations between data source and connections (inside Data Sources)."""

    def __init__(self, relationxml):
        """Instantiate relation of the datasource and named connection.

        It is possible to change table_name of the extract via this class.
        self._connection_name provides the name of the named-connection for which relation is
        self._datasource_name provides the name of the datasource for which relation is

        """
        self._relationXML = relationxml
        self._connection_name = relationxml.get('connection')
        self._datasource_name = relationxml.get('name')
        self._table_name = relationxml.get('table')

    @property
    def connection_name(self):
        """The name of the connection to which relation belongs."""
        return self._connection_name

    @property
    def datasource_name(self):
        """The name of the datasource to which relation belongs."""
        return self._datasource_name

    @property
    def table_name(self):
        """The name of the table created by WDC."""
        return self._table_name
    
    @table_name.setter
    def table_name(self, value):
        """
        Sets the new table name for the relation.
        
        Args:
            value: new table name. String.
            
        Returns:
            Nothing.
        
        """
        self._table_name = value
        self._relationXML.set('table', value)