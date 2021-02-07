import xml.etree.ElementTree as ET
from tableaudocumentapi import BaseObject, Relation
from tableaudocumentapi.dbclass import is_valid_dbclass


class RelationParser(object):
    """Parser for detecting and extracting relations from Connection entities."""

    def __init__(self, connection_xml, version):
        self._connxml = connection_xml
        self._relversion = version

    def get_relations(self):
        """Find and return all relations."""
        relations_xml = self._connxml.findall('./relation')
        if relations_xml:
            return list(map(Relation, relations_xml))
        else:
            return None


class BaseConnection(BaseObject):

    def __init__(self, connxml, version=None):
        self._connectionXML = connxml
        self._class = connxml.get('class')
        self._dbname = connxml.get('dbname')
        self._server = connxml.get('server')
        self._username = connxml.get('username')
        self._authentication = connxml.get('authentication')
        self._port = connxml.get('port')
        self._channel = connxml.get('channel')
        self._dataserver_permissions = connxml.get('dataserver-permissions')
        self._directory = connxml.get('directory')
        self._server_oauth = connxml.get('server-oauth')
        self._workgroup_auth_mode = connxml.get('workgroup-auth-mode')
        self._query_band = connxml.get('query-band-spec')
        self._initial_sql = connxml.get('one-time-sql')

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
    def class_(self):
        """The type of connection (e.g. 'MySQL', 'Postgresql'). A complete list
        can be found in dbclass.py"""
        return self._class

    @class_.setter
    def class_(self, value):
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
    def channel(self):
        return self._channel

    @property
    def dataserver_permissions(self):
        return self._dataserver_permissions

    @property
    def directory(self):
        return self._directory

    @property
    def server_oauth(self):
        return self._server_oauth

    @property
    def workgroup_auth_mode(self):
        return self._workgroup_auth_mode

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

    def base_dict(self):
        base_attrs = [
            'class_', 'dbname', 'server', 'username',
            'authentication', 'port', 'channel', 'dataserver_permissions',
            'directory', 'server_oauth', 'workgroup_auth_mode',
            'query_band', 'initial_sql'
        ]
        base = self._to_dict(
            base_attrs=base_attrs
        )
        return base


class Connection(BaseConnection):

    def __init__(self, connxml, version=None):
        super().__init__(connxml, version=None)
        self._named_connections = self._extract_named_connections()
        self._relation_parser = RelationParser(
            connxml, version=version
        )
        self._relations = self._relation_parser.get_relations()

    def _extract_named_connections(self):
        named_connections = [
            conn for conn in self._connectionXML.findall('./named-connections/named-connection')
        ]
        return {nc.name: nc for nc in list(map(NamedConnection, named_connections))}

    @property
    def named_connections(self):
        return self._named_connections

    @property
    def relations(self):
        return self._relations

    def to_dict(self):
        base = super().base_dict()
        to_dict_list_attrs = ['relations']
        to_dict_of_dict_attrs = ['named_connections']
        base.update(
            self._to_dict(
                to_dict_list_attrs=to_dict_list_attrs,
                to_dict_of_dict_attrs=to_dict_of_dict_attrs
            )
        )
        return base


class NamedConnection(BaseConnection):
    """A class representing connections inside Data Sources."""

    def __init__(self, connxml, version=None):
        """Connection is usually instantiated by passing in connection elements
        in a Data Source. If creating a connection from scratch you can call
        `from_attributes` passing in the connection attributes.

        """
        assert connxml.tag == 'named-connection', "Must be of type named-connection"
        super().__init__(connxml.find('./connection'), version=version)
        self._name = connxml.get('name')
        self._caption = connxml.get('caption')

    @property
    def name(self):
        return self._name

    @property
    def caption(self):
        return self._caption

    def to_dict(self):
        base = super().base_dict()
        base_attrs = ['name', 'caption']
        base.update(
            self._to_dict(base_attrs=base_attrs)
        )
        return base
