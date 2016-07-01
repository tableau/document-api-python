###############################################################################
#
# Datasource - A class for writing datasources to Tableau files
#
###############################################################################
import collections
import xml.etree.ElementTree as ET
import xml.sax.saxutils as sax
import zipfile

from tableaudocumentapi import Connection, xfile
from tableaudocumentapi import Field
from tableaudocumentapi.multilookup_dict import MultiLookupDict


def _mapping_from_xml(root_xml, column_xml):
    retval = Field.from_xml(column_xml)
    local_name = retval.id
    if "'" in local_name:
        local_name = sax.escape(local_name, {"'": "&apos;"})
    xpath = ".//metadata-record[@class='column'][local-name='{}']".format(local_name)
    metadata_record = root_xml.find(xpath)
    if metadata_record is not None:
        retval.apply_metadata(metadata_record)
    return retval.id, retval


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
        self._fields = None

    @classmethod
    def from_file(cls, filename):
        "Initialize datasource from file (.tds)"

        if zipfile.is_zipfile(filename):
            dsxml = xfile.get_xml_from_archive(filename).getroot()
        else:
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

        xfile._save_file(self._filename, self._datasourceTree)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        xfile._save_file(self._filename, self._datasourceTree, new_filename)

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

    ###########
    # fields
    ###########
    @property
    def fields(self):
        if not self._fields:
            self._fields = self._get_all_fields()
        return self._fields

    def _get_all_fields(self):
        column_objects = (_mapping_from_xml(self._datasourceTree, xml)
                          for xml in self._datasourceTree.findall('.//column'))
        return MultiLookupDict({k: v for k, v in column_objects})
