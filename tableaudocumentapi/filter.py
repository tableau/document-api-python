class Filter(object):
    """A clas representing a Filter in a worksheet"""
    def __init__(self, filter_xml):
        """Ininitalize Filter from XML Element
        
        Args:
            filter_xml: XML element representing the filter
        """
        self._xml = filter_xml 
        self._filter_class = filter_xml.attrib['class']
        self._columns = filter_xml.attrib['column']
        
    @property
    def xml(self):
        """Return xml of the datsource dependency """
        return self._xml
    
    @property
    def filter_class(self):
        """Return class attribute of the filter"""
        return self._filter_class
    
    @property
    def columns(self):
        """Return columns of the datsource dependency """
        return self._columns
    