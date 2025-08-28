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
                    self.assertTrue(hasattr(filter_obj, 'groupfilters'))
                    
    def test_filter_groupfilters_is_list(self):
        """Test that groupfilters property returns a list"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)
            
        for filter_obj in filters:
            with self.subTest(filter_class=filter_obj.filter_class):
                self.assertIsInstance(filter_obj.groupfilters, list)
                
    def test_filter_column_is_list(self):
        """Test that column property returns a list (cleaned column names)"""
        filters = []
        for worksheet in self.wb.worksheet_objects.values():
            filters.extend(worksheet.filters)
            
        for filter_obj in filters:
            with self.subTest(filter_class=filter_obj.filter_class):
                self.assertIsInstance(filter_obj.column, list)
                # Each cleaned column should be a string
                for column in filter_obj.column:
                    self.assertIsInstance(column, str)
                    
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
        
    def test_query_get_workbook_dependencies_returns_list(self):
        """Test that get_workbook_dependencies returns a list"""
        dependencies = self.wb.query.get_workbook_dependencies()
        self.assertIsInstance(dependencies, list)
        
    def test_query_get_workbook_filters_returns_list(self):
        """Test that get_workbook_filters returns a list"""
        filters = self.wb.query.get_workbook_filters()
        self.assertIsInstance(filters, list)
        
    def test_query_dependency_structure(self):
        """Test structure of dependency objects returned by query"""
        dependencies = self.wb.query.get_workbook_dependencies()
        if dependencies:
            dep = dependencies[0]
            required_keys = [
                "Workbook", "Dashboard", "Worksheet", "Datasource", 
                "Columns", "Column_instance", "Column_instance_Derivation",
                "Column_instance_Name", "Column_instance_Pivot", "Column_instance_Type"
            ]
            for key in required_keys:
                with self.subTest(key=key):
                    self.assertIn(key, dep)
                    
    def test_query_filter_structure(self):
        """Test structure of filter objects returned by query"""
        filters = self.wb.query.get_workbook_filters()
        if filters:
            filter_obj = filters[0]
            required_keys = [
                "Workbook", "Dashboard", "Worksheet", 
                "Filter_class", "Column", "Groupfilters"
            ]
            for key in required_keys:
                with self.subTest(key=key):
                    self.assertIn(key, filter_obj)
                    
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
        
    def test_query_worksheet_dashboard_mapping(self):
        """Test that query correctly maps worksheets to dashboards"""
        query = self.wb.query
        dependencies = query.get_workbook_dependencies()
        
        for dep in dependencies:
            with self.subTest(worksheet=dep["Worksheet"]):
                # Dashboard should be a list (since worksheets can appear in multiple dashboards)
                self.assertIsInstance(dep["Dashboard"], list)
                # If worksheet appears in dashboards, each should be a string
                for dashboard_name in dep["Dashboard"]:
                    self.assertIsInstance(dashboard_name, str)
                    self.assertIn(dashboard_name, self.wb.dashboard_objects)


class TestUtils(unittest.TestCase):
    """Test utility functions for version 012"""

    def test_clean_aggregated_column_names_basic(self):
        result = _clean_aggregated_column_names("[federated.123].[Date:ok]")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "[federated.123].[Date]")

    def test_clean_aggregated_column_names_with_none_prefix(self):
        result = _clean_aggregated_column_names("[federated.123].[none:Date:ok]")
        self.assertEqual(result, ["[federated.123].[Date]"])

    def test_clean_aggregated_column_names_multiple_fields(self):
        result = _clean_aggregated_column_names(
            "[federated.123].[Date:ok]*[federated.456].[Sales:ok]"
        )
        self.assertCountEqual(
            result,
            ["[federated.123].[Date]", "[federated.456].[Sales]"]
        )

    def test_clean_aggregated_column_names_with_parentheses(self):
        result = _clean_aggregated_column_names(
            "([federated.123].[Date:ok]*[federated.456].[Sales:ok])"
        )
        self.assertCountEqual(
            result,
            ["[federated.123].[Date]", "[federated.456].[Sales]"]
        )

    def test_clean_handles_attr_prefix(self):
        result = _clean_aggregated_column_names(
            "[federated.abc].[attr:Time (copy)_2124854612630003715:ok]"
        )
        self.assertEqual(result, ["[federated.abc].[Time (copy)_2124854612630003715]"])

    def test_clean_handles_sum_prefix_and_qk_suffix(self):
        result = _clean_aggregated_column_names(
            "[federated.xyz].[sum:Calculation_386465155945086977:qk]"
        )
        self.assertEqual(result, ["[federated.xyz].[Calculation_386465155945086977]"])

    def test_clean_handles_none_prefix_and_ok_suffix_long_calc(self):
        result = _clean_aggregated_column_names(
            "[federated.id].[none:Calculation_1871104940863873027:ok]"
        )
        self.assertEqual(result, ["[federated.id].[Calculation_1871104940863873027]"])

    def test_clean_from_filter_attribute_like_xml(self):
        result = _clean_aggregated_column_names(
            "[federated.1].[none:Calculation_676102912337485826:nk]"
        )
        self.assertEqual(result, ["[federated.1].[Calculation_676102912337485826]"])

    def test_empty_input(self):
        self.assertEqual(_clean_aggregated_column_names(""), [])

    def test_none_input(self):
        self.assertEqual(_clean_aggregated_column_names(None), [])

    def test_non_string_input(self):
        self.assertEqual(_clean_aggregated_column_names(123), [])

    def test_clean_single_bracket_with_suffix_only(self):
        result = _clean_aggregated_column_names("[Calculation_386465155945086977:qk]")
        self.assertEqual(result, ["[Calculation_386465155945086977]"])

    def test_clean_single_bracket_with_prefix_and_suffix(self):
        result = _clean_aggregated_column_names("[none:Date:ok]")
        self.assertEqual(result, ["[Date]"])


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


if __name__ == '__main__':
    unittest.main()