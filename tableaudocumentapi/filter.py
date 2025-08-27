import re
from tableaudocumentapi.utils import _clean_aggregated_column_name
class Filter(object):
    """A class representing a Filter in a worksheet"""
    def __init__(self, filter_xml):
        """Inititialize Filter from XML Element
        
        Args:
            filter_xml: XML element representing the filter
        """
        self._xml = filter_xml 
        self._filter_class = filter_xml.get('class')
        self._column = _clean_aggregated_column_name(filter_xml.get('column'))
        
    @property
    def xml(self):
        """Return xml of the datsource dependency """
        return self._xml
    
    @property
    def filter_class(self):
        """Return class attribute of the filter""" 
        return self._filter_class
    
    @property
    def column(self):
        """Return columns of the filter """
        return self._column
