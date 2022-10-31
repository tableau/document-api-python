import functools
from lxml import etree as ET
from xml.dom import minidom

from tableaudocumentapi.property_decorators import argument_is_one_of

_ATTRIBUTES = [
    'id',           # Name of the field as specified in the file, usually surrounded by [ ]
    'caption',      # Name of the field as displayed in Tableau unless an aliases is defined
    'datatype',     # Type of the field within Tableau (string, integer, etc)
    'role',         # Dimension or Measure
    'type',         # three possible values: quantitative, ordinal, or nominal
    'alias',        # Name of the field as displayed in Tableau if the default name isn't wanted
    'calculation',  # If this field is a calculated field, this will be the formula
    'description',  # If this field has a description, this will be the description (including formatting tags)
    'hidden',       # If this field has been hidden
    'value',        # If this field is a parameter field, this will be the value 
]

_METADATA_ATTRIBUTES = [
    'aggregation',  # The type of aggregation on the field (e.g Sum, Avg)
]

_METADATA_TO_FIELD_MAP = [
    ('local-name', 'id'),
    ('local-type', 'datatype'),
    ('remote-alias', 'alias')
]


def _find_metadata_record(record, attrib):
    element = record.find('.//{}'.format(attrib))
    if element is None:
        return None
    return element.text


