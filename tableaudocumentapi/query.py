class Query(object):
    """A class for querying the parsed elements of the Tableau Workbook"""
    
    def __init__(self, workbook):
        self._workbook = workbook
        self._xml = workbook._workbookRoot
    
    
    def get_dashboard(self, dashboard_name):
        for dashboard in self._workbook.dashboard_objects:
            if dashboard.name == dashboard_name:
                return dashboard
    
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
    