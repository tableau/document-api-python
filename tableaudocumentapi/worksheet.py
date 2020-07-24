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
        self._datasource_dependencies = self._worksheetViewXmlElement.findall('./datasource-dependencies')
        self._filters = self._worksheetViewXmlElement.findall('./filter')  # each filter can have multiple group filter elements
        self._manual_sorts = self._worksheetViewXmlElement.findall('./manual-sort')
        self._slices = self._worksheetViewXmlElement.find('slices')

        self._dependent_on = self.get_names_of_dependency_datasources(self._datasource_dependencies)


    @property
    def worksheet_name(self):
        return self._worksheet_name

    @worksheet_name.setter
    def worksheet_name(self, value):
        self._worksheet_name = value
    
    @classmethod
    def get_names_of_dependency_datasources(cls, datasource_dependecies_xml):
        return list(ds.get('datasource') for ds in datasource_dependecies_xml)

    @property
    def dependent_on(self):
        return self._dependent_on

    @dependent_on.setter
    def dependent_on(self, value):
        self._dependent_on = value

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