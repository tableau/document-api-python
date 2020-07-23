class ColumnInstance(object):
    """Class representing column instance XML element"""
    
    def __init__(self, columnInstanceXmlElement):

        self._column_instance_xml = columnInstanceXmlElement
        self._column_instance_name = columnInstanceXmlElement.get('name')
        self._column_instance_column = columnInstanceXmlElement.get('column').strip('[').strip(']')


    @property
    def column_instance_column(self):
        return self._column_instance_column

    @property
    def column_instance_name(self):
        return self._column_instance_name

    @column_instance_column.setter
    def column_instance_column(self, value):
        processed_value = value.strip('[').strip(']')
        self._column_instance_column = processed_value
        self._column_instance_xml.set('column', "[{}]".format(processed_value))

    @column_instance_name.setter
    def column_instance_name(self, value):
        self._column_instance_name = value
        self._column_instance_xml.set('name', value)