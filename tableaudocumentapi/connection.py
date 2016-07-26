###############################################################################
#
# Connection - A class for writing connections to Tableau files
#
###############################################################################

KNOWN_DB_CLASSES = ('msaccess',
                    'msolap',
                    'bigquery',
                    'asterncluster',
                    'bigsql',
                    'aurora',
                    'awshadoophive',
                    'dataengine',
                    'DataStax',
                    'db2',
                    'essbase',
                    'exasolution',
                    'excel',
                    'excel-direct',
                    'excel-reader',
                    'firebird',
                    'powerpivot',
                    'genericodbc',
                    'google-analytics',
                    'googlecloudsql',
                    'google-sheets',
                    'greenplum',
                    'saphana',
                    'hadoophive',
                    'hortonworkshadoophive',
                    'maprhadoophive',
                    'marklogic',
                    'memsql',
                    'mysql',
                    'netezza',
                    'oracle',
                    'paraccel',
                    'postgres',
                    'progressopenedge',
                    'redshift',
                    'snowflake',
                    'spark',
                    'splunk',
                    'kognitio',
                    'sqlserver',
                    'salesforce',
                    'sapbw',
                    'sybasease',
                    'sybaseiq',
                    'tbio',
                    'teradata',
                    'vectorwise',
                    'vertica',
                    'denormalized-cube',
                    'csv',
                    'textscan',
                    'webdata',
                    'webdata-direct',
                    'cubeextract')


class Connection(object):
    """
    A class for writing connections to Tableau files.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################

    def __init__(self, connxml):
        """
        Constructor.

        """
        self._connectionXML = connxml
        self._dbname = connxml.get('dbname')
        self._server = connxml.get('server')
        self._username = connxml.get('username')
        self._authentication = connxml.get('authentication')
        self._class = connxml.get('class')

    def __repr__(self):
        return "'<Connection server='{}' dbname='{}' @ {}>'".format(self._server, self._dbname, hex(id(self)))

    ###########
    # dbname
    ###########
    @property
    def dbname(self):
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

    ###########
    # server
    ###########
    @property
    def server(self):
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

    ###########
    # username
    ###########
    @property
    def username(self):
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

    ###########
    # authentication
    ###########
    @property
    def authentication(self):
        return self._authentication

    ###########
    # dbclass
    ###########
    @property
    def dbclass(self):
        return self._class

    @dbclass.setter
    def dbclass(self, value):

        if value not in KNOWN_DB_CLASSES:
            raise AttributeError("'{}' is not a valid database type")

        self._class = value
        self._connectionXML.set('dbclass', value)
