class StyleMap(object):
    """This class represents bucket in the style XML element."""

    def __init__(self, styleMapXmlElement):

        self._style_map_xml_element = styleMapXmlElement
        self._bucket_text = styleMapXmlElement.find('bucket').text
        
    @property
    def bucket_text(self):
        return self._bucket_text
    
    @bucket_text.setter
    def bucket_text(self, value):
        self._bucket_text = value
        self._style_map_xml_element.find('bucket').text = value

class StyleEncoding(object):
    """This class represents enconding XML element in the datasource/style/style-rule/enconding XML path."""

    def __init__(self, styleEncodingXmlElement):

        self._style_encoding_xml_element = styleEncodingXmlElement
        self._style_maps = list(StyleMap(sm) for sm in styleEncodingXmlElement.findall('map')) if styleEncodingXmlElement else None

    @property
    def style_maps(self):
        return self._style_maps