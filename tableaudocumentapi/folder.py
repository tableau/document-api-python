import xml.etree.ElementTree as ET
from functools import wraps

from tableaudocumentapi import Field

########
# This is needed in order to determine if something is a string or not.  It is necessary because
# of differences between python2 (basestring) and python3 (str).  If python2 support is every
# dropped, remove this and change the basestring references below to str
try:
    basestring
except NameError:  # pragma: no cover
    basestring = str


class AlreadyMemberOfThisFolderException(Exception):
    pass


class MemberOfMultipleFoldersException(Exception):
    pass


def argument_is_one_of(*allowed_values):
    def property_type_decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if value not in allowed_values:
                error = "Invalid argument: {0}. {1} must be one of {2}."
                msg = error.format(value, func.__name__, allowed_values)
                raise ValueError(error)
            return func(self, value)
        return wrapper
    return property_type_decorator


class FolderItem(object):
    """ FolderItems belong to Folders and describe the Field-Objects
    that belong to a folder
    """

    def __init__(self, name, _type):
        self.name = name
        self.type = _type

    @classmethod
    def from_xml(cls, xml):
        return cls(xml.get('name', None), xml.get('type', None))

    @classmethod
    def from_field(cls, field):
        return cls(field.id, 'field')


class Folder(object):
    """ This class represents a folder in a Datasource.

    Folders have a name, a role (dimensions or measures) and contain Items
    """

    def __init__(self, datasource, xml):
        self._datasource = datasource
        self._xml = xml
        self.name = self._xml.get('name', None)
        self.role = self._xml.get('role', None)
        folder_item_xml = self._xml.findall('folder-item')
        self._folder_items = [FolderItem.from_xml(xml) for xml in folder_item_xml]

    # Alternative constructors

    @classmethod
    def all_folders_from_datasource(cls, datasource):
        folders_xml = datasource._datasourceTree.findall('.//folder')
        return [cls(datasource, xml) for xml in folders_xml]

    @classmethod
    def from_name_and_role(cls, name, role, parent_datasource):
        """Creates a new folder with a given name and a given role.
        """
        attributes = {
            'name': name,
            'role': role
        }
        xml = ET.Element('folder', attrib=attributes)
        return cls(parent_datasource, xml)

    # Properties

    @property
    def folder_items(self):
        return self._folder_items

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self._xml.set('name', name)

    @property
    def role(self):
        return self._role

    @property
    def xml(self):
        return self._xml

    @role.setter
    @argument_is_one_of('dimensions', 'measures')
    def role(self, role):
        self._role = role
        self._xml.set('role', role)

    # Functions that deal with folder-items

    def add_field(self, field):
        """ Adds a field to this folder
        """
        if not isinstance(field, Field):
            msg = 'Can only add Fields to Folders, not {}'
            raise ValueError(msg.format(type(field)))
        if self.has_item(field):
            raise AlreadyMemberOfThisFolderException(field)
        if any(f.has_item(field) for f in self._datasource.folders.values()):
            raise MemberOfMultipleFoldersException(field)

        self._add_field(field)

    def _add_field(self, field):
        """ Internal function to add a field
        """
        folder_item = FolderItem.from_field(field)
        self._folder_items.append(folder_item)
        name, _type = folder_item.name, folder_item.type
        ET.SubElement(self._xml, 'folder-item', {'name': name, 'type': _type})

    def remove_field(self, field):
        """ Removes a field from this folder
        """
        if not isinstance(field, Field):
            msg = 'Can only remove Fields from Folders, not {}'
            raise ValueError(msg.format(type(field)))
        if not self.has_item(field):
            raise ValueError('This field is not a member of the folder')

        self._remove_field(field)

    def _remove_field(self, field):
        """ Internal function to remove field
        """
        # remove from the data structure
        folder_items = filter(lambda f: f.name == field.id, self.folder_items)
        folder_item = list(folder_items)[0]
        self.folder_items.remove(folder_item)

        # remove from xml
        xml_elem = self.xml.find("folder-item[@name='{}']".format(field.id))
        self.xml.remove(xml_elem)

    # Utility functions

    def has_item(self, item):
        """ Returns True if the given item is a FolderItem of this Folder.
        Item may be String, Field or FolderItem
        """
        if isinstance(item, FolderItem):
            return item in self.folder_items
        elif isinstance(item, Field):
            return item.id in map(lambda fi: fi.name, self.folder_items)
        elif isinstance(item, basestring):
            return item in map(lambda fi: fi.name, self.folder_items)
        else:
            msg = 'Argument must be either String or FolderItem, not {}'
            raise ValueError(msg.format(type(item)))
