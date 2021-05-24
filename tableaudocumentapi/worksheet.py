import xml.etree.ElementTree as ET
from tableaudocumentapi import Filter, DatasourceDependancy


class Worksheet:
    """An object representing a worksheet in Tableau"""

    def __init__(self, xml):
        self._worksheet_xml = xml
        self._worksheet_tree = ET.ElementTree(self._worksheet_xml)
        self._worksheet_root = self._worksheet_tree.getroot()
        self._filters = self._prepare_filters(self._worksheet_root)
        self._ds_dependancies = self._prepare_ds_dependancies(self._worksheet_root)

        self.name = self._worksheet_xml.get('name')
        
    @property
    def filters(self):
        return self._filters
    
    @property
    def fields(self):
        return self._ds_dependancies
    
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
    def _prepare_ds_dependancies(xml_root):
        ds_dependancies = []
        element_list = xml_root.find('.//datasource-dependencies')
        if element_list is None:
            return []
        
        for elem in element_list:
            if elem.tag == 'column-instance':
                ds_dependancy = DatasourceDependancy(elem)
                ds_dependancies.append(ds_dependancy)
        
        return ds_dependancies
