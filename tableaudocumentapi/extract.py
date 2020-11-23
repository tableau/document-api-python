from tableaudocumentapi.metadata_record import MetadataRecord

class DatasourceExtract(object):
    """A class representing extract XMl section (the one inside of a datasource XML)."""
    
    def __init__(self, extractXmlElement):
        
        self._extract_xml = extractXmlElement
        self._extract_metadata_records = list(MetadataRecord(mtdr) for mtdr in extractXmlElement.findall('.//*metadata-record'))  if extractXmlElement is not None else []
        
    @property
    def extract_metadata_records(self):
        return self._extract_metadata_records
        
        