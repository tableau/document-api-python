import re

class WorksheetBucket(object):
    """Class describing generic Bucket element in the worksheet. Also describes column in join-lod-exclude-overrides element."""

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
        self._run_elements = self._layoutxml.findall('.//*run') if self._layoutxml else None

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
        self._texts = list(map(PaneEncodingText, self._xml.findall('./text'))) if self._xml else []
        self._colors = list(map(PaneEncodingColor, self._xml.findall('./color'))) if self._xml else []

    @property
    def texts(self):
        return self._texts

    @property
    def colors(self):
        return self._colors


class WorksheetPaneCustomizedTooltip(object):
    """Represents encoding at worksheet/../panes/pane/customized-tooltip."""

    def __init__(self, customizedtooltipxmlelement):
        self._xml = customizedtooltipxmlelement
        self._formattedtext = list(map(PaneTooltipFormattedTextRun, self._xml.findall('./formatted-text/run'))) if self._xml is not None else []

    @property
    def formattedtext(self):
        return self._formattedtext


class PaneTooltipFormattedTextRun(object):
    """text xml element within customized-tooltip."""

    def __init__(self, runxml):
        self._xml = runxml
        self._runtext = self._xml.text

    @property
    def runtext(self):
        return self._runtext

    @runtext.setter
    def runtext(self, value):
        self._xml.text = value
        self._runtext = value


class WorksheetPane(object):
    """Describes worksheet pane element."""

    def __init__(self, panexmlelement):
        self._xml = panexmlelement
        self._pane_x_axis_name = self._xml.get('x-axis-name')
        self._pane_y_axis_name = self._xml.get('y-axis-name')

        self._pane_style_rule_elements = list(map(WorksheetStyleRule, self._xml.findall('./style/style-rule')))
        self._pane_encodings = WorksheetPaneEncoding(self._xml.find('encodings'))
        self._customized_tooltip = WorksheetPaneCustomizedTooltip(self._xml.find('customized-tooltip')) if self._xml.find('customized-tooltip') else None # TODO

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

    @property
    def customized_tooltip(self):
        return self._customized_tooltip

class WorksheetRowsOrCols(object):
    """Describes rows element in the worksheet.
    """

    def __init__(self, rowsorcolsxml):
        self._xml = rowsorcolsxml

        self._rowsorcolscontent = self._xml.text

    @property
    def rowsorcolscontent(self):
        return self._rowsorcolscontent

    @rowsorcolscontent.setter
    def rowsorcolscontent(self, value):
        self._rowsorcolscontent = value
        self._xml.text = value

    def replace_correct_fields_names_in_content(self, ds_name, field_name_to_be_replaced, replacement_field_name):
        """
        :param ds_name: influenced ds_name, string
        :param field_name_to_be_replaced: original field name to be replaced, string
        :param replacement_field_name: new field name, string

        Note: rows / cols content is is a bit tricky, because it can have following forms (or any combinations of them):
        [ds_name].[field_name]
        ([ds_name].[field_name1] +|/ [ds_name][field_name2])  # ds_name can be also different for each member
        (([ds_name].[field_name1] +|/ [ds_name][field_name2]) +|/ [ds_name][field_name3])

        Multiple combinations can be multiple times in the content. Best to do this using also ds_name & regex.
        """
        # [ds_name].[xxx:field_name:xx]
        regex_pattern = r"\[{ds}\]\.\[[\w*:]+{fn}:\w*\]".format(ds=ds_name, fn=field_name_to_be_replaced)

        matched_occurrences = re.search(regex_pattern, self._rowsorcolscontent)
        if matched_occurrences:
            matched = matched_occurrences.group(0)
            replacement = matched.replace(field_name_to_be_replaced, replacement_field_name)
            new_content = self._rowsorcolscontent.replace(matched, replacement)
            self.rowsorcolscontent = new_content

class JoinLodExcludeOverrides(object):
    """Describes join-lod-exclude-overrides element in the worksheet."""

    def __init__(self, jeloxml):
        self._xml = jeloxml
        self._columns = list(map(WorksheetBucket, self._xml.findall('./column'))) if self._xml else None

    @property
    def columns(self):
        return self._columns
