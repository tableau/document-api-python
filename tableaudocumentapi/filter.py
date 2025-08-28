import re
from tableaudocumentapi.utils import _clean_aggregated_column_names
class Filter(object):
    """A class representing a Filter in a worksheet or datasource"""
    def __init__(self, filter_xml):
        """Initialize Filter from XML Element
        
        Args:
            filter_xml: XML element representing the filter
        """
        
        self._xml = filter_xml 
        self._filter_class = filter_xml.get('class')
        self._column = _clean_aggregated_column_names(filter_xml.get('column'))
        self._groupfilters = self._parse_groupfilters()
        
    @property
    def xml(self):
        """Return xml of the filter """
        return self._xml
    
    @property
    def groupfilters(self):
        """Return groupfilters of the filter"""
        return self._groupfilters
    
    @property
    def filter_class(self):
        """Return class attribute of the filter""" 
        return self._filter_class
    
    @property
    def column(self):
        """Return columns of the filter """
        return self._column

    def _parse_groupfilters(self):
        """Function that will parse the groupfilters under the filter"""
        groupfilters = []
        groupfilter_elements = self._xml.findall('groupfilter')
        for groupfilter in groupfilter_elements:
            parsed_groupfilter = self._parse_single_groupfilter(groupfilter)
            if parsed_groupfilter:
                groupfilters.append(parsed_groupfilter)
        return groupfilters
    
    def _parse_single_groupfilter(self, groupfilter_xml):
        """Parse a single groupfilter element recursively"""
        if groupfilter_xml is None:
            return None
            
        groupfilter_data = {
            'function': groupfilter_xml.get('function'),
            'level': groupfilter_xml.get('level'),
            'member': groupfilter_xml.get('member'),
            'attributes': dict(groupfilter_xml.attrib),
            'children': []
        }
        
        # Parse nested groupfilters recursively
        child_groupfilters = groupfilter_xml.findall('groupfilter')
        for child in child_groupfilters:
            child_data = self._parse_single_groupfilter(child)
            if child_data:
                groupfilter_data['children'].append(child_data)
                
        return groupfilter_data
    
def _parse_filters(root_node, path):
    """Function that will parse the filters under the worksheet or datasource"""
    filters = []
    filter_elements = root_node.findall(path)
    for filter_element in filter_elements:
        filters.append(Filter(filter_element))
    return filters    