import xml.etree.ElementTree as ET
from tableaudocumentapi import Filter


class Worksheet:
    """An object representing a worksheet in Tableau"""

    def __init__(self, xml):
        self._worksheet_xml = xml
        self._worksheet_tree = ET.ElementTree(self._worksheet_xml)
        self._worksheet_root = self._worksheet_tree.getroot()
