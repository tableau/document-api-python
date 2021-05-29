import xml.etree.ElementTree as ET
from tableaudocumentapi import Filter, WorksheetField


class Worksheet:
    """An object representing a worksheet in Tableau"""

    def __init__(self, xml):
        self._worksheet_xml = xml
        self._worksheet_tree = ET.ElementTree(self._worksheet_xml)
        self._worksheet_root = self._worksheet_tree.getroot()
        self._filters = self._prepare_filters(self._worksheet_root)
        self._worksheet_fields = self._prepare_fields(self._worksheet_root)

        self.name = self._worksheet_xml.get('name')
        
    @property
    def filters(self):
        return self._filters
    
    @property
    def fields(self):
        return self._worksheet_fields
    
    @staticmethod
    def _prepare_filters(xml_root):
        filters = []
        element_list = xml_root.findall('.//filter')
        if element_list is None:
            return []
        
        for elem in element_list:
            filter = Filter(elem)
            filters.append(filter)
        
        return filters
    
    @staticmethod
    def _prepare_fields(xml_root):
        worksheet_fields = []
        datasources = xml_root.findall('.//datasource-dependencies')
        if datasources is None:
            return []
        
        for ds in datasources:
            datasource_name = ds.get('datasource')
            fields = ds.findall('column-instance')
            for field in fields:
                worksheet_fields.append(WorksheetField(field, datasource_name))
        
        return worksheet_fields
