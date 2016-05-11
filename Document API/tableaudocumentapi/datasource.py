###############################################################################
#
# Datasource - A class for writing datasources to Tableau files
#
###############################################################################
import xml.etree.ElementTree as ET
from tableaudocumentapi import Connection


class Datasource(object):
    """
    A class for writing datasources to Tableau files.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################
    def __init__(self, dsxml):
        """
        Constructor.  Default is to create datasource from xml.

        """
        self._datasourceXML = dsxml
        self._name = self._datasourceXML.get('name') or self._datasourceXML.get('formatted-name') # TDS files don't have a name attribute
        self._version = self._datasourceXML.get('version')
        self._connection = Connection(self._datasourceXML.find('connection'))

    @classmethod
    def from_file(cls, filename):
        "Initialize datasource from file (.tds)"
        dsxml = ET.parse(filename).getroot()
        return cls(dsxml)

    ###########
    # name
    ###########
    @property
    def name(self):
        return self._name

    ###########
    # version
    ###########
    @property
    def version(self):
        return self._version

    ###########
    # connection
    ###########
    @property
    def connection(self):
        return self._connection
