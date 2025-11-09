"""
Test suite for Version 012 new features of the Tableau Document API.

This test file comprehensively tests all new features added in v012:

1. Dashboard Objects (TestDashboardObjects)
   - dashboard_objects property on Workbook
   - Dashboard class with name, xml, worksheets, datasource_dependencies properties

2. Worksheet Objects (TestWorksheetObjects)
   - worksheet_objects property on Workbook
   - Worksheet class with name, xml, id, datasource_dependencies, filters, rows, cols properties

3. DatasourceDependency Objects (TestDatasourceDependencyObjects)
   - DatasourceDependency class with datasource, xml, columns, column_instances properties
   - Separation of dependencies from field definitions

4. Filter Objects (TestFilterObjects)
   - Filter class with filter_class, xml, column, datasource, groupfilters properties
   - Support for both worksheet and datasource level filters
   - Nested groupfilter structure parsing

5. Query Interface (TestQueryObjects)
   - Query object accessible via workbook.query
   - get_worksheet_dependencies() - returns list of all dependencies
   - get_worksheet_filters() - returns DataFrame with normalized groupfilters
   - get_worksheet_rows() - returns row field references with datasource mapping
   - get_worksheet_cols() - returns column field references with datasource mapping
   - get_workbook_fields() - returns all non-parameter fields with attributes
   - get_workbook_metadata_table() - generates comprehensive metadata table
   - normalize_groupfilter() - flattens nested filter structures

6. Workbook Comparison (TestQueryComparisonMethods)
   - Query.compare_diffs() - static method to compare two workbooks
   - Support for both file paths and XML strings as input
   - Returns DataFrame with 'Workbook_Source' column (wb1/wb2/both)
   - Query.json_safe_dataframe() - converts complex types to JSON strings

7. Utility Functions (TestUtils)
   - _clean_aggregated_column_names() now returns tuple (datasource, field)
   - Support for 'usr' aggregation prefix
   - Proper handling of empty/None inputs

8. Backward Compatibility (TestBackwardsCompatibility)
   - Original dashboards, worksheets, datasources properties still work
   - Names match between old list properties and new object dictionaries

9. XML String Input (TestXMLStringInput)
   - Workbook can be created from TWB XML string
   - Integration with Tableau Server Client and REST API
   - save() raises error for XML-created workbooks
   - save_as() works with new filename

10. Parameter Support (TestParameterFunctionality)
    - get_workbook_parameters() method on Query
    - Extracts parameter attributes: value, param_domain_type, members

11. Enhanced Field Properties (TestNewFieldProperties)
    - Field.value - parameter default value
    - Field.param_domain_type - parameter domain type
    - Field.members - parameter member values
    - Field.table - datasource table for columns
    - create_field_xml() supports parameter attributes
"""

import unittest
import os.path

from tableaudocumentapi import Workbook
from tableaudocumentapi.dashboard import Dashboard
from tableaudocumentapi.worksheet import Worksheet
from tableaudocumentapi.filter import Filter
from tableaudocumentapi.datasource_dependency import DatasourceDependency
from tableaudocumentapi.query import Query
from tableaudocumentapi.utils import _clean_aggregated_column_names

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)

TEST_SUPERSTORE_FILE = os.path.join(TEST_ASSET_DIR, 'US_Superstore_10.0.twbx')


class TestNewFeaturesFileAvailability(unittest.TestCase):
    """Test that the required test file exists before running other tests"""
    
    def test_superstore_file_exists(self):
        """Test that US_Superstore_10.0.twbx exists"""
        self.assertTrue(os.path.exists(TEST_SUPERSTORE_FILE), 
                       f"Test file {TEST_SUPERSTORE_FILE} does not exist")


class TestDashboardObjects(unittest.TestCase):
    """Test Dashboard objects using US Superstore file"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_workbook_has_dashboard_objects_property(self):
        """Test that workbook has dashboard_objects property"""
        self.assertTrue(hasattr(self.wb, 'dashboard_objects'))
        self.assertIsInstance(self.wb.dashboard_objects, dict)
        
    def test_dashboard_objects_are_dashboard_instances(self):
        """Test that dashboard objects are Dashboard instances"""
        for dashboard_name, dashboard in self.wb.dashboard_objects.items():
            with self.subTest(dashboard_name=dashboard_name):
                self.assertIsInstance(dashboard, Dashboard)
                self.assertIsInstance(dashboard_name, str)
                self.assertEqual(dashboard.name, dashboard_name)
                
    def test_dashboard_has_required_properties(self):
        """Test that Dashboard objects have all expected properties"""
        self.assertGreater(len(self.wb.dashboard_objects), 0, 
                          "Superstore file should have at least one dashboard")
        
        dashboard = next(iter(self.wb.dashboard_objects.values()))
        self.assertTrue(hasattr(dashboard, 'name'))
        self.assertTrue(hasattr(dashboard, 'xml'))
        self.assertTrue(hasattr(dashboard, 'worksheets'))
        self.assertTrue(hasattr(dashboard, 'datasource_dependencies'))
        self.assertIsNotNone(dashboard.xml)
        
    def test_dashboard_worksheets_property(self):
        """Test dashboard worksheets property"""
        for dashboard in self.wb.dashboard_objects.values():
            with self.subTest(dashboard=dashboard.name):
                self.assertIsInstance(dashboard.worksheets, list)
                # Each worksheet name should be a string
                for worksheet_name in dashboard.worksheets:
                    self.assertIsInstance(worksheet_name, str)
                    
    def test_dashboard_datasource_dependencies_property(self):
        """Test dashboard datasource_dependencies property"""
        for dashboard in self.wb.dashboard_objects.values():
            with self.subTest(dashboard=dashboard.name):
                self.assertIsInstance(dashboard.datasource_dependencies, list)
                for dep in dashboard.datasource_dependencies:
                    self.assertIsInstance(dep, DatasourceDependency)
                    
    def test_dashboard_xml_property(self):
        """Test dashboard xml property returns valid XML element"""
        for dashboard in self.wb.dashboard_objects.values():
            with self.subTest(dashboard=dashboard.name):
                xml = dashboard.xml
                self.assertIsNotNone(xml)
                self.assertEqual(xml.tag, 'dashboard')
                self.assertEqual(xml.get('name'), dashboard.name)


class TestWorksheetObjects(unittest.TestCase):
    """Test Worksheet objects using US Superstore file"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_workbook_has_worksheet_objects_property(self):
        """Test that workbook has worksheet_objects property"""
        self.assertTrue(hasattr(self.wb, 'worksheet_objects'))
        self.assertIsInstance(self.wb.worksheet_objects, dict)
        
    def test_worksheet_objects_are_worksheet_instances(self):
        """Test that worksheet objects are Worksheet instances"""
        self.assertGreater(len(self.wb.worksheet_objects), 0,
                          "Superstore file should have at least one worksheet")
        
        for worksheet_name, worksheet in self.wb.worksheet_objects.items():
            with self.subTest(worksheet_name=worksheet_name):
                self.assertIsInstance(worksheet, Worksheet)
                self.assertIsInstance(worksheet_name, str)
                self.assertEqual(worksheet.name, worksheet_name)
                
    def test_worksheet_has_required_properties(self):
        """Test that Worksheet objects have all expected properties"""
        worksheet = next(iter(self.wb.worksheet_objects.values()))
        
        properties = ['name', 'xml', 'id', 'datasource_dependencies', 'filters', 'rows', 'cols']
        for prop in properties:
            with self.subTest(property=prop):
                self.assertTrue(hasattr(worksheet, prop))
                
    def test_worksheet_properties_return_correct_types(self):
        """Test that worksheet properties return expected types"""
        for worksheet in self.wb.worksheet_objects.values():
            with self.subTest(worksheet=worksheet.name):
                self.assertIsInstance(worksheet.name, str)
                self.assertIsInstance(worksheet.id, str)
                self.assertIsInstance(worksheet.datasource_dependencies, list)
                self.assertIsInstance(worksheet.filters, list)
                self.assertIsInstance(worksheet.rows, list)
                self.assertIsInstance(worksheet.cols, list)
                
    def test_worksheet_id_extraction(self):
        """Test worksheet ID extraction"""
        for worksheet in self.wb.worksheet_objects.values():
            with self.subTest(worksheet=worksheet.name):
                # ID should be string (empty if no simple-id element)
                self.assertIsInstance(worksheet.id, str)
                # If ID exists, it should not contain curly braces
                if worksheet.id:
                    self.assertNotIn('{', worksheet.id)
                    self.assertNotIn('}', worksheet.id)
                    
    def test_worksheet_dependencies_contain_datasource_dependency_objects(self):
        """Test that worksheet dependencies contain DatasourceDependency objects"""
        for worksheet in self.wb.worksheet_objects.values():
            with self.subTest(worksheet=worksheet.name):
                for dep in worksheet.datasource_dependencies:
                    self.assertIsInstance(dep, DatasourceDependency)
                    
    def test_worksheet_filters_contain_filter_objects(self):
        """Test that worksheet filters contain Filter objects"""
        for worksheet in self.wb.worksheet_objects.values():
            with self.subTest(worksheet=worksheet.name):
                for filter_obj in worksheet.filters:
                    self.assertIsInstance(filter_obj, Filter)
                    
    def test_worksheet_rows_cols_parsing(self):
        """Test that rows and cols are properly parsed and cleaned"""
        for worksheet in self.wb.worksheet_objects.values():
            with self.subTest(worksheet=worksheet.name):
                # Rows and cols should be lists
                self.assertIsInstance(worksheet.rows, list)
                self.assertIsInstance(worksheet.cols, list)
                
                # Each item in rows/cols should be a string (cleaned column reference)
                for row in worksheet.rows:
                    self.assertIsInstance(row, str)
                for col in worksheet.cols:
                    self.assertIsInstance(col, str)


class TestDatasourceDependencyObjects(unittest.TestCase):
    """Test DatasourceDependency objects using US Superstore file"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_datasource_dependency_properties(self):
        """Test DatasourceDependency properties"""
        dependencies = []
        for worksheet in self.wb.worksheet_objects.values():
            dependencies.extend(worksheet.datasource_dependencies)
            
        self.assertGreater(len(dependencies), 0, 
                          "Superstore should have datasource dependencies")
        
        for dep in dependencies:
            with self.subTest(datasource=dep.datasource):
                self.assertTrue(hasattr(dep, 'datasource'))
                self.assertTrue(hasattr(dep, 'xml'))
                self.assertTrue(hasattr(dep, 'columns'))
                self.assertTrue(hasattr(dep, 'column_instances'))
                
    def test_datasource_dependency_columns_is_list(self):
        """Test that columns property returns a list"""
        dependencies = []
        for worksheet in self.wb.worksheet_objects.values():
            dependencies.extend(worksheet.datasource_dependencies)
            
        for dep in dependencies:
            with self.subTest(datasource=dep.datasource):
                self.assertIsInstance(dep.columns, list)
                # Each column should be a string
                for column in dep.columns:
                    self.assertIsInstance(column, str)
                    
    def test_datasource_dependency_column_instances_is_dict(self):
        """Test that column_instances property returns a dict"""
        dependencies = []
        for worksheet in self.wb.worksheet_objects.values():
            dependencies.extend(worksheet.datasource_dependencies)
            
        for dep in dependencies:
            with self.subTest(datasource=dep.datasource):
                self.assertIsInstance(dep.column_instances, dict)
                # Each value should be a dict of attributes
                for column_ref, attributes in dep.column_instances.items():
                    self.assertIsInstance(column_ref, str)
                    self.assertIsInstance(attributes, dict)
                    
    def test_datasource_dependency_datasource_property(self):
        """Test datasource property"""
        dependencies = []
        for worksheet in self.wb.worksheet_objects.values():
            dependencies.extend(worksheet.datasource_dependencies)
            
        for dep in dependencies:
            # Datasource should be string or None
            self.assertTrue(dep.datasource is None or isinstance(dep.datasource, str))


class TestFilterObjects(unittest.TestCase):
    """Test Filter objects using US Superstore file"""

    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)

    def test_datasource_has_filters_property(self):
        """Test that datasources have filters property"""
        for datasource in self.wb.datasources:
            with self.subTest(datasource=datasource.name):
                self.assertTrue(hasattr(datasource, 'filters'))
                self.assertIsInstance(datasource.filters, list)
                # Each filter should be a Filter object
                for filter_obj in datasource.filters:
                    self.assertIsInstance(filter_obj, Filter)
        
    def test_filter_properties(self):
        """Test Filter properties"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)

        if filters:  # Only test if filters exist
            for filter_obj in filters:
                with self.subTest(filter_class=filter_obj.filter_class):
                    self.assertTrue(hasattr(filter_obj, 'filter_class'))
                    self.assertTrue(hasattr(filter_obj, 'xml'))
                    self.assertTrue(hasattr(filter_obj, 'column'))
                    self.assertTrue(hasattr(filter_obj, 'datasource'))
                    self.assertTrue(hasattr(filter_obj, 'groupfilters'))
                    
    def test_filter_groupfilters_is_list(self):
        """Test that groupfilters property returns a list"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)
            
        for filter_obj in filters:
            with self.subTest(filter_class=filter_obj.filter_class):
                self.assertIsInstance(filter_obj.groupfilters, list)
                
    def test_filter_column_is_string(self):
        """Test that column property returns a string (cleaned column name)"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)

        for filter_obj in filters:
            with self.subTest(filter_class=filter_obj.filter_class):
                # Column should be a string or None
                self.assertTrue(filter_obj.column is None or isinstance(filter_obj.column, str))

    def test_filter_datasource_property(self):
        """Test that datasource property returns a string"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)

        for filter_obj in filters:
            with self.subTest(filter_class=filter_obj.filter_class):
                # Datasource should be a string or None
                self.assertTrue(filter_obj.datasource is None or isinstance(filter_obj.datasource, str))
                    
    def test_filter_groupfilter_structure(self):
        """Test groupfilter structure"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)
            
        for filter_obj in filters:
            for groupfilter in filter_obj.groupfilters:
                with self.subTest(filter_class=filter_obj.filter_class):
                    self.assertIsInstance(groupfilter, dict)
                    # Should have basic structure keys
                    expected_keys = ['function', 'level', 'member', 'attributes', 'children']
                    for key in expected_keys:
                        self.assertIn(key, groupfilter)
                    self.assertIsInstance(groupfilter['children'], list)
                    self.assertIsInstance(groupfilter['attributes'], dict)


class TestQueryObjects(unittest.TestCase):
    """Test Query objects using US Superstore file"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_workbook_has_query_property(self):
        """Test that workbook has query property"""
        self.assertTrue(hasattr(self.wb, 'query'))
        self.assertIsInstance(self.wb.query, Query)
        
    def test_query_get_worksheet_dependencies_returns_list(self):
        """Test that get_worksheet_dependencies returns a list"""
        dependencies = self.wb.query.get_worksheet_dependencies()
        self.assertIsInstance(dependencies, list)

    def test_query_get_worksheet_filters_returns_dataframe(self):
        """Test that get_worksheet_filters returns a DataFrame"""
        import pandas as pd
        filters = self.wb.query.get_worksheet_filters()
        self.assertIsInstance(filters, pd.DataFrame)
        
    def test_query_dependency_structure(self):
        """Test structure of dependency objects returned by query"""
        dependencies = self.wb.query.get_worksheet_dependencies()
        if dependencies:
            dep = dependencies[0]
            required_keys = [
                "Worksheet", "Datasource",
                "Columns", "Column_instance", "Column_instance_Derivation",
                "Column_instance_Name", "Column_instance_Pivot", "Column_instance_Type"
            ]
            for key in required_keys:
                with self.subTest(key=key):
                    self.assertIn(key, dep)

    def test_query_filter_structure(self):
        """Test structure of filter objects returned by query"""
        import pandas as pd
        filters = self.wb.query.get_worksheet_filters()
        if not filters.empty:
            # Check DataFrame columns
            expected_columns = ["Worksheet", "Filter_class", "Column", "Datasource"]
            for col in expected_columns:
                with self.subTest(column=col):
                    self.assertIn(col, filters.columns)
                    
    def test_query_get_field_objects_with_invalid_input(self):
        """Test get_field_objects with invalid input"""
        query = self.wb.query
        
        # Test with None
        result = query.get_field_objects(None)
        self.assertIsNone(result)
        
        # Test with empty string
        result = query.get_field_objects("")
        self.assertIsNone(result)
        
        # Test with non-string
        result = query.get_field_objects(123)
        self.assertIsNone(result)
        
    def test_query_get_worksheet_rows(self):
        """Test that get_worksheet_rows returns a list"""
        rows = self.wb.query.get_worksheet_rows()
        self.assertIsInstance(rows, list)
        if rows:
            row = rows[0]
            self.assertIn("Worksheet", row)
            self.assertIn("Datasource", row)
            self.assertIn("Row", row)

    def test_query_get_worksheet_cols(self):
        """Test that get_worksheet_cols returns a list"""
        cols = self.wb.query.get_worksheet_cols()
        self.assertIsInstance(cols, list)
        if cols:
            col = cols[0]
            self.assertIn("Worksheet", col)
            self.assertIn("Datasource", col)
            self.assertIn("Col", col)

    def test_query_get_workbook_fields(self):
        """Test that get_workbook_fields returns a list"""
        fields = self.wb.query.get_workbook_fields()
        self.assertIsInstance(fields, list)
        if fields:
            field = fields[0]
            # Check for some expected keys
            self.assertIn("datasource", field)
            self.assertIn("field_key", field)
            self.assertIn("name", field)

    def test_query_get_workbook_metadata_table(self):
        """Test that get_workbook_metadata_table returns a DataFrame"""
        import pandas as pd
        metadata_table = self.wb.query.get_workbook_metadata_table()
        self.assertIsInstance(metadata_table, pd.DataFrame)
        # Should have at least some rows if workbook has content
        if len(self.wb.worksheet_objects) > 0:
            self.assertGreater(len(metadata_table), 0)

    def test_query_normalize_groupfilter(self):
        """Test normalize_groupfilter method"""
        query = self.wb.query

        # Test with empty input
        result = query.normalize_groupfilter([])
        self.assertEqual(result, [])

        # Test with None
        result = query.normalize_groupfilter(None)
        self.assertEqual(result, [])

        # Test with sample groupfilter structure
        sample_groupfilter = [{
            'function': 'member',
            'level': '[Customer]',
            'member': 'John Doe',
            'attributes': {'user': 'test'},
            'children': []
        }]
        result = query.normalize_groupfilter(sample_groupfilter)
        self.assertIsInstance(result, list)
        if result:
            self.assertIn('function', result[0])
            self.assertIn('depth', result[0])
            self.assertIn('parent_index', result[0])


class TestUtils(unittest.TestCase):
    """Test utility functions for version 012 - updated to return tuple"""

    def test_clean_aggregated_column_names_basic(self):
        result = _clean_aggregated_column_names("[federated.123].[Date:ok]")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "federated.123")  # datasource
        self.assertEqual(result[1], "[Date]")  # field

    def test_clean_aggregated_column_names_with_none_prefix(self):
        result = _clean_aggregated_column_names("[federated.123].[none:Date:ok]")
        self.assertEqual(result[0], "federated.123")
        self.assertEqual(result[1], "[Date]")

    def test_clean_handles_attr_prefix(self):
        result = _clean_aggregated_column_names(
            "[federated.abc].[attr:Time (copy)_2124854612630003715:ok]"
        )
        self.assertEqual(result[0], "federated.abc")
        self.assertEqual(result[1], "[Time (copy)_2124854612630003715]")

    def test_clean_handles_sum_prefix_and_qk_suffix(self):
        result = _clean_aggregated_column_names(
            "[federated.xyz].[sum:Calculation_386465155945086977:qk]"
        )
        self.assertEqual(result[0], "federated.xyz")
        self.assertEqual(result[1], "[Calculation_386465155945086977]")

    def test_clean_handles_usr_prefix(self):
        result = _clean_aggregated_column_names(
            "[federated.abc].[usr:CustomCalc:ok]"
        )
        self.assertEqual(result[0], "federated.abc")
        self.assertEqual(result[1], "[CustomCalc]")

    def test_clean_handles_none_prefix_and_ok_suffix_long_calc(self):
        result = _clean_aggregated_column_names(
            "[federated.id].[none:Calculation_1871104940863873027:ok]"
        )
        self.assertEqual(result[0], "federated.id")
        self.assertEqual(result[1], "[Calculation_1871104940863873027]")

    def test_clean_from_filter_attribute_like_xml(self):
        result = _clean_aggregated_column_names(
            "[federated.1].[none:Calculation_676102912337485826:nk]"
        )
        self.assertEqual(result[0], "federated.1")
        self.assertEqual(result[1], "[Calculation_676102912337485826]")

    def test_empty_input(self):
        result = _clean_aggregated_column_names("")
        # Should return tuple (None, None) or similar for empty input
        self.assertTrue(result is None or result == (None, None) or result == ())

    def test_none_input(self):
        result = _clean_aggregated_column_names(None)
        # Should return tuple (None, None) or similar for None input
        self.assertTrue(result is None or result == (None, None) or result == ())

    def test_non_string_input(self):
        result = _clean_aggregated_column_names(123)
        # Should return tuple (None, None) or similar for non-string input
        self.assertTrue(result is None or result == (None, None) or result == ())


class TestBackwardsCompatibility(unittest.TestCase):
    """Test that version 012 features don't break existing functionality"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_existing_dashboards_property_still_works(self):
        """Test that the original dashboards property still works"""
        self.assertTrue(hasattr(self.wb, 'dashboards'))
        self.assertIsInstance(self.wb.dashboards, list)
        
    def test_existing_worksheets_property_still_works(self):
        """Test that the original worksheets property still works"""
        self.assertTrue(hasattr(self.wb, 'worksheets'))
        self.assertIsInstance(self.wb.worksheets, list)
        
    def test_existing_datasources_property_still_works(self):
        """Test that the original datasources property still works"""
        self.assertTrue(hasattr(self.wb, 'datasources'))
        self.assertIsInstance(self.wb.datasources, list)
        
    def test_dashboard_names_match_between_old_and_new(self):
        """Test that dashboard names match between old and new properties"""
        old_dashboard_names = set(self.wb.dashboards)
        new_dashboard_names = set(self.wb.dashboard_objects.keys())
        self.assertEqual(old_dashboard_names, new_dashboard_names)
        
    def test_worksheet_names_match_between_old_and_new(self):
        """Test that worksheet names match between old and new properties"""
        old_worksheet_names = set(self.wb.worksheets)
        new_worksheet_names = set(self.wb.worksheet_objects.keys())
        self.assertEqual(old_worksheet_names, new_worksheet_names)


class TestXMLStringInput(unittest.TestCase):
    """Test XML string input feature for Workbook class"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        # Read the TWB XML content from existing file for testing
        self.wb_from_file = Workbook(TEST_SUPERSTORE_FILE)
    
    def test_workbook_can_be_created_from_xml_string(self):
        """Test that Workbook can be created from XML string"""
        # Extract XML from existing workbook file
        if hasattr(self.wb_from_file, '_workbookTree') and self.wb_from_file._workbookTree is not None:
            import xml.etree.ElementTree as ET
            xml_string = ET.tostring(self.wb_from_file._workbookTree.getroot(), encoding='unicode')
            
            # Create workbook from XML string
            wb_from_string = Workbook(twb_xml_string=xml_string)
            
            # Basic validation
            self.assertIsNotNone(wb_from_string)
            self.assertIsNone(wb_from_string._filename)  # Should be None for string input
            self.assertIsNotNone(wb_from_string._workbookRoot)
            
    def test_workbook_xml_string_has_same_properties_as_file(self):
        """Test that workbook created from XML string has same properties as file"""
        if hasattr(self.wb_from_file, '_workbookTree') and self.wb_from_file._workbookTree is not None:
            import xml.etree.ElementTree as ET
            xml_string = ET.tostring(self.wb_from_file._workbookTree.getroot(), encoding='unicode')
            
            wb_from_string = Workbook(twb_xml_string=xml_string)
            
            # Compare basic properties
            self.assertEqual(len(self.wb_from_file.dashboards), len(wb_from_string.dashboards))
            self.assertEqual(len(self.wb_from_file.worksheets), len(wb_from_string.worksheets))
            self.assertEqual(len(self.wb_from_file.datasources), len(wb_from_string.datasources))
            
    def test_workbook_xml_string_invalid_input_raises_error(self):
        """Test that invalid XML string input raises appropriate errors"""
        # Test with non-string input
        with self.assertRaises(TypeError):
            Workbook(twb_xml_string=123)
            
        # Test with invalid XML
        with self.assertRaises(Exception):
            Workbook(twb_xml_string="<invalid>xml</invalid>")
            
        # Test with wrong root element
        with self.assertRaises(Exception):
            Workbook(twb_xml_string="<wrongroot></wrongroot>")
            
    def test_workbook_xml_string_save_methods(self):
        """Test save behavior for workbooks created from XML strings"""
        if hasattr(self.wb_from_file, '_workbookTree') and self.wb_from_file._workbookTree is not None:
            import xml.etree.ElementTree as ET
            xml_string = ET.tostring(self.wb_from_file._workbookTree.getroot(), encoding='unicode')
            
            wb_from_string = Workbook(twb_xml_string=xml_string)
            
            # save() should raise error
            with self.assertRaises(Exception):
                wb_from_string.save()
                
            # save_as() should work if we provide a filename
            # We won't actually save, just test that it doesn't raise error for filename validation
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.twb', delete=True) as tmp:
                # This should not raise an error
                try:
                    wb_from_string.save_as(tmp.name)
                except Exception as e:
                    # Allow file write errors, but not parameter validation errors
                    if "new filename must be a non-empty path" in str(e):
                        self.fail("save_as parameter validation failed")


class TestParameterFunctionality(unittest.TestCase):
    """Test parameter-related functionality"""
    
    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_query_has_get_workbook_parameters_method(self):
        """Test that Query class has get_workbook_parameters method"""
        self.assertTrue(hasattr(self.wb.query, 'get_workbook_parameters'))
        
    def test_get_workbook_parameters_returns_list(self):
        """Test that get_workbook_parameters returns a list"""
        parameters = self.wb.query.get_workbook_parameters()
        self.assertIsInstance(parameters, list)
        
    def test_parameter_structure_contains_expected_keys(self):
        """Test that parameter dictionaries contain expected keys"""
        parameters = self.wb.query.get_workbook_parameters()
        
        if parameters:  # Only test if parameters exist
            param = parameters[0]
            expected_keys = [
                "Alias", "Aliases", "Calculation", "Caption", "Datatype", 
                "Name", "Parameter_Domain_Type", "Role", "Type", "Value",
                "Worksheets", "Members"
            ]
            for key in expected_keys:
                with self.subTest(key=key):
                    self.assertIn(key, param)
                    
    def test_parameter_data_types(self):
        """Test that parameter attributes have correct data types"""
        parameters = self.wb.query.get_workbook_parameters()
        
        for param in parameters:
            with self.subTest(parameter=param.get("Name", "Unknown")):
                # String fields (can be None)
                string_fields = ["Alias", "Caption", "Datatype", "Name", "Parameter_Domain_Type", "Role", "Type", "Value", "Calculation"]
                for field in string_fields:
                    value = param.get(field)
                    self.assertTrue(value is None or isinstance(value, str))
                
                # List fields
                self.assertIsInstance(param["Worksheets"], list)
                self.assertIsInstance(param["Members"], list)
                
                # Dict field
                self.assertIsInstance(param["Aliases"], dict)


class TestQueryComparisonMethods(unittest.TestCase):
    """Test Query comparison methods"""

    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)

    def test_query_compare_diffs_exists(self):
        """Test that Query.compare_diffs static method exists"""
        self.assertTrue(hasattr(Query, 'compare_diffs'))

    def test_query_compare_diffs_with_same_file(self):
        """Test comparing a workbook with itself"""
        import pandas as pd
        # Compare the same file
        df_diff = Query.compare_diffs(
            wb1_filename=TEST_SUPERSTORE_FILE,
            wb2_filename=TEST_SUPERSTORE_FILE
        )
        self.assertIsInstance(df_diff, pd.DataFrame)
        # Should have Workbook_Source column
        self.assertIn('Workbook_Source', df_diff.columns)
        # All items should be in 'both' when comparing identical files
        if not df_diff.empty:
            # Check if all are marked as 'both' after deduplication
            unique_sources = df_diff['Workbook_Source'].unique()
            # Most entries should be 'both' for identical files
            self.assertIn('both', unique_sources)

    def test_query_compare_diffs_with_xml_strings(self):
        """Test compare_diffs with XML string input"""
        import pandas as pd
        import xml.etree.ElementTree as ET

        # Get XML string from existing workbook
        if hasattr(self.wb, '_workbookTree') and self.wb._workbookTree is not None:
            xml_string = ET.tostring(self.wb._workbookTree.getroot(), encoding='unicode')

            # Compare using XML strings
            df_diff = Query.compare_diffs(
                wb1_filename=None,
                wb2_filename=None,
                wb1_twb_string=xml_string,
                wb2_twb_string=xml_string
            )
            self.assertIsInstance(df_diff, pd.DataFrame)
            self.assertIn('Workbook_Source', df_diff.columns)

    def test_query_json_safe_dataframe_exists(self):
        """Test that Query.json_safe_dataframe static method exists"""
        self.assertTrue(hasattr(Query, 'json_safe_dataframe'))

    def test_query_json_safe_dataframe_converts_complex_types(self):
        """Test json_safe_dataframe converts complex types to JSON strings"""
        import pandas as pd
        import numpy as np

        # Create a test DataFrame with complex types
        df = pd.DataFrame({
            'dict_col': [{'key': 'value'}, {'key2': 'value2'}],
            'list_col': [[1, 2, 3], [4, 5, 6]],
            'scalar_col': [1, 2],
            'string_col': ['a', 'b']
        })

        # Convert to JSON-safe
        result = Query.json_safe_dataframe(df)

        # Dict and list columns should be JSON strings
        self.assertIsInstance(result.iloc[0]['dict_col'], str)
        self.assertIsInstance(result.iloc[0]['list_col'], str)
        # Scalar columns should remain unchanged
        self.assertEqual(result.iloc[0]['scalar_col'], 1)
        self.assertEqual(result.iloc[0]['string_col'], 'a')


class TestNewFieldProperties(unittest.TestCase):
    """Test new Field properties: value, param_domain_type, members, table"""

    def setUp(self):
        if not os.path.exists(TEST_SUPERSTORE_FILE):
            self.skipTest(f"Test file {TEST_SUPERSTORE_FILE} not available")
        self.wb = Workbook(TEST_SUPERSTORE_FILE)
        
    def test_field_has_value_property(self):
        """Test that Field objects have value property"""
        # Get a field from any datasource
        if self.wb.datasources:
            datasource = self.wb.datasources[0]
            if datasource.fields:
                field = next(iter(datasource.fields.values()))
                self.assertTrue(hasattr(field, 'value'))
                # Value can be None or string
                value = field.value
                self.assertTrue(value is None or isinstance(value, str))
                
    def test_field_has_param_domain_type_property(self):
        """Test that Field objects have param_domain_type property"""
        if self.wb.datasources:
            datasource = self.wb.datasources[0]
            if datasource.fields:
                field = next(iter(datasource.fields.values()))
                self.assertTrue(hasattr(field, 'param_domain_type'))
                # param_domain_type can be None or string
                param_domain_type = field.param_domain_type
                self.assertTrue(param_domain_type is None or isinstance(param_domain_type, str))
                
    def test_field_has_members_property(self):
        """Test that Field objects have members property"""
        if self.wb.datasources:
            datasource = self.wb.datasources[0]
            if datasource.fields:
                field = next(iter(datasource.fields.values()))
                self.assertTrue(hasattr(field, 'members'))
                # Members should be a list
                members = field.members
                self.assertIsInstance(members, list)
                # Each member should be a string or None
                for member in members:
                    self.assertTrue(member is None or isinstance(member, str))

    def test_field_has_table_property(self):
        """Test that Field objects have table property"""
        if self.wb.datasources:
            # Find a non-parameters datasource
            non_param_datasources = [ds for ds in self.wb.datasources if ds.name != "Parameters"]
            if non_param_datasources:
                datasource = non_param_datasources[0]
                if datasource.fields:
                    field = next(iter(datasource.fields.values()))
                    self.assertTrue(hasattr(field, 'table'))
                    # Table can be None or string
                    table = field.table
                    self.assertTrue(table is None or isinstance(table, str))
                    
    def test_field_create_field_xml_with_parameter_attributes(self):
        """Test that create_field_xml works with new parameter attributes"""
        from tableaudocumentapi.field import Field
        
        # Test with parameter attributes
        xml = Field.create_field_xml(
            caption="Test Param",
            datatype="string", 
            hidden="false",
            role="dimension",
            field_type="nominal",
            name="[Test Param]",
            value="default_value",
            param_domain_type="range"
        )
        
        self.assertIsNotNone(xml)
        self.assertEqual(xml.get('caption'), "Test Param")
        self.assertEqual(xml.get('value'), "default_value")
        self.assertEqual(xml.get('param_domain_type'), "range")
        
    def test_field_create_field_xml_without_parameter_attributes(self):
        """Test that create_field_xml works without parameter attributes (backward compatibility)"""
        from tableaudocumentapi.field import Field
        
        # Test without parameter attributes (should work with defaults)
        xml = Field.create_field_xml(
            caption="Test Field",
            datatype="string",
            hidden="false", 
            role="dimension",
            field_type="nominal",
            name="[Test Field]"
        )
        
        self.assertIsNotNone(xml)
        self.assertEqual(xml.get('caption'), "Test Field")
        self.assertIsNone(xml.get('value'))
        self.assertIsNone(xml.get('param_domain_type'))
        
    def test_parameters_datasource_exists(self):
        """Test if Parameters datasource exists in workbook"""
        parameter_datasources = [ds for ds in self.wb.datasources if ds.name == "Parameters"]
        
        # This test documents whether the test file has parameters
        # If no parameters exist, the test passes but logs the information
        if not parameter_datasources:
            # This is informational - the test file might not have parameters
            pass
        else:
            # If parameters exist, test their structure
            params_ds = parameter_datasources[0]
            self.assertIsInstance(params_ds.fields, dict)
            
            for field_name, field in params_ds.fields.items():
                with self.subTest(field=field_name):
                    # Parameter fields should have these properties accessible
                    self.assertTrue(hasattr(field, 'value'))
                    self.assertTrue(hasattr(field, 'param_domain_type'))
                    self.assertTrue(hasattr(field, 'members'))


if __name__ == '__main__':
    unittest.main()