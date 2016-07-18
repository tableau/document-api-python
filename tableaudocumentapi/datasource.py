###############################################################################
#
# Datasource - A class for writing datasources to Tableau files
#
###############################################################################
import xml.etree.ElementTree as ET
import xml.sax.saxutils as sax
import zipfile

from tableaudocumentapi import Connection, xfile
from tableaudocumentapi import Field
from tableaudocumentapi.multilookup_dict import MultiLookupDict

########
# This is needed in order to determine if something is a string or not.  It is necessary because
# of differences between python2 (basestring) and python3 (str).  If python2 support is every
# dropped, remove this and change the basestring references below to str
try:
    basestring
except NameError:
    basestring = str
########


def _is_used_by_worksheet(names, field):
    return any((True for y in names if y in field.worksheets))


class FieldDictionary(MultiLookupDict):
    def found_in(self, name):
        # If we pass in a string, no need to get complicated, just check to see if name is in
        # the field's list of worksheets
        if isinstance(name, basestring):
            return [x for x in self.values() if name in x.worksheets]

        # if we pass in a list, we need to check to see if any of the names in the list are in
        # the field's list of worksheets
        return [x for x in self.values() if _is_used_by_worksheet(name, x)]


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
    def __init__(self, dsxml, filename=None, workbook_xml_root=None):
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
        self._usedFields = None
        # if workbook_xml_root is not None:
        #     self._prepare_from_worksheet(workbook_xml_root)

    @classmethod
    def from_file(cls, filename):
        """Initialize datasource from file (.tds)"""

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
        return FieldDictionary({k: v for k, v in column_objects})

    # def _prepare_from_worksheet(self, worksheet_xml):
    #     self._fields = self._get_all_fields()
    #     for element in worksheet_xml.findall(".//datasource-dependencies[@datasource='{}']/column".format(self.name)):
    #         column_name = element.attrib.get('name', None)
    #         column = self._fields.get(column_name, None)
    #         if column is not None:
    #             column.set_in_use()