class Field(object):
    """ Represents a field in a datasource """

    def __init__(self, column_xml=None, metadata_xml=None):

        # Initialize all the possible attributes
        for attrib in _ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), None)
        for attrib in _METADATA_ATTRIBUTES:
            setattr(self, '_{}'.format(attrib), None)
        self._worksheets = set()

        if column_xml is not None:
            self._initialize_from_column_xml(column_xml)
            self._xml = column_xml
            # This isn't currently called because of the way we get the data from the xml,
            # but during the refactor, we might need it.  This is commented out as a reminder
            # if metadata_xml is not None:
            #     self.apply_metadata(metadata_xml)

        elif metadata_xml is not None:
            self._xml = metadata_xml
            self._initialize_from_metadata_xml(metadata_xml)

        else:
            raise AttributeError('column_xml or metadata_xml needed to initialize field')

    def _initialize_from_column_xml(self, xmldata):
        for attrib in _ATTRIBUTES:
            self._apply_attribute(xmldata, attrib, lambda x: xmldata.attrib.get(x, None))

    def _initialize_from_metadata_xml(self, xmldata):
        for metadata_name, field_name in _METADATA_TO_FIELD_MAP:
            self._apply_attribute(xmldata, field_name,
                                  lambda x: getattr(xmldata.find('.//{}'.format(metadata_name)), 'text', None),
                                  read_name=metadata_name)
            # print(metadata_name, field_name)
        self.apply_metadata(xmldata)

    @classmethod
    def create_field_xml(cls, caption, datatype, hidden, role, field_type, name):
        column = ET.Element('column')
        column.set('caption', caption)
        column.set('datatype', datatype)
        column.set('hidden', hidden)
        column.set('role', role)
        column.set('type', field_type)
        column.set('name', name)
        return column

    ########################################
    # Special Case methods for construction fields from various sources
    # not intended for client use
    ########################################
    def apply_metadata(self, metadata_record):
        for attrib in _METADATA_ATTRIBUTES:
            self._apply_attribute(metadata_record, attrib, functools.partial(_find_metadata_record, metadata_record))

    def add_used_in(self, name):
        self._worksheets.add(name)

    @classmethod
    def from_column_xml(cls, xmldata):
        return cls(column_xml=xmldata)

    @classmethod
    def from_metadata_xml(cls, xmldata):
        return cls(metadata_xml=xmldata)

    def _apply_attribute(self, xmldata, attrib, default_func, read_name=None):
        if read_name is None:
            read_name = attrib
        if hasattr(self, '_read_{}'.format(read_name)):
            value = getattr(self, '_read_{}'.format(read_name))(xmldata)
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
    def xml(self):
        """ XML representation of the field. """
        return self._xml

    def pretty_xml(self):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(self._xml, 'utf-8')
        prepared_string = minidom.parseString(rough_string)
        print_string = prepared_string.toprettyxml(indent="  ", newl="")
        return print_string.lstrip('<?xml version="1.0" ?>')

    def __str__(self):
        """ String representation of the field (only includes usable attributes) """
        # TODO: ideally this should just loop through the ATTRIBUTES so it doesn't need touching for new ones
        output = "------ FIELD {} ({}/{}/{}): {}(type), {}(datatype), {}(role), {}(aggregation)".format(
            self.name, self.caption, self.alias, self.id, self.type, self.datatype, self.role, self.default_aggregation)
        return output

    def detailed_str(self):
        if self.calculation:
            calc = "\ncalc: `{}`".format(self.calculation)
        else:
            calc = ""

    ########################################
    # Attribute getters and setters
    ########################################

    @property
    def caption(self):
        """ Name of the field as displayed in Tableau unless an aliases is defined """
        return self._caption

    @caption.setter
    def caption(self, caption):
        """ Set the caption of a field

            Args:
                caption:  New caption. String.

            Returns:
                Nothing.
        """
        self._caption = caption
        self._xml.set('caption', caption)

    @property
    def alias(self):
        """ Name of the field as displayed in Tableau if the default name isn't wanted """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """ Set the alias of a field

            Args:
                alias:  New alias. String.

            Returns:
                Nothing.
        """
        self._alias = alias
        self._xml.set('alias', alias)

    @property
    def datatype(self):
        """ Type of the field within Tableau (string, integer, etc) """
        return self._datatype

    @datatype.setter
    @argument_is_one_of('string', 'integer', 'date', 'boolean')
    def datatype(self, datatype):
        """ Set the datatype of a field

            Args:
                datatype:  New datatype. String.

            Returns:
                Nothing.
        """
        self._datatype = datatype
        self._xml.set('datatype', datatype)

    @property
    def hidden(self):
        """ If the column is Hidden ('true', 'false') """
        return self._hidden

    @hidden.setter
    @argument_is_one_of('true', 'false')
    def hidden(self, hidden):
        """ Set the hidden property of a field

            Args:
                hidden:  New hidden. String.

            Returns:
                Nothing.
        """
        self._hidden = hidden
        self._xml.set('hidden', hidden)

    @property
    def role(self):
        """ Dimension or Measure """
        return self._role

    @role.setter
    @argument_is_one_of('dimension', 'measure')
    def role(self, role):
        """ Set the role of a field

            Args:
                role:  New role. String.

            Returns:
                Nothing.
        """
        self._role = role
        self._xml.set('role', role)

    @property
    def type(self):
        """ Type of field (quantitative, ordinal, nominal) """
        return self._type

    @type.setter
    @argument_is_one_of('quantitative', 'ordinal', 'nominal')
    def type(self, field_type):
        """ Set the type of a field

            Args:
                field_type:  New type. String.

            Returns:
                Nothing.
        """
        self._type = field_type
        self._xml.set('type', field_type)

    ########################################
    # Aliases getter and setter
    # Those are NOT the 'alias' field of the column,
    # but instead the key-value aliases in its child elements
    ########################################

    def add_alias(self, key, value):
        """ Add an alias for a given display value.

            Args:
                key:  The data value to map. Example: "1". String.
                value: The display value for the key. Example: "True". String.
            Returns:
                Nothing.
        """

        # determine whether there already is an aliases-tag
        aliases = self._xml.find('aliases')
        # and create it if there isn't
        if not aliases:  # ignore the FutureWarning, does not apply to our usage
            aliases = ET.Element('aliases')
            self._xml.append(aliases)

        # find out if an alias with this key already exists and use it
        existing_alias = [tag for tag in aliases.findall('alias') if tag.get('key') == key]
        # if not, create a new ET.Element
        alias = existing_alias[0] if existing_alias else ET.Element('alias')

        alias.set('key', key)
        alias.set('value', value)
        if not existing_alias:
            aliases.append(alias)

    @property
    def aliases(self):
        """ Returns all aliases that are registered under this field.

        Returns:
            Key-value mappings of all registered aliases. Dict.
        """
        aliases_tag = self._xml.find('aliases') or []    # ignore the FutureWarning, does not apply to our usage
        return {a.get('key', 'None'): a.get('value', 'None') for a in list(aliases_tag)}

    ########################################
    # Attribute getters
    ########################################

    @property
    def is_quantitative(self):
        """ A dependent value, usually a measure of something

        e.g. Profit, Gross Sales """
        return self.type == 'quantitative'

    @property
    def is_ordinal(self):
        """ Is this field a categorical field that has a specific order

        e.g. How do you feel? 1 - awful, 2 - ok, 3 - fantastic """
        return self.type == 'ordinal'

    @property
    def is_nominal(self):
        """ Is this field a categorical field that does not have a specific order

        e.g. What color is your hair? """
        return self.type == 'nominal'

    @property
    def calculation(self):
        """ If this field is a calculated field, this will be the formula """
        return self._calculation

    @calculation.setter
    def calculation(self, new_calculation):
        """ Set the calculation of a calculated field.

        Args:
            new_calculation: The new calculation/formula of the field. String.
        """
        if self.calculation is None:
            calculation = ET.Element('calculation')
            calculation.set('class', 'tableau')
            calculation.set('formula', new_calculation)
            # Append the elements to the respective structure
            self._xml.append(calculation)

        else:
            self._xml.find('calculation').set('formula', new_calculation)

        self._calculation = new_calculation

    @property
    def value(self):
        """ If this field is a parameter field, this will be the value """
        return self._value

    @value.setter
    def value(self, new_value):
        """ Set the value of a parameter field.

        Args:
            new_value: The new value/formula of the field. String.
        """
        if self.value is None:
            value = ET.Element('calculation')
            value.set('class', 'tableau')
            value.set('formula', new_value)
            # Append the elements to the respective structure
            self._xml.append(value)

        else:
            self._xml.find('calculation').set('formula', new_value)

        self._value = new_value
        self._xml.set('value', new_value)

    @property
    def default_aggregation(self):
        """ The default type of aggregation on the field (e.g Sum, Avg)"""
        return self._aggregation

    @property
    def description(self):
        """ The contents of the <desc> tag on a field """
        return self._description

    @property
    def worksheets(self):
        """ Worksheets which uses field. """
        return list(self._worksheets)

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

    @staticmethod
    def _read_description(xmldata):
        description = xmldata.find('.//desc')
        if description is None:
            return None

        description_string = ET.tostring(description, encoding='utf-8')
        # Format expects a unicode string so in Python 2 we have to do the explicit conversion
        if isinstance(description_string, bytes):
            description_string = description_string.decode('utf-8')

        return description_string
