try:
    from distutils2.version import NormalizedVersion as Version
except ImportError:
    from distutils.version import LooseVersion as Version

import xml.etree.ElementTree as ET
import zipfile

from tableaudocumentapi import xfile

MIN_SUPPORTED_VERSION = Version("9.0")


class VersionNotSupportedException(Exception):
    pass


def xml_open(filename):
    # Determine if this is a twb or twbx and get the xml root
    if zipfile.is_zipfile(filename):
        tree = xfile.get_xml_from_archive(filename)
    else:
        tree = ET.parse(filename)
    file_version = Version(tree.getroot().attrib.get('version', '0.0'))
    print(file_version, MIN_SUPPORTED_VERSION)
    if file_version < MIN_SUPPORTED_VERSION:
        raise VersionNotSupportedException(file_version)
    return tree
