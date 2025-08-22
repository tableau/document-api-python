class Query(object):
    """A class for querying the parsed elements of the Tableau Workbook"""
    
    def __init__(self, workbook):
        self._workbook = workbook
        self._xml = workbook._workbookRoot
    
        
    def get_dashboards_for_worksheet(self, worksheet_name):
        dashboards = []
        for _ in self._workbook.dashboard_objects.values():
            if worksheet_name in _.worksheets:
                dashboards.append(_.name)
        return dashboards

    
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