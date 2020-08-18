from tableaudocumentapi.worksheet_view_subelements import DatasourceDependency, Filter, SliceColumn, Sort
from tableaudocumentapi.worksheet_subelements import LayoutOptions, WorksheetPane, WorksheetStyleRule, WorksheetRowsOrCols

class Worksheet(object):
    """A class representing worksheet object."""

    def __init__(self, worksheetXmlElement):
        """Constructor for XMl element representing Tableau worksheet with its children XML elements."""

        self._worksheetXmlElement = worksheetXmlElement
        self._worksheetTableXmlElement = worksheetXmlElement.find('table')
        self._worksheetViewXmlElement = self._worksheetTableXmlElement.find('view')

        self._worksheet_name = worksheetXmlElement.get('name')
        self._layout_options = LayoutOptions(worksheetXmlElement.find('layout-options'))

        self._styles = list(map(WorksheetStyleRule, self._worksheetTableXmlElement.findall('./style/style-rule')))
        self._panes = list(map(WorksheetPane, self._worksheetTableXmlElement.findall('./panes/pane')))
        self._rows = WorksheetRowsOrCols( self._worksheetTableXmlElement.find('rows'))
        self._cols = WorksheetRowsOrCols(self._worksheetTableXmlElement.find('cols'))
        self._join_lod_exclude_overrides = self._worksheetTableXmlElement.find('join-lod-exclude-override')

        self._datasources = self._worksheetViewXmlElement.find('datasources')
        self._datasource_dependencies = list(map(DatasourceDependency, self._worksheetViewXmlElement.findall('./datasource-dependencies')))
        self._filters = list(map(Filter, self._worksheetViewXmlElement.findall('./filter')))
        self._manual_sorts = self._worksheetViewXmlElement.findall('./manual-sort') # TODO
        self._sorts = list(map(Sort, self._worksheetViewXmlElement.findall('./sort')))
        self._slices_columns = list(map(SliceColumn, self._worksheetViewXmlElement.findall('./slices/column')))

        self._dependent_on_datasources = self.get_names_of_dependency_datasources()  # list of names
        self._datasources_dependent_on_columns = self.get_names_of_columns_per_datasource()


    @property
    def worksheet_name(self):
        return self._worksheet_name

    @classmethod
    def get_names_of_dependency_datasources(cls):
        datasource_names = list(dsxml.find('datasource').get('name') for dsxml in cls.datasources)
        print(datasource_names)
        return datasource_names

    @classmethod
    def get_names_of_columns_per_datasource(cls):
        names_per_ds = {}

        # loop through the list of the names of the datasources
        for ds in cls.dependent_on_datasources:
            # check against dependent columns and create a map (dictionary)
            for ds_dep in cls.datasources_dependencies:
                if ds_dep.dependency_datasource_name == ds:
                    # column name is enough as it seems that the columns mirror column instances in this case
                    names_per_ds[ds] = list(cl.name for cl in ds_dep.columns)
        return names_per_ds

    @property
    def dependent_on_datasources(self):
        """List of data source names on which the worksheet is dependent.
            :rtype: list()
        """
        return self._dependent_on_datasources

    @property
    def datasources_dependent_on_columns(self, ):
        """Dictionary of data source names on which the worksheet is dependent together with columns of the data sources.
           keys: data source names.
           values: list of column names
        """
        return self._datasources_dependent_on_columns

    @property
    def layout_options(self):
        return self._layout_options

    @property
    def styles(self):
        return self._styles

    @property
    def panes(self):
        return self._panes

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._rows

    @property
    def join_lod_exclude_overrides(self):
        return self._join_lod_exclude_overrides

    @property
    def datasources(self):
        return self._datasources

    @property
    def datasources_dependencies(self):
        return self._datasource_dependencies

    @property
    def filters(self):
        return self._filters

    @property
    def manual_sorts(self):
        return self._manual_sorts

    @property
    def sort(self):
        return self._sorts

    @property
    def slices_columns(self):
        return self._slices_columns
