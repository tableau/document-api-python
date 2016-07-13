import functools

_ATTRIBUTES = [
    'id',           # Name of the field as specified in the file, usually surrounded by [ ]
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


class Field(object):
    """ Represents a field in a datasource """

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

    def _apply_attribute(self, xmldata, attrib, default_func):
        if hasattr(self, '_read_{}'.format(attrib)):
            value = getattr(self, '_read_{}'.format(attrib))(xmldata)
        else:
            value = default_func(attrib)

        setattr(self, '_{}'.format(attrib), value)

    @property
    def name(self):
        """ Provides a nice name for the field which is derived from the alias, caption, or the id.

        The name resolves as either the alias if it's defined, or the caption if alias is not defined,
        and finally the id which is the underlying name if neither of the fields exist. """
        alias = getattr(self, 'alias', None)
        if alias:
            return alias

        caption = getattr(self, 'caption', None)
        if caption:
            return caption

        return self.id

    @property
    def id(self):
        """ Name of the field as specified in the file, usually surrounded by [ ] """
        return self._id

    @property
    def caption(self):
        """ Name of the field as displayed in Tableau unless an aliases is defined """
        return self._caption

    @property
    def alias(self):
        """ Name of the field as displayed in Tableau if the default name isn't wanted """
        return self._alias

    @property
    def datatype(self):
        """ Type of the field within Tableau (string, integer, etc) """
        return self._datatype

    @property
    def role(self):
        """ Dimension or Measure """
        return self._role

    @property
    def is_quantitative(self):
        """ A dependent value, usually a measure of something

        e.g. Profit, Gross Sales """
        return self._type == 'quantitative'

    @property
    def is_ordinal(self):
        """ Is this field a categorical field that has a specific order

        e.g. How do you feel? 1 - awful, 2 - ok, 3 - fantastic """
        return self._type == 'ordinal'

    @property
    def is_nominal(self):
        """ Is this field a categorical field that does not have a specific order

        e.g. What color is your hair? """
        return self._type == 'nominal'

    @property
    def calculation(self):
        """ If this field is a calculated field, this will be the formula """
        return self._calculation

    @property
    def default_aggregation(self):
        """ The default type of aggregation on the field (e.g Sum, Avg)"""
        return self._aggregation

    ######################################
    # Special Case handling methods for reading the values from the XML
    ######################################
    @staticmethod
    def _read_id(xmldata):
        # ID is actually the name of the field, but to provide a nice name, we call this ID
        return xmldata.attrib.get('name', None)

    @staticmethod
    def _read_calculation(xmldata):
        # The formula for a calculation is stored in a child element, so we need to pull it out separately.
        calc = xmldata.find('.//calculation')
        if calc is None:
            return None

        return calc.attrib.get('formula', None)
