import weakref
import re

from tableaudocumentapi import Datasource, Field, xfile
from tableaudocumentapi.xfile import xml_open, TableauInvalidFileException

def _remove_brackets(text):
    return text.lstrip("[").rstrip("]")

def _clean_columns(marks):
    """
    Extract rows/cols data that is stored such as [datasource].[column]
    We use a regex to find multiple marks and another regex to extract the field name

    We return a dictionary of datasource: [fields] so we can map them to field items
    """
    if marks is None:
        return None
    # find all [datasource].[column] strings by positive lookahead of ), space, or string end
    # some will have three parts so we need to use a lookahead to ensure we capture the entire object
    matching_marks = re.findall(r"(\[.*?\])(?=\)|\s|$)",str(marks))
    datasource_fields = {}
    for mark in matching_marks:
        # split column into datasource and field display
        column = mark.split("].[")
        datasource = _remove_brackets(column[0])
        # initialize dictionary entry
        if datasource not in datasource_fields:
            datasource_fields[datasource] = []
        # the field is always the last item in the list
        field_display = _remove_brackets(column[-1])
        # use ordinal (ok), quantitative (qk), nominal (nk), or string end as lookahead
        field_match = re.match(r".*?(?<=:)([^:]+)(?=:ok|:qk|:nk|$)", field_display)
        # if no match, eg. Measure Names, just return the string
        if field_match:
            field = field_match.groups(1)[0]
        else:
            field = field_display
        datasource_fields[datasource].append(field)
    return datasource_fields

def _ds_fields_to_tems(ds_fields, ds_index):
    fields = []
    for ds, field_ids in ds_fields.items():
        fields_dict = ds_index[ds].fields
        for field_id in field_ids:
            # many field ids include brackets, so we need to check for these as well
            field_id_brackets = f"[{field_id}]"
            if field_id in fields_dict:
                field = fields_dict.get(field_id)
            elif field_id_brackets in fields_dict:
                field = fields_dict.get(field_id_brackets)
            else:
                field = field_id
            fields.append(field)
    return fields

class Worksheet(object):
    """
    A class to parse key attributes of a worksheet.
    """

    def __init__(self, worksheet_element, ds_index):
        self._worksheetRoot = worksheet_element
        self.name = worksheet_element.attrib['name']
        self._datasource_index = ds_index
        self._datasources = self._prepare_datasources(self._worksheetRoot, self._datasource_index)
        self._fields = self._prepare_datasource_dependencies(self._worksheetRoot)
        self._rows = self._prepare_rows(self._worksheetRoot, self._datasource_index)
        self._cols = self._prepare_cols(self._worksheetRoot, self._datasource_index)
        self._filter_fields = self._prepare_filter_fields(self._worksheetRoot, self._datasource_index)

    def __repr__(self):
        name = self.name
        datasources = ", ".join([ds.caption or ds.name for ds in self._datasources])
        fields = ", ".join([f.name for f in self._fields])
        return f"name: {name}, datasources: {datasources}, fields: {fields}"
    
    def __iter__(self):
        keys = self.__dict__.keys()
        filtered_keys = [key for key in keys if key != "_worksheetRoot"]
        for key in filtered_keys:
            yield key.lstrip("_"), getattr(self, key)

    @staticmethod
    def _prepare_filter_fields(worksheet_element, ds_index):
        filters = []
        slices_list = worksheet_element.find(".//slices")
        if slices_list is None:
            return filters
        slices = [column.text for column in slices_list]
        # combine slices into single string to use same function as rows/cols
        ds_fields = _clean_columns(" ".join(slices))
        if ds_fields == None or len(ds_fields) == 0:
            return None
        fields = _ds_fields_to_tems(ds_fields, ds_index)
        return fields
    
    @staticmethod
    def _prepare_datasources(worksheet_element, ds_index):
        worksheet_datasources = worksheet_element.find(".//datasources")
        datasource_names = [ds.attrib["name"] for ds in worksheet_datasources]
        datasource_list = [ds_index[name] for name in datasource_names]
        return datasource_list
    
    @property
    def datasources(self):
        return self._datasources
    
    @staticmethod
    def _prepare_datasource_dependencies(worksheet_element):
        dependencies = worksheet_element.findall('.//datasource-dependencies')
        for dependency in dependencies:
            columns = dependency.findall('.//column')
            return [Field.from_column_xml(column) for column in columns]
    
    @property
    def fields(self):
        return self._prepare_datasource_dependencies
    
    @property
    def fields_list(self):
        return [field.caption for field in self._fields]
    
    @staticmethod
    def _prepare_rows(worksheet_element, ds_index):
        rows = worksheet_element.find('.//rows')
        ds_fields = _clean_columns(rows.text)
        if ds_fields == None or len(ds_fields) == 0:
            return None
        fields = _ds_fields_to_tems(ds_fields, ds_index)
        return fields
    
    @staticmethod
    def _prepare_cols(worksheet_element, ds_index):
        cols = worksheet_element.find('.//cols')
        ds_fields = _clean_columns(cols.text)
        if ds_fields == None or len(ds_fields) == 0:
            return None
        fields = _ds_fields_to_tems(ds_fields, ds_index)
        return fields
    
    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols
    
    @property
    def filter_fields(self):
        return self._filter_fields
    
class Workbook(object):
    """A class for writing Tableau workbook files."""

    def __init__(self, filename):
        """Open the workbook at `filename`. This will handle packaged and unpacked
        workbook files automatically. This will also parse Data Sources and Worksheets
        for access.

        """

        self._filename = filename

        self._workbookTree = xml_open(self._filename, 'workbook')
        if not self._workbookTree:
            raise TableauInvalidFileException("Workbook file must have a workbook element at root")

        self._workbookRoot = self._workbookTree.getroot()

        self._dashboards = self._prepare_dashboards(self._workbookRoot)

        self._datasources = self._prepare_datasources(
            self._workbookRoot)

        self._datasource_index = self._prepare_datasource_index(self._datasources)

        self._worksheets = self._prepare_worksheets(
            self._workbookRoot, self._datasource_index)
        
        self._worksheet_items = self._prepare_worksheet_items(self._workbookRoot, self._datasource_index)

        self._shapes = self._prepare_shapes(self._workbookRoot)

    @property
    def dashboards(self):
        return self._dashboards

    @property
    def datasources(self):
        return self._datasources

    @property
    def worksheets(self):
        return self._worksheets
    
    @property
    def worksheet_items(self):
        return self._worksheet_items

    @property
    def filename(self):
        return self._filename

    @property
    def shapes(self):
        return self._shapes

    def save(self):
        """
        Call finalization code and save file.

        Args:
            None.

        Returns:
            Nothing.

        """

        # save the file
        xfile._save_file(self._filename, self._workbookTree)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        xfile._save_file(
            self._filename, self._workbookTree, new_filename)

    @staticmethod
    def _prepare_datasource_index(datasources):
        retval = weakref.WeakValueDictionary()
        for datasource in datasources:
            retval[datasource.name] = datasource

        return retval

    @staticmethod
    def _prepare_datasources(xml_root):
        datasources = []

        # loop through our datasources and append
        datasource_elements = xml_root.find('datasources')
        if datasource_elements is None:
            return []

        for datasource in datasource_elements:
            ds = Datasource(datasource)
            datasources.append(ds)

        return datasources

    @staticmethod
    def _prepare_dashboards(xml_root):
        dashboards = []

        dashboard_elements = xml_root.find('.//dashboards')
        if dashboard_elements is None:
            return []

        for dash_element in dashboard_elements:
            dash_name = dash_element.attrib['name']
            dashboards.append(dash_name)

        return dashboards

    @staticmethod
    def _prepare_worksheets(xml_root, ds_index):
        worksheets = []
        worksheets_element = xml_root.find('.//worksheets')
        if worksheets_element is None:
            return worksheets

        for worksheet_element in worksheets_element:
            worksheet_name = worksheet_element.attrib['name']
            worksheets.append(worksheet_name)  # TODO: A real worksheet object, for now, only name

            dependencies = worksheet_element.findall('.//datasource-dependencies')

            for dependency in dependencies:
                datasource_name = dependency.attrib['datasource']
                datasource = ds_index[datasource_name]
                for column in dependency.findall('.//column'):
                    column_name = column.attrib['name']
                    if column_name in datasource.fields:
                        datasource.fields[column_name].add_used_in(worksheet_name)

        return worksheets
    
    @staticmethod
    def _prepare_worksheet_items(xml_root, ds_index):
        worksheets = []
        worksheets_element = xml_root.find('.//worksheets')
        if worksheets_element is None:
            return worksheets
        worksheets = [Worksheet(worksheet_element, ds_index) for worksheet_element in worksheets_element]
        return worksheets
    
    @staticmethod
    def _prepare_shapes(xml_root):
        shapes = []
        worksheets_element = xml_root.find('.//external/shapes')
        if worksheets_element is None:
            return shapes

        for worksheet_element in worksheets_element:
            shape_name = worksheet_element.attrib['name']
            shapes.append(shape_name)

        return shapes
