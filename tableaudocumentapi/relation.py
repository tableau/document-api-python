from tableaudocumentapi.column import Column

class ConnectionRelation(object):
    """A class representing relations between data source and connections (inside Data Sources)."""

    def __init__(self, relationxml):
        """Instantiate relation of the datasource and named connection.

        It is possible to change table_name of the extract via this class.
        self._connection_name provides the name of the named-connection for which relation is
        self._datasource_name provides the name of the datasource for which relation is

        """

        has_columns, columns = self.get_relation_columns(relationxml)

        self._relationXML = relationxml
        self._connection_name = relationxml.get('connection')
        self._datasource_name = relationxml.get('name')
        self._table_name = relationxml.get('table')
        self._has_columns = has_columns
        self._columns = list(Column(col)for col in columns)

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
    
    @property
    def has_columns(self):
        return self._has_columns
    
    @property
    def columns(self):
        return self._columns
    
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

    @staticmethod
    def get_relation_columns(relationxml):
        columns = relationxml.findall('columns')
        return True if columns else False, columns