class ViewPointField(object):
    """Represents viewpoint field."""
    def __init__(self, fieldxml):
        self._xml = fieldxml
        self._field_text = self._xml.text

    @property
    def field_text(self):
        return self._field_text


    @field_text.setter
    def field_text(self, value):
        self._field_text = value
        self._xml.text = value
        

class Window(object):
    """A class representing workbook window."""

    def __init__(self, windowxml):
        self._xml = windowxml
        self._viewpoint_fields = list(map(ViewPointField, self._xml.findall('./viewpoint//*field')))

    @property
    def viewpoint_fields(self):
        return self._viewpoint_fields
