import xml.etree.ElementTree as ET
from tableaudocumentapi.dbclass import is_valid_dbclass


class Connection(object):
    """A class representing connections inside Data Sources."""

    def __init__(self, connxml):
        """Connection is usually instantiated by passing in connection elements
        in a Data Source. If creating a connection from scratch you can call
        `from_attributes` passing in the connection attributes.

        """
        self._connectionXML = connxml
        self._dbname = connxml.get('dbname')
        self._server = connxml.get('server')
        self._username = connxml.get('username')
        self._authentication = connxml.get('authentication')
        self._class = connxml.get('class')
        self._port = connxml.get('port', None)
        self._query_band = connxml.get('query-band-spec', None)
        self._initial_sql = connxml.get('one-time-sql', None)

    def __repr__(self):
        return "'<Connection server='{}' dbname='{}' @ {}>'".format(self._server, self._dbname, hex(id(self)))

    @classmethod
    def from_attributes(cls, server, dbname, username, dbclass, port=None, query_band=None,
                        initial_sql=None, authentication=''):
        """Creates a new connection that can be added into a Data Source.
        defaults to `''` which will be treated as 'prompt' by Tableau."""

        root = ET.Element('connection', authentication=authentication)
        xml = cls(root)
        xml.server = server
        xml.dbname = dbname
        xml.username = username
        xml.dbclass = dbclass
        xml.port = port
        xml.query_band = query_band
        xml.initial_sql = initial_sql

        return xml

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
