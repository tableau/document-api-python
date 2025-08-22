class Query(object):
    """A class for querying the parsed elements of the Tableau Workbook"""
    
    def __init__(self, workbook):
        self._workbook = workbook
        self._xml = workbook._workbookRoot
    
    
    # def get_dashboard(self, dashboard_name):
    #     for dashboard in self._workbook.dashboard_objects:
    #         if dashboard.name == dashboard_name:
    #             return dashboard
    
    # def get_datasource(self, datasource_name):
    #     for datasource in self._workbook.datasources:
    #         if datasource.name == datasource_name:
    #             return datasource
    
    # def get_datasources_for_worksheet(self, worksheet_name):
    #     worksheet = self.get_worksheet(worksheet_name)
    #     datasources = []
    #     for dependency in worksheet.datasource_dependencies:
    #         datasources.append(dependency.datasource)
    #     return datasources
    
    # def get_field_for_datasource(self, field_name, datasource):
    #     for field in datasource.fields:
    #         if field.name == field_name:
    #             return field
    
    # def get_worksheet(self, worksheet_name):
    #     for worksheet in self._workbook.worksheet_objects:
    #         if worksheet.name == worksheet_name:
    #             return worksheet
    
    # def get_worksheets_for_dashboard(self, dashboard_name):
    #     dashboard = self._workbook.dashboard_objects[dashboard_name]
    #     worksheets = {}
    #     for _ in dashboard.xml.find('zones').findall(".//zone"):
    #         if 'name' in _.attrib:
    #             worksheets[_.attrib['name']] = _
    #     return worksheets       
    
    def get_dashboards_for_worksheet(self, worksheet_name):
        dashboards = []
        for _ in self._workbook.dashboard_objects.values():
            if worksheet_name in _.worksheets:
                dashboards.append(_.name)
        return dashboards
    
    # def get_fil(self, worksheet_name):
    #     worksheet = self._workbook.worksheet_objects[worksheet_name]
    #     column_contexts = {}
    #     for datasource_dependency in worksheet.datasource_dependencies:
    #         for column in datasource_dependency.columns:
    #             context = dict(column.items())
    #             context['datasource'] = datasource_dependency.datasource
    #             column_contexts[context
    #     return list_of_column_contexts
    
    def get_workbook_depenencies(self):
        workbook_dependencies = []
        for worksheet in self._workbook.worksheet_objects.values():
            # import pdb; pdb.set_trace()
            if len(self.get_dashboards_for_worksheet(worksheet.name)) == 0:
                dbs = [None]
            else:
                dbs = self.get_dashboards_for_worksheet(worksheet.name)
            for db in dbs:
                for dependency in worksheet.datasource_dependencies:
                    for column in dependency.columns.values():
                        # import pdb; pdb.set_trace()
                        workbook_dependencies.append({
                            "Workbook":self._workbook.filename,
                            "Dashboard":db,
                            "Worksheet":worksheet.name,
                            "Datasource":dependency.datasource,
                            "Field":column.get('name'),
                            "Caption":column.get('caption'),
                            "Datatype":column.get('datatype'),
                            "Role":column.get('role'),
                            "Type":column.get('type')
                        })
        return workbook_dependencies