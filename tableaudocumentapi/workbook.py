import weakref
from tableaudocumentapi.dashboard import Dashboard
from tableaudocumentapi.worksheet import Worksheet
from tableaudocumentapi.query import Query
from tableaudocumentapi import Datasource, xfile
from tableaudocumentapi.xfile import xml_open, TableauInvalidFileException
from lxml import etree as ET

class Workbook(object):
    """A class for writing Tableau workbook files."""

    def __init__(self, filename=None, twb_xml_string=None):
        """Open the workbook at `filename`, or as a string. This will handle packaged and unpacked
        workbook files automatically. This will also parse Data Sources and Worksheets
        for access.

        """
        if twb_xml_string is not None:
            if not isinstance(twb_xml_string, str):
                raise TypeError(f"twb_xml_string must be a str")
            root = ET.fromstring(twb_xml_string.encode('utf-8'))
            if root.tag !="workbook":
                raise TableauInvalidFileException(f"Expected 'workbook' tag in xml root, got {root.tag}")
            self._workbookRoot = root
            self._workbookTree = ET.ElementTree(root)
            self._filename = None
        else:
            self._filename = filename
            self._workbookTree = xml_open(self._filename, 'workbook')
            if not self._workbookTree:
                raise TableauInvalidFileException("Workbook file must have a workbook element at root")
            self._workbookRoot = self._workbookTree.getroot()

        self._dashboards = self._prepare_dashboards(self._workbookRoot)
        
        self._dashboard_objects = self._prepare_dashboard_objects(self._workbookRoot)
                                
        self._datasources = self._prepare_datasources(
            self._workbookRoot)

        self._datasource_index = self._prepare_datasource_index(self._datasources)

        self._worksheets = self._prepare_worksheets(
            self._workbookRoot, self._datasource_index)
        
        self._worksheet_objects = self._prepare_worksheet_objects(self._workbookRoot)

        self._shapes = self._prepare_shapes(self._workbookRoot)
        
        self._query = Query(self)

    @property
    def dashboards(self):
        return self._dashboards

    @property
    def dashboard_objects(self):
        return self._dashboard_objects

    @property
    def datasources(self):
        return self._datasources

    @property
    def worksheets(self):
        return self._worksheets
    
    @property
    def worksheet_objects(self):
        return self._worksheet_objects

    @property
    def filename(self):
        return self._filename

    @property
    def shapes(self):
        return self._shapes
    
    @property
    def query(self):
        return self._query

    def save(self):
        """
        Call finalization code and save file.

        Args:
            None.

        Returns:
            Nothing.

        """
        if not self._filename:
            raise TableauInvalidFileException("Cannot use save for workbook created from twb xml string, use save_as(new_filename) instead")
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
        if not new_filename:
            raise TableauInvalidFileException("new filename must be a non-empty path")
        
        if not self._filename:
            xfile._save_file(
                new_filename, self._workbookTree
            )
        else:    
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
    def _prepare_dashboard_objects(xml_root):
        dashboard_objects = {}

        # loop through our dashboards and append
        dashboard_elements = xml_root.find('dashboards')
        if dashboard_elements is None:
            return {}

        for dashboard in dashboard_elements:
            db = Dashboard(dashboard)
            dashboard_objects[db.name] = db

        return dashboard_objects

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
    def _prepare_worksheet_objects(xml_root):
        worksheet_objects = {}

        # loop through our worksheets and add to worksheets dict
        worksheet_elements = xml_root.find('worksheets')
        if worksheet_elements is None:
            return {}

        for worksheet in worksheet_elements:
            wsheet = Worksheet(worksheet)
            worksheet_objects[wsheet.name] = wsheet

        return worksheet_objects

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
    
    