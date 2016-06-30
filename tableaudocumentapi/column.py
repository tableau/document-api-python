import functools

_ATTRIBUTES = [
    'name',         # Name of the field as specified in the file, usually surrounded by [ ]
    'caption',      # Name of the field as displayed in Tableau unless an aliases is defined
    'datatype',     # Type of the field within Tableau (string, integer, etc)
    'role',         # Dimension or Measure
    'type',         # three possible values: quantitative, ordinal, or nominal
    'alias',        # Name of the field as displayed in Tableau if the default name isn't wanted
    'calculation',  # If this field is a calculated field, this will be the formula
]

_METADATA_ATTRIBUTES = [
    'aggregation',  # The type of aggregation on the field (e.g Sum, Avg)
]


def _find_metadata_record(record, attrib):
    element = record.find('.//{}'.format(attrib))
    if element is None:
        return None
    return element.text


class Column(object):
    def __init__(self, xmldata):
        for attrib in _ATTRIBUTES:
            self._apply_attribute(xmldata, attrib, lambda x: xmldata.attrib.get(x, None))

        # All metadata attributes begin at None
        for attrib in _METADATA_ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), None)

    def apply_metadata(self, metadata_record):
        for attrib in _METADATA_ATTRIBUTES:
            self._apply_attribute(metadata_record, attrib, functools.partial(_find_metadata_record, metadata_record))

    @classmethod
    def from_xml(cls, xmldata):
        return cls(xmldata)

    def __getattr__(self, item):
        private_name = '_{}'.format(item)
        if item in _ATTRIBUTES or item in _METADATA_ATTRIBUTES:
            return getattr(self, private_name)
        raise AttributeError(item)

    def _apply_attribute(self, xmldata, attrib, default_func):
        if hasattr(self, '_read_{}'.format(attrib)):
            value = getattr(self, '_read_{}'.format(attrib))(xmldata)
        else:
            value = default_func(attrib)

        setattr(self, '_{}'.format(attrib), value)

    @staticmethod
    def _read_calculation(xmldata):
        calc = xmldata.find('.//calculation')
        if calc is None:
            return None

        return calc.attrib.get('formula', None)
