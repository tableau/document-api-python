import re
import pandas as pd
import json
import numpy as np
from tableaudocumentapi.utils import _clean_aggregated_column_names

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
            worksheet_dashboard_map[this_worksheet] = worksheet_dashboard_map[this_worksheet]
        return worksheet_dashboard_map

    def get_worksheet_dependencies(self):
        worksheet_dependencies = []
        for worksheet in self._workbook.worksheet_objects.values():
            for dependency in worksheet.datasource_dependencies:
                for column_instance in dependency.column_instances.values():
                    worksheet_dependencies.append({
                        "Worksheet":worksheet.name,
                        "Datasource":dependency.datasource,
                        "Columns":dependency.columns,
                        "Column_instance":column_instance.get('column'),
                        "Column_instance_Derivation":column_instance.get('derivation'),
                        "Column_instance_Name":column_instance.get('name'),
                        "Column_instance_Pivot":column_instance.get('pivot'),
                        "Column_instance_Type":column_instance.get('type'),
                        "Column_instance_Type":column_instance.get('type'),
                    })
        return worksheet_dependencies
    
    
    def normalize_groupfilter(self, filter_json):    
        # import pdb; pdb.set_trace()
        normalized_groupfilter = pd.json_normalize(filter_json).explode("children").reset_index(drop=True).to_dict(orient="records")
        return normalized_groupfilter
    
    def normalize_worksheet_filters(self, worksheet_filters):
        for worksheet_filter in worksheet_filters:
            if len(worksheet_filter.get('Groupfilters')) > 0:
                worksheet_filter['normalized_groupfilter'] = self.normalize_groupfilter(worksheet_filter.get('Groupfilters'))
        worksheet_filters2 = pd.DataFrame(worksheet_filters).explode('normalized_groupfilter').reset_index(drop=True)
        worksheet_normalized_groupfilter = pd.json_normalize(worksheet_filters2['normalized_groupfilter'])
        col_dict = {}
        for col in worksheet_normalized_groupfilter.columns:
            col_dict[col]= "groupfilter_"+ col
        
        worksheet_normalized_groupfilter.rename(columns=col_dict, inplace=True)
        worksheet_filters = worksheet_filters2.join(worksheet_normalized_groupfilter)
        return worksheet_filters
            
    def get_worksheet_filters(self):
        worksheet_filters = []
        for worksheet in self._workbook.worksheet_objects.values():
            for filter_obj in worksheet.filters:
                worksheet_filters.append({
                    "Worksheet": worksheet.name,
                    "Filter_class": filter_obj.filter_class,
                    "Datasource": filter_obj.datasource,
                    "Column": filter_obj.column,
                    "Groupfilters": filter_obj.groupfilters
                })
            normalized_worksheet_filters = self.normalize_worksheet_filters(worksheet_filters)
        return normalized_worksheet_filters
    
    def get_worksheet_rows(self):
        worksheet_rows = []
        for worksheet in self._workbook.worksheet_objects.values():
            for row in worksheet.rows:
                worksheet_rows.append({
                    "Worksheet": worksheet.name,
                    "Datasource": _clean_aggregated_column_names(row)[0],
                    "Row": _clean_aggregated_column_names(row)[1]                
                })
        return worksheet_rows
    
    def get_worksheet_cols(self):
        worksheet_cols = []
        for worksheet in self._workbook.worksheet_objects.values():
            for col in worksheet.cols:
                worksheet_cols.append({
                    "Worksheet": worksheet.name,
                    "Datasource": _clean_aggregated_column_names(col)[0],
                    "Col": _clean_aggregated_column_names(col)[1]                
                })
        return worksheet_cols
    
    def get_field_objects(self, column, datasource_name = None):
        """Link filter column or worksheets rows/cols to actual Field object from datasource"""
        if not isinstance(column, str) or not column:
            return None
        if datasource_name is None:
            # Extract field name from column reference
            # '[federated.xxx].[Table]' -> 'Table'
            result = re.split(r'(?<=\])\.(?=\[)', column)
            datasource_name = result[0][1:-1]
            field_name = result[1]
        else:
            field_name = column
        # Find matching field in datasources
        for datasource in self._workbook.datasources:
            if datasource_name == datasource.name:
                if field_name in datasource.fields:
                    return datasource.fields[field_name]
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
                        "Worksheets": datasource.fields[field].worksheets,
                        "Members": datasource.fields[field].members
                    })
        return workbook_parameters
    
    def get_workbook_fields(self):
        """Get all non-parameter Fields in a workbook and their attributes as a list of dictionaries"""
        field_attributes = [
            'alias', 'aliases', 'calculation', 'caption', 'datatype', 'default_aggregation',
            'description', 'hidden', 'id', 'is_nominal', 'is_ordinal','is_quantitative', 
            'members','name', 'param_domain_type', 'role', 'table', 'type','value','worksheets']
        workbook_fields = []
        for datasource in self._workbook.datasources:
            fields = datasource.fields
            for key in fields:
                if key.startswith('[') and key.endswith(']'):
                    field_dict = {}
                    field_dict['datasource'] = datasource.name
                    field_dict['datasource_caption'] = datasource.caption
                    field_dict['field_key'] = key
                    for field_attribute in field_attributes:
                        field_dict[field_attribute] = getattr(fields[key],field_attribute)
                    workbook_fields.append(field_dict)
        return workbook_fields
    
    def get_workbook_diff_table(self):
        """Generate a table all workbook dependencies and their attributes"""
        # Join Worksheets with dashboards        
        df_dependencies = pd.DataFrame(self.get_worksheet_dependencies())
        worksheet_dashboard_map = self._get_worksheet_dashboard_map()
        df_worksheet_dashboard_map = pd.DataFrame({"Worksheet":worksheet_dashboard_map.keys(), "Dashboard":worksheet_dashboard_map.values()})
        df_diff = df_dependencies.merge(df_worksheet_dashboard_map, how='left', on='Worksheet')
        
        # Join with Filters
        df_filters = pd.DataFrame(self.get_worksheet_filters())
        df_diff = pd.merge(df_diff, df_filters.add_prefix('_filter_'), left_on = ['Datasource', 'Column_instance', 'Worksheet'], 
                           right_on=['_filter_Datasource', '_filter_Column', '_filter_Worksheet'], how='left')
        # Join with Rows
        df_rows = pd.DataFrame(self.get_worksheet_rows())
        df_diff = pd.merge(df_diff, df_rows.add_prefix('_rows_'), left_on = ['Datasource', 'Column_instance', 'Worksheet'], 
                           right_on=['_rows_Datasource', '_rows_Row', '_rows_Worksheet'], how='left')
        # Join with Cols
        df_cols = pd.DataFrame(self.get_worksheet_cols())
        df_diff = pd.merge(df_diff, df_cols.add_prefix('_cols_'), left_on = ['Datasource', 'Column_instance', 'Worksheet'], 
                           right_on=['_cols_Datasource', '_cols_Col', '_cols_Worksheet'], how='left')
        # Join with fields
        df_fields = pd.DataFrame(self.get_workbook_fields())
        df_diff = pd.merge(df_diff, df_fields.add_prefix('_fields_'), left_on = ['Datasource', 'Column_instance'], 
                           right_on=['_fields_datasource', '_fields_field_key'], how='left')
        return df_diff
    
    @staticmethod
    def json_safe_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns containing dicts/lists/ndarrays to JSON strings (leaves scalars alone)."""
        df = df.copy()
        def to_json_if_needed(x):
            # Convert JSON-serializable containers
            if isinstance(x, (dict, list)):
                return json.dumps(x, ensure_ascii=False)
            # Convert numpy arrays to lists first
            if isinstance(x, np.ndarray):
                return json.dumps(x.tolist(), ensure_ascii=False)
            # Leave everything else (including None/NaN) unchanged
            return x

        # Only touch columns that actually contain container types to avoid overhead
        for col in df.columns:
            if df[col].apply(lambda v: isinstance(v, (dict, list)) or hasattr(v, "__array__")).any():
                df[col] = df[col].apply(to_json_if_needed)
        return df

    def compare_diffs(self, diff_wb1, diff_wb2):
        diff_wb1 = self.json_safe_dataframe(diff_wb1)
        diff_wb2 = self.json_safe_dataframe(diff_wb2)
        df_diff = pd.merge(diff_wb1, diff_wb2, how='outer', indicator=True)
        return df_diff