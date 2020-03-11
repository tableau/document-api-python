import xml.etree.ElementTree as ET
import json
from tableaudocumentapi.dbclass import is_valid_dbclass


class Connection(object):
    """A class representing connections inside Data Sources."""

    def __init__(self, namedconnxml):
        """Connection is usually instantiated by passing in connection elements
        in a Data Source. If creating a connection from scratch you can call
        `from_attributes` passing in the connection attributes.

        """
        # TODO each named connection should only have contain one connection instance always, maybe raise error if it does not?
        connxml = namedconnxml.findall('connection')[0]  
     
        self._connectionXML = connxml
        self._dbname = connxml.get('dbname')
        self._protocol = connxml.get('channel')
        self._server = connxml.get('server')
        self._connpath = connxml.get('path')
        self._filename = connxml.get('filename')
        self._username = connxml.get('username')
        self._authentication = connxml.get('authentication')
        self._class = connxml.get('class')
        self._port = connxml.get('port', None)
        self._query_band = connxml.get('query-band-spec', None)
        self._initial_sql = connxml.get('one-time-sql', None)
        self._connection_data = connxml.get('connectionData')
        self._connection_name = namedconnxml.get('name')

    def __repr__(self):
        return "'<Connection server='{}' dbname='{}' @ {}>'".format(self._server, self._dbname, hex(id(self)))

    @classmethod
    def from_attributes(cls, server, dbname, username, dbclass, port=None, query_band=None,
                        initial_sql=None, authentication='', channel='https', path=None, 
                        filename='connector.html', connection_data=None):
        """Creates a new connection that can be added into a Data Source.
        defaults to `''` which will be treated as 'prompt' by Tableau."""

        root = ET.Element('connection', authentication=authentication)
        xml = cls(root)
        xml.channel = channel
        xml.server = server
        xml.path = path
        xml.filename = filename
        xml.dbname = dbname
        xml.username = username
        xml.dbclass = dbclass
        xml.port = port
        xml.query_band = query_band
        xml.initial_sql = initial_sql
        xml.connection_data = connection_data

        return xml

    def connection_data_to_dictionary(self):
        """Returns self.connection_data as a dictionary. So it can be processed using Python dictionary functions."""
        return json.loads(self._connection_data)
    
    @staticmethod
    def connection_data_to_string(value, separators=(',', ':')):
        """
        Converts given value to JSONified string.
        
        Args:
            value: JSON serializable dictionary to be used as connectionData query
            separators: separators to be used in the JSON
        """
        return json.dumps(value, separators=separators)

    @property
    def dbname(self):
        """Database name for the connection. Not the table name."""
        return self._dbname

    @dbname.setter
    def dbname(self, value):
        """
        Set the connection's database name property.

        Args:
            value:  New name of the database. String.

        Returns:
            Nothing.

        """
        self._dbname = value
        self._connectionXML.set('dbname', value)

    @property
    def protocol(self):
        """Internet protocol to be used for WDC URL: http or https."""
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        """
        Set the connection's protocol property.

        Args:
            value: New protocol. String.

        Returns:
            Nothing.
        """
        self._protocol = value
        self._connectionXML.set('channel', value)
    
    @property
    def server(self):
        """Hostname or IP address of the database server. May also be a URL in some connection types."""
        return self._server

    @server.setter
    def server(self, value):
        """
        Set the connection's server property.

        Args:
            value:  New server. String.

        Returns:
            Nothing.

        """
        self._server = value
        self._connectionXML.set('server', value)

    @property
    def connpath(self):
        """Path to the WDC filename (the part of the WDC URL between server and filename)."""
        return self._connpath

    @connpath.setter
    def connpath(self, value):
        """
        Set the connection's connpath name property.

        Args:
            value: New path to the WDC filename. String.

        Returns:
            Nothing.

        """
        self._connpath = value
        # path can be None, in that case try to remove the element and don't write it to XML
        if value is None:
            try:
                del self._connectionXML.attrib['path']
            except KeyError:
                pass
        self._connectionXML.set('path', value)

    @property
    def filename(self):
        """WDC filename (.html)."""
        return self._filename

    @filename.setter
    def filename(self, value):
        """
        Set the connection's filename property.

        Args:
            value: New filename of the WDC. String.

        Returns:
            Nothing.

        """
        self._filename = value
        self._connectionXML.set('filename', value)

    @property
    def username(self):
        """Username used to authenticate to the database."""
        return self._username

    @username.setter
    def username(self, value):
        """
        Set the connection's username property.

        Args:
            value:  New username value. String.

        Returns:
            Nothing.

        """
        self._username = value
        self._connectionXML.set('username', value)

    @property
    def authentication(self):
        return self._authentication

    @property
    def dbclass(self):
        """The type of connection (e.g. 'MySQL', 'Postgresql'). A complete list
        can be found in dbclass.py"""
        return self._class

    @dbclass.setter
    def dbclass(self, value):
        """Set the connection's dbclass property.

        Args:
            value:  New dbclass value. String.

        Returns:
            Nothing.
        """

        if not is_valid_dbclass(value):
            raise AttributeError("'{}' is not a valid database type".format(value))

        self._class = value
        self._connectionXML.set('class', value)

    @property
    def port(self):
        """Port used to connect to the database."""
        return self._port

    @port.setter
    def port(self, value):
        """Set the connection's port property.

        Args:
            value:  New port value. String.

        Returns:
            Nothing.
        """

        self._port = value
        # If port is None we remove the element and don't write it to XML
        if value is None:
            try:
                del self._connectionXML.attrib['port']
            except KeyError:
                pass
        else:
            self._connectionXML.set('port', value)

    @property
    def query_band(self):
        """Query band passed on connection to database."""
        return self._query_band

    @query_band.setter
    def query_band(self, value):
        """Set the connection's query_band property.

        Args:
            value:  New query_band value. String.

        Returns:
            Nothing.
        """

        self._query_band = value
        # If query band is None we remove the element and don't write it to XML
        if value is None:
            try:
                del self._connectionXML.attrib['query-band-spec']
            except KeyError:
                pass
        else:
            self._connectionXML.set('query-band-spec', value)

    @property
    def initial_sql(self):
        """Initial SQL to be run."""
        return self._initial_sql

    @initial_sql.setter
    def initial_sql(self, value):
        """Set the connection's initial_sql property.

        Args:
            value:  New initial_sql value. String.

        Returns:
            Nothing.
        """

        self._initial_sql = value
        # If initial_sql is None we remove the element and don't write it to XML
        if value is None:
            try:
                del self._connectionXML.attrib['one-time-sql']
            except KeyError:
                pass
        else:
            self._connectionXML.set('one-time-sql', value)

    @property
    def connection_data(self):
        """Data connection string used to create data extract from WDC."""
        return self._connection_data

    @connection_data.setter
    def connection_data(self, value, separators=(',', ':')):
        """Set the connection's connection_data property.

        Args:
            value: New connection data value. JSON-like string or JSON-serializable dictionary.

        Returns:
            Nothing.

        """
        if isinstance(value, str):
            self._connection_data = value
            self._connectionXML.set('connectionData', value)
        elif isinstance(value, dict):
            value = self.connection_data_to_string(value, separators=separators)
            self._connection_data = value
            self._connectionXML.set('connectionData', value)
        else:
            raise TypeError("dataConnection value must be a string or dictionary.")
        
    @property
    def connection_name(self):
        """
        Named connection name to which the connection belongs.
        Cannot be changed via this class because it comes from one step above in the XMl element tree.
        """
        return self._connection_name