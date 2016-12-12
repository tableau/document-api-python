###############################################################################
#
# Datasource - A class for writing datasources to Tableau files
#
###############################################################################
import collections
import itertools
import xml.etree.ElementTree as ET
import xml.sax.saxutils as sax
from uuid import uuid4

from tableaudocumentapi import Connection, xfile
from tableaudocumentapi import Field
from tableaudocumentapi.multilookup_dict import MultiLookupDict
from tableaudocumentapi.xfile import xml_open

########
# This is needed in order to determine if something is a string or not.  It is necessary because
# of differences between python2 (basestring) and python3 (str).  If python2 support is every
# dropped, remove this and change the basestring references below to str
try:
    basestring
except NameError:  # pragma: no cover
    basestring = str
########

_ColumnObjectReturnTuple = collections.namedtuple('_ColumnObjectReturnTupleType', ['id', 'object'])


def _get_metadata_xml_for_field(root_xml, field_name):
    if "'" in field_name:
        field_name = sax.escape(field_name, {"'": "&apos;"})
    xpath = u".//metadata-record[@class='column'][local-name='{}']".format(field_name)
    return root_xml.find(xpath)


def _is_used_by_worksheet(names, field):
    return any((y for y in names if y in field.worksheets))


class FieldDictionary(MultiLookupDict):

    def used_by_sheet(self, name):
        # If we pass in a string, no need to get complicated, just check to see if name is in
        # the field's list of worksheets
        if isinstance(name, basestring):
            return [x for x in self.values() if name in x.worksheets]

        # if we pass in a list, we need to check to see if any of the names in the list are in
        # the field's list of worksheets
        return [x for x in self.values() if _is_used_by_worksheet(name, x)]


def _column_object_from_column_xml(root_xml, column_xml):
    field_object = Field.from_column_xml(column_xml)
    local_name = field_object.id
    metadata_record = _get_metadata_xml_for_field(root_xml, local_name)
    if metadata_record is not None:
        field_object.apply_metadata(metadata_record)
    return _ColumnObjectReturnTuple(field_object.id, field_object)


def _column_object_from_metadata_xml(metadata_xml):
    field_object = Field.from_metadata_xml(metadata_xml)
    return _ColumnObjectReturnTuple(field_object.id, field_object)


def base36encode(number):
    """Converts an integer into a base36 string."""

    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(ALPHABET):
        return sign + ALPHABET[number]

    while number != 0:
        number, i = divmod(number, len(ALPHABET))
        base36 = ALPHABET[i] + base36

    return sign + base36


def make_unique_name(dbclass):
    rand_part = base36encode(uuid4().int)
    name = dbclass + '.' + rand_part
    return name


class ConnectionParser(object):

    def __init__(self, datasource_xml, version):
        self._dsxml = datasource_xml
        self._dsversion = version

    def _extract_federated_connections(self):
        connections = list(map(Connection, self._dsxml.findall('.//named-connections/named-connection/*')))
        connections.extend(map(Connection, self._dsxml.findall("./connection[@class='sqlproxy']")))
        return connections

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
        self._caption = self._datasourceXML.get('caption', '')
        self._connection_parser = ConnectionParser(
            self._datasourceXML, version=self._version)
        self._connections = self._connection_parser.get_connections()
        self._fields = None

    @classmethod
    def from_file(cls, filename):
        """Initialize datasource from file (.tds)"""

        dsxml = xml_open(filename, cls.__name__.lower()).getroot()
        return cls(dsxml, filename)

    @classmethod
    def from_connections(cls, caption, connections):
        root = ET.Element('datasource', caption=caption, version='10.0', inline='true')
        outer_connection = ET.SubElement(root, 'connection')
        outer_connection.set('class', 'federated')
        named_conns = ET.SubElement(outer_connection, 'named-connections')
        for conn in connections:
            nc = ET.SubElement(named_conns,
                               'named-connection',
                               name=make_unique_name(conn.dbclass),
                               caption=conn.server)
            nc.append(conn._connectionXML)
        return cls(root)

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

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._datasourceXML.set('caption', value)
        self._caption = value

    @caption.deleter
    def caption(self):
        del self._datasourceXML.attrib['caption']
        self._caption = ''

    ###########
    # connections
    ###########
    @property
    def connections(self):
        return self._connections

    def clear_repository_location(self):
        tag = self._datasourceXML.find('./repository-location')
        if tag is not None:
            self._datasourceXML.remove(tag)

    ###########
    # Folders
    ###########

    @property
    def folders(self):
        """ Returns all folders.
        """
        return self._datasourceTree.findall('.//folder')

    def add_folder(self, name, role, fields):
        """ Adds a folder field with the given fields.

        Args:
            name:  Name of the new folder. String.
            role:  Role of the new folder. String.
            fields:  Fields of the new folder. String.

        Returns:
            The new calculated folder that was created. ET.Element.
        """
        # TODO: It might be better to create a dedicated "Folder" object:
        # Currently, there is a difference in Folder-Objects (ET.Elements) and
        # other Fields (dedicated Field-objects)
        folder = ET.Element('folder')
        folder.set('name', name)
        folder.set('role', role)

        for field in fields:
            item = ET.Element("folder-item")
            item.set("name", field)
            item.set("type", "field")
            folder.append(item)

        self._datasourceTree.getroot().append(folder)
        return folder

    def add_to_folder(self, name, fields):
        """ Adds fields to a folder field with the given fields.
        """
        folder = self._datasourceTree.find(".//folder/[@name='{}']".format(name))
        if not folder:
            raise ValueError("Could not find a folder named {}.".format(name))

        for field in fields:
            item = ET.Element("folder-item")
            item.set("name", field)
            item.set("type", "field")
            folder.append(item)

    ###########
    # fields
    ###########
    @property
    def fields(self):
        if not self._fields:
            self._fields = self._get_all_fields()
        return self._fields

    def _get_all_fields(self):
        column_field_objects = self._get_column_objects()
        existing_column_fields = [x.id for x in column_field_objects]
        metadata_only_field_objects = (x for x in self._get_metadata_objects() if x.id not in existing_column_fields)
        field_objects = itertools.chain(column_field_objects, metadata_only_field_objects)

        return FieldDictionary({k: v for k, v in field_objects})

    def _get_metadata_objects(self):
        return (_column_object_from_metadata_xml(x)
                for x in self._datasourceTree.findall(".//metadata-record[@class='column']"))

    def _get_column_objects(self):
        return [_column_object_from_column_xml(self._datasourceTree, xml)
                for xml in self._datasourceTree.findall('.//column')]
