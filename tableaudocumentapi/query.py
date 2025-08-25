class Query(object):
    """A class for querying the parsed elements of the Tableau Workbook"""
    
    def __init__(self, workbook):
        self._workbook = workbook
        self._xml = workbook._workbookRoot
        self._worksheet_dashboard_map = self._get_worksheet_dashboard_map()
    
        
    def _get_worksheet_dashboard_map(self):
        worksheet_dashboard_map = {}
        for this_worksheet in self._workbook.worksheet_objects:
            worksheet_dashboard_map[this_worksheet] = []
            for dashboard, worksheets_in_dashboard in self._workbook.dashboard_objects.items():
                if this_worksheet in worksheets_in_dashboard.worksheets:
                    worksheet_dashboard_map[this_worksheet].append(dashboard)
        return worksheet_dashboard_map
    

    
    def get_workbook_dependencies(self):
        workbook_dependencies = []
        for worksheet in self._workbook.worksheet_objects.values():
            for dependency in worksheet.datasource_dependencies:
                for column in dependency.columns.values():
                    workbook_dependencies.append({
                        "Workbook":self._workbook.filename,
                        "Dashboard":self._worksheet_dashboard_map.get(worksheet.name),
                        "Worksheet":worksheet.name,
                        "Datasource":dependency.datasource,
                        "Field":column.get('name'),
                        "Caption":column.get('caption'),
                        "Datatype":column.get('datatype'),
                        "Role":column.get('role'),
                        "Type":column.get('type')
                    })
        return workbook_dependencies
    
    