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
    def __init__(self, dsxml, filename=None):
        """
        Constructor.  Default is to create datasource from xml.

        """
        self._filename = filename
        self._datasourceXML = dsxml
        self._datasourceTree = ET.ElementTree(self._datasourceXML)
        self._name = self._datasourceXML.get('name') or self._datasourceXML.get('formatted-name') # TDS files don't have a name attribute
        self._version = self._datasourceXML.get('version')
        if self._version == '10.0':
            self._connection = list(map(Connection,self._datasourceXML.findall('.//named-connections/named-connection/*')))
        else:
            self._connection = Connection(self._datasourceXML.find('connection'))

    @classmethod
    def from_file(cls, filename):
        "Initialize datasource from file (.tds)"
        dsxml = ET.parse(filename).getroot()
        return cls(dsxml, filename)

    def save(self):
        """
        Call finalization code and save file.

        Args:
            None.

        Returns:
            Nothing.

        """

        # save the file
        self._datasourceTree.write(self._filename)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        self._datasourceTree.write(new_filename)


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
