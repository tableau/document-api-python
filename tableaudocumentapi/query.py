import re

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
                for column_instance in dependency.column_instances.values():
                    workbook_dependencies.append({
                        "Workbook":self._workbook.filename,
                        "Dashboard":self._worksheet_dashboard_map.get(worksheet.name),
                        "Worksheet":worksheet.name,
                        "Datasource":dependency.datasource,
                        "Columns":dependency.columns,
                        "Column_instance":column_instance.get('column'),
                        "Column_instance_Derivation":column_instance.get('derivation'),
                        "Column_instance_Name":column_instance.get('name'),
                        "Column_instance_Pivot":column_instance.get('pivot'),
                        "Column_instance_Type":column_instance.get('type')
                    })
        return workbook_dependencies
    
    
    
    def get_workbook_filters(self):
        workbook_filters = []
        for worksheet in self._workbook.worksheet_objects.values():
            for filter_obj in worksheet.filters:
                workbook_filters.append({
                    "Workbook": self._workbook.filename,
                    "Dashboard": self._worksheet_dashboard_map.get(worksheet.name),
                    "Worksheet": worksheet.name,
                    "Filter_class": filter_obj.filter_class,
                    "Column": filter_obj.column,
                    "Groupfilters": filter_obj.groupfilters
                })
        return workbook_filters
    
    
    
    def get_field_objects(self, column):
        """Link filter column or worksheets rows/cols to actual Field object from datasource"""
        
        if not isinstance(column, str) or not column:
            return None

        # Extract field name from column reference
        # '[federated.xxx].[Table]' -> 'Table'
        result = re.split(r'(?<=\])\.(?=\[)', column)
        # Find matching field in datasources
        for datasource in self._workbook.datasources:
            if result[0][1:-1] == datasource.name:
                if result[1] in datasource.fields:
                    return datasource.fields[result[1]]
        return None
    
    def get_workbook_parameters(self):
        """Get all Parameters in workbook and their attributes as a list of dictionaries"""
        workbook_parameters = []
        for datasource in self._workbook.datasources:
            if datasource.name == "Parameters":
                for field in datasource.fields:
                    workbook_parameters.append({
                        "Alias": datasource.fields[field].alias,
                        "Aliases": datasource.fields[field].aliases,
                        "Calculation": datasource.fields[field].calculation,
                        "Caption": datasource.fields[field].caption,
                        "Datatype": datasource.fields[field].datatype,
                        "Name": datasource.fields[field].name,
                        "Parameter_Domain_Type": datasource.fields[field].param_domain_type,
                        "Role": datasource.fields[field].role,
                        "Type": datasource.fields[field].type,
                        "Value": datasource.fields[field].value,
                        "Calculation": datasource.fields[field].calculation,
                        "Worksheets": datasource.fields[field].worksheets,
                        "Members": datasource.fields[field].members
                    })
        return workbook_parameters