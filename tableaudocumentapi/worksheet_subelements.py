class WorksheetBucket(object):
    """Class describing generic Bucket element in the worksheet."""

    def __init__(self, bucketxml):
        self._bucketxml = bucketxml
        self._bucket_text = self._bucketxml.text

    @property
    def bucket_text(self):
        return self._bucket_text


    @bucket_text.setter
    def bucket_text(self, value):
        self._bucket_text = value
        self._bucketxml.text = value

class LayoutOptions(object):
    """Describes layout-options sub element of worksheet."""

    def __init__(self, layoutoptionsxml):

        self._layoutxml = layoutoptionsxml
        self._run_elements = self._layoutxml.findall('.//*run')

    @property
    def run_elements(self):
        return self._run_elements

    def change_elements_text(self, ds_name, keyword_dictionary):
        """
        This method ues keyword dictionary:
        keys: strings to be changed
        values: target value of change per key
        """

        for run_el_xml in self._run_elements:
            if ds_name in run_el_xml.text:
                to_be_replaced = list(f for f in keyword_dictionary.keys() if f in run_el_xml.text)
                if len(to_be_replaced) > 0:
                    new_run_el_text = ''.join(run_el_xml.text.replace(field_name, keyword_dictionary[field_name])
                                              for field_name in to_be_replaced)
                    run_el_xml.text = new_run_el_text

class WorksheetStyleRuleFormat(object):
    """Represents format xml element within style-rule."""

    def __init__(self, formatxmlelement):
        self._xml = formatxmlelement
        self._field_text = self._xml.get('format')

    @property
    def field_text(self):
        return self._field_text

    @field_text.setter
    def field_text(self, value):
        self._field_text = value
        self._xml.set('field', value)

class WorksheetStyleRuleEncoding(object):
    """Represents encoding xml element within style-rule."""

    def __init__(self, encodingxmlelement):
        self._xml = encodingxmlelement
        self._field_text = self._xml.get('field')

    @property
    def field_text(self):
        return self._field_text

    @field_text.setter
    def field_text(self, value):
        self._field_text = value
        self._xml.set('field', value)


class WorksheetStyleRule(object):
    """This class represents style-rule xml element(s) in
        - worksheet/table/style
        - worksheet/table/panes/style
    """

    def __init__ (self, stylerulexmlelement):
        self._xml = stylerulexmlelement
        self._encodings = list(map(WorksheetStyleRuleEncoding, self._xml.findall('./encoding')))
        self._formats = list(map(WorksheetStyleRuleFormat, self._xml.findall('./format')))

    @property
    def encodings(self):
        return self._encodings

    @property
    def formats(self):
        return self._formats

class PaneEncodingText(object):
    """text xml element within encodings."""

    def __init__(self, etextxml):
        self._xml = etextxml
        self._column_attribute = self._xml.get('column')

    @property
    def column_attribute(self):
        return self._column_attribute

    @column_attribute.setter
    def column_attribute(self, value):
        self._column_attribute = value
        self._xml.set('column', value)

class PaneEncodingColor(object):
    """color xml element within encodings."""

    def __init__(self,ecolorxml):
        self._xml = ecolorxml
        self._column_attribute = self._xml.get('column')

    @property
    def column_attribute(self):
        return self._column_attribute

    @column_attribute.setter
    def column_attribute(self, value):
        self._column_attribute = value
        self._xml.set('column', value)

class WorksheetPaneEncoding(object):
    """Represents encoding at worksheet/../panes/pane/encoding."""

    def __init__(self, encodingsxmlelement):
        self._xml = encodingsxmlelement
        self._texts = list(map(PaneEncodingText, self._xml.findall('./text')))
        self._colors = list(map(PaneEncodingColor, self._xml.findall('./color')))

    @property
    def texts(self):
        return self._texts

    @property
    def colors(self):
        return self._colors

class WorksheetPane(object):
    """Describes worksheet pane element."""

    def __init__(self, panexmlelement):
        self._xml = panexmlelement
        self._pane_x_axis_name = self._xml.get('x-axis-name')
        self._pane_y_axis_name = self._xml.get('y-axis-name')

        self._pane_style_rule_elements = list(map(WorksheetStyleRule, self._xml.findall('./style/style-rule')))
        self._pane_encodings = WorksheetPaneEncoding(self._xml.find('encodings'))

    @property
    def pane_x_axis_name(self):
        return self._pane_x_axis_name

    @pane_x_axis_name.setter
    def pane_x_axis_name(self, value):
        self._pane_x_axis_name = value
        self._xml.set('x-axis-name', value)

    @property
    def pane_y_axis_name(self):
        return self._pane_y_axis_name

    @pane_y_axis_name.setter
    def pane_y_axis_name(self, value):
        self._pane_y_axis_name = value
        self._xml.set('y-axis-name', value)

    @property
    def pane_style_rule_elements(self):
        return self._pane_style_rule_elements

    @property
    def pane_encodings(self):
        return self._pane_encodings

