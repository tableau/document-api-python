class Query(object):
    """A class for querying the parsed elements of the Tableau Workbook"""
    
    def __init__(self, workbook):
        self._workbook = workbook
        self._xml = workbook._workbookRoot
    
    
    def get_dashboard(self, dashboard_name):
        for dashboard in self._workbook.dashboard_objects:
            if dashboard.name == dashboard_name:
                return dashboard
    
    def get_datasource(self, datasource_name):
        for datasource in self._workbook.datasources:
            if datasource.name == datasource_name:
                return datasource
    
    def get_datasources_for_worksheet(self, worksheet_name):
        worksheet = self.get_worksheet(worksheet_name)
        datasources = []
        for dependency in worksheet.datasource_dependencies:
            datasources.append(dependency.datasource)
        return datasources
    
    def get_field_for_datasource(self, field_name, datasource):
        for field in datasource.fields:
            if field.name == field_name:
                return field
    
    def get_worksheet(self, worksheet_name):
        for worksheet in self._workbook.worksheet_objects:
            if worksheet.name == worksheet_name:
                return worksheet
    
    def get_worksheets_for_dashboard(self, dashboard_name):
        dashboard = self.get_dashboard(dashboard_name)
        worksheet_list = []
        for _ in dashboard.xml.find('zones').findall(".//zone"):
            if 'name' in _.attrib:
                worksheet_list.append(_.attrib['name'])
        return worksheet_list       
    
    def get_column_instances_for_worksheet(self, worksheet_name):
        worksheet = self.get_worksheet(worksheet_name)
        list_of_column_instances = []
        for datasource_dependency in worksheet.datasource_dependencies:
            for column in datasource_dependency.columns:
                context = dict(column.items())
                context['datasource'] = datasource_dependency.datasource
                list_of_column_instances.append(context)
        return list_of_column_instances