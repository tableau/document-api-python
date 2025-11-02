import re
import pandas as pd
import json
import numpy as np
import tableaudocumentapi
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
                        "Column_instance_Type":column_instance.get('type')
                    })
        return worksheet_dependencies
    
    def normalize_groupfilter(self, filter_json):
        if not filter_json:
            return []
        # Ensure list-of-dicts structure; explode safely
        df = pd.json_normalize(filter_json)
        if 'children' in df.columns:
            df = df.explode('children', ignore_index=True)
        return df.to_dict(orient="records")

    def normalize_worksheet_filters(self, worksheet_filters):
        for wf in worksheet_filters:
            gf = wf.get('Groupfilters') or []
            wf['normalized_groupfilter'] = self.normalize_groupfilter(gf) if gf else []
        # Build frame even if some rows have empty normalized lists
        wf2 = pd.DataFrame(worksheet_filters)
        # Explode safely (empty lists will repeat row once)
        wf2 = wf2.explode('normalized_groupfilter', ignore_index=True)
        wf_norm = pd.json_normalize(wf2['normalized_groupfilter'])
        wf_norm = wf_norm.add_prefix('groupfilter_')
        return wf2.join(wf_norm)

    
    def get_worksheet_filters(self):
        worksheet_filters = []
        for worksheet in self._workbook.worksheet_objects.values():
            for f in worksheet.filters:
                worksheet_filters.append({
                    "Worksheet": worksheet.name,
                    "Filter_class": f.filter_class,
                    "Datasource": f.datasource,
                    "Column": f.column,
                    "Groupfilters": f.groupfilters
                })
        return self.normalize_worksheet_filters(worksheet_filters)

    
    def get_worksheet_rows(self):
        out = []
        for ws in self._workbook.worksheet_objects.values():
            for r in ws.rows:
                ds_name, row_name = _clean_aggregated_column_names(r) or (None, None)
                out.append({"Worksheet": ws.name, "Datasource": ds_name, "Row": row_name})
        return out

    def get_worksheet_cols(self):
        out = []
        for ws in self._workbook.worksheet_objects.values():
            for c in ws.cols:
                ds_name, col_name = _clean_aggregated_column_names(c) or (None, None)
                out.append({"Worksheet": ws.name, "Datasource": ds_name, "Col": col_name})
        return out

        
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
        """All non-parameter fields (+ attributes)."""
        field_attrs = [
            'alias','aliases','calculation','caption','datatype','default_aggregation',
            'description','hidden','id','is_nominal','is_ordinal','is_quantitative',
            'members','name','param_domain_type','role','table','type','value','worksheets'
        ]
        rows = []
        for ds in self._workbook.datasources:
            if ds.name == "Parameters":
                continue
            for key, field in ds.fields.items():
                if isinstance(key, str) and key.startswith('[') and key.endswith(']'):
                    row = {
                        'datasource': ds.name,
                        'datasource_caption': getattr(ds, 'caption', None),
                        'field_key': key,
                    }
                    for attr in field_attrs:
                        row[attr] = getattr(field, attr, None)
                    rows.append(row)
        return rows

    
    def get_workbook_diff_table(self):
        df_dep = pd.DataFrame(self.get_worksheet_dependencies())

        ws_db_map = self._get_worksheet_dashboard_map()
        df_wsdb = pd.DataFrame({
            "Worksheet": list(ws_db_map.keys()),
            "Dashboard": list(ws_db_map.values())
        })
        df = df_dep.merge(df_wsdb, how='left', on='Worksheet')

        df_filters = pd.DataFrame(self.get_worksheet_filters())
        if not df_filters.empty:
            df = df.merge(df_filters.add_prefix('_filter_'),
                        left_on=['Datasource','Column_instance','Worksheet'],
                        right_on=['_filter_Datasource','_filter_Column','_filter_Worksheet'],
                        how='left')

        df_rows = pd.DataFrame(self.get_worksheet_rows())
        if not df_rows.empty:
            df = df.merge(df_rows.add_prefix('_rows_'),
                        left_on=['Datasource','Column_instance','Worksheet'],
                        right_on=['_rows_Datasource','_rows_Row','_rows_Worksheet'],
                        how='left')

        df_cols = pd.DataFrame(self.get_worksheet_cols())
        if not df_cols.empty:
            df = df.merge(df_cols.add_prefix('_cols_'),
                        left_on=['Datasource','Column_instance','Worksheet'],
                        right_on=['_cols_Datasource','_cols_Col','_cols_Worksheet'],
                        how='left')

        df_fields = pd.DataFrame(self.get_workbook_fields())
        if not df_fields.empty:
            df = df.merge(df_fields.add_prefix('_fields_'),
                        left_on=['Datasource','Column_instance'],
                        right_on=['_fields_datasource','_fields_field_key'],
                        how='left')
        return df

    
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
    
    @staticmethod
    def compare_diffs(wb1_filename, wb2_filename, wb1_twb_string=None, wb2_twb_string=None):
        from tableaudocumentapi import Workbook

        if wb1_twb_string:
            d1 = Workbook(twb_xml_string=wb1_twb_string).query.get_workbook_diff_table()
        else:
            d1 = Workbook(wb1_filename).query.get_workbook_diff_table()

        if wb2_twb_string:
            d2 = Workbook(twb_xml_string=wb2_twb_string).query.get_workbook_diff_table()
        else:
            d2 = Workbook(wb2_filename).query.get_workbook_diff_table()

        d1 = Query.json_safe_dataframe(d1)
        d2 = Query.json_safe_dataframe(d2)

        # Partition columns
        def split_cols(cols):
            id_cols = [c for c in cols if isinstance(c, str) and c and c[0] != '_']
            val_cols = [c for c in cols if isinstance(c, str) and c and c[0] == '_']
            # If nothing qualifies as id, keep at least 'Worksheet' and 'Datasource' if present
            if not id_cols:
                id_cols = [c for c in ['Worksheet','Datasource','Column_instance'] if c in cols]
            return id_cols, val_cols

        id1, val1 = split_cols(d1.columns)
        id2, val2 = split_cols(d2.columns)

        d1m = d1.melt(id_vars=id1, value_vars=val1) if val1 else d1
        d2m = d2.melt(id_vars=id2, value_vars=val2) if val2 else d2

        out = pd.merge(d1m, d2m, how='outer', indicator=True)
        out = out.rename(columns={'_merge': 'Workbook_Source'})
        out['Workbook_Source'] = out['Workbook_Source'].map({
            'left_only': 'wb1',
            'right_only': 'wb2',
            'both': 'both'
        })
        return out.drop_duplicates()
