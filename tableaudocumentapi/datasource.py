###############################################################################
#
# Datasource - A class for writing datasources to Tableau files
#
###############################################################################
import xml.etree.ElementTree as ET
from tableaudocumentapi import Connection


class ConnectionParser(object):

    def __init__(self, datasource_xml, version):
        self._dsxml = datasource_xml
        self._dsversion = version

    def _extract_federated_connections(self):
        return list(map(Connection, self._dsxml.findall('.//named-connections/named-connection/*')))

    def _extract_legacy_connection(self):
        return list(map(Connection, self._dsxml.findall('connection')))

    def get_connections(self):
        if float(self._dsversion) < 10:
            connections = self._extract_legacy_connection()
        else:
            connections = self._extract_federated_connections()
        return connections


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
        self._name = self._datasourceXML.get('name') or self._datasourceXML.get(
            'formatted-name')  # TDS files don't have a name attribute
        self._version = self._datasourceXML.get('version')
        self._connection_parser = ConnectionParser(
            self._datasourceXML, version=self._version)
        self._connections = self._connection_parser.get_connections()

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
        self._datasourceTree.write(self._filename, encoding="utf-8", xml_declaration=True)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        self._datasourceTree.write(new_filename, encoding="utf-8", xml_declaration=True)

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
    # connections
    ###########
    @property
    def connections(self):
        return self._connections
