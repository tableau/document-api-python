from tableaudocumentapi.worksheet_datasource_dependecy import DatasourceDependency

class Worksheet(object):
    """A class representing worksheet object."""

    def __init__(self, worksheetXmlElement):
        """Constructor for XMl element representing Tableau worksheet with its children XML elements."""

        self._worksheetXmlElement = worksheetXmlElement
        self._worksheetTableXmlElement = worksheetXmlElement.find('table')
        self._worksheetViewXmlElement = self._worksheetTableXmlElement.find('view')

        self._worksheet_name = worksheetXmlElement.get('name')
        self._layout_options = worksheetXmlElement.find('layout-options')

        self._styles = self._worksheetTableXmlElement.find('style')
        self._panes = self._worksheetTableXmlElement.find('panes')  # encoding & style xml elements
        self._rows = self._worksheetTableXmlElement.find('rows')
        self._cols = self._worksheetTableXmlElement.find('cols')
        self._join_lod_exclude_overrides = self._worksheetTableXmlElement.find('join-lod-exclude-override')

        self._datasources = self._worksheetViewXmlElement.find('datasources')
        self._datasourceDependenciesXmlElement = self._worksheetViewXmlElement.findall('./datasource-dependencies')
        self._datasource_dependencies = list(map(DatasourceDependency, self._datasourceDependenciesXmlElement))
        self._filters = self._worksheetViewXmlElement.findall('./filter')  # each filter can have multiple group filter elements
        self._manual_sorts = self._worksheetViewXmlElement.findall('./manual-sort')
        self._slices = self._worksheetViewXmlElement.find('slices')

        self._dependent_on_datasources = self.get_names_of_dependency_datasources()  # list of names
        self._datasources_dependent_on_columns = self.get_names_of_columns_per_datasource()


    @property
    def worksheet_name(self):
        return self._worksheet_name

    @worksheet_name.setter
    def worksheet_name(self, value):
        self._worksheet_name = value

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

    @layout_options.setter
    def layout_options(self, value):
        self._layout_options = value

    @property
    def styles(self):
        return self._styles

    @styles.setter
    def styles(self, value):
        self._styles = value

    @property
    def panes(self):
        return self._panes

    @panes.setter
    def panes(self, value):
        self._panes = value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    @property
    def cols(self):
        return self._rows

    @cols.setter
    def cols(self, value):
        self._cols = value

    @property
    def join_lod_exclude_overrides(self):
        return self._join_lod_exclude_overrides

    @join_lod_exclude_overrides.setter
    def join_lod_exclude_overrides(self, value):
        self._join_lod_exclude_overrides = value

    @property
    def datasources(self):
        return self._datasources

    @datasources.setter
    def datasources(self, value):
        self._datasources = value

    @property
    def datasources_dependencies(self):
        return self._datasource_dependencies

    @datasources_dependencies.setter
    def datasources_dependencies(self, value):
        self._datasource_dependencies = value

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value

    @property
    def manual_sorts(self):
        return self._manual_sorts

    @manual_sorts.setter
    def manual_sorts(self, value):
        self._manual_sorts = value

    @property
    def slices(self):
        return self._slices

    @slices.setter
    def slices(self, value):
        self._slices = value
