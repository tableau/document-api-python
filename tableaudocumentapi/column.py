class Column(object):
    """A class to describe column XMl element in the datasource or in the datasource-relation XML elements."""

    def __init__(self, columnxmlelement):
        """Initializes column element."""

        is_calculation, calculation_xml = self.set_calculation(columnxmlelement)
        has_aliases, aliases_list_xml = self.set_aliases(columnxmlelement)

        self._columnxml = columnxmlelement
        self._calculationxml = calculation_xml
        self._column_name = columnxmlelement.get('name').strip('[').strip(']') if columnxmlelement.get('name') is not None else None
        self._has_aliases = has_aliases
        self._is_calculation = is_calculation
        self._calculation_formula = calculation_xml.get('formula') if is_calculation else None
        self._aliases_list = list(ColumnAlias(clm) for clm in aliases_list_xml)


    @property
    def column_name(self):
        return self._column_name

    @property
    def is_calculation(self):
        return self._is_calculation

    @property
    def calculation_formula(self):
        return self._calculation_formula

    @property
    def has_aliases(self):
        return self._has_aliases

    @property
    def aliases_list(self):
        return self._aliases_list

    @column_name.setter
    def column_name(self, value):
        processed_value = value.strip('[').strip(']')
        self._column_name = processed_value
        self._columnxml.set('name', "[{}]".format(value))

    @calculation_formula.setter
    def calculation_formula(self, value):
        self._calculation_formula = value
        self._calculationxml.set('formula', value)

    @staticmethod
    def set_calculation(columnxmlelement):
        calculation_el = columnxmlelement.find('calculation')
        return True if not calculation_el is None  else False, calculation_el

    @staticmethod
    def set_aliases(columnxmlelement):
        aliases_el = columnxmlelement.findall('alias')
        return True if len(aliases_el) > 0 else False, aliases_el
            
            
class ColumnAlias(object):
    """A class which describes column alias XML element."""

    def __init__(self, aliasxmlelement):
        self._aliasxmlelement = aliasxmlelement
        self._alias_key = aliasxmlelement.get('key')
        self._alias_value = aliasxmlelement.get('value')


    @property
    def alias_key(self):
        return self._alias_key

    @property
    def alias_value(self):
        return self._alias_value

    @alias_key.setter
    def alias_key(self, value):
        self._alias_key = value
        self._aliasxmlelement.set('key', value)

    @alias_value.setter
    def alias_value(self, value):
        self._alias_value = value
        self._aliasxmlelement.set('value', value)