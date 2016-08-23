import unittest
import os.path

from tableaudocumentapi import Datasource, Workbook

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
TEST_TDS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'datasource_test.tds'
)

TEST_TWB_FILE = os.path.join(
    TEST_ASSET_DIR,
    'datasource_test.twb'
)


class DataSourceFieldsTDS(unittest.TestCase):

    def setUp(self):
        self.ds = Datasource.from_file(TEST_TDS_FILE)

    def test_datasource_returns_correct_fields(self):
        self.assertIsNotNone(self.ds.fields)
        self.assertIsNotNone(self.ds.fields.get('[Number of Records]', None))

    def test_datasource_returns_calculation_from_fields(self):
        self.assertEqual('1', self.ds.fields['[Number of Records]'].calculation)

    def test_datasource_uses_metadata_record(self):
        self.assertEqual('Sum', self.ds.fields['[x]'].default_aggregation)

    def test_datasource_column_name_contains_apostrophy(self):
        self.assertIsNotNone(self.ds.fields.get("[Today's Date]", None))

    def test_datasource_field_can_get_caption(self):
        self.assertEqual(self.ds.fields['[a]'].caption, 'A')
        self.assertEqual(getattr(self.ds.fields['[a]'], 'caption', None), 'A')

    def test_datasource_field_caption_can_be_used_to_query(self):
        self.assertIsNotNone(self.ds.fields.get('A', None))

    def test_datasource_field_is_nominal(self):
        self.assertTrue(self.ds.fields['[a]'].is_nominal)

    def test_datasource_field_is_quantitative(self):
        self.assertTrue(self.ds.fields['[y]'].is_quantitative)

    def test_datasource_field_is_ordinal(self):
        self.assertTrue(self.ds.fields['[x]'].is_ordinal)

    def test_datasource_field_datatype(self):
        self.assertEqual(self.ds.fields['[x]'].datatype, 'integer')

    def test_datasource_field_role(self):
        self.assertEqual(self.ds.fields['[x]'].role, 'measure')

    def test_datasource_field_description(self):
        actual = self.ds.fields['[a]'].description
        self.assertIsNotNone(actual)
        self.assertTrue(u'muted gray' in actual)


class DataSourceFieldsTWB(unittest.TestCase):

    def setUp(self):
        self.wb = Workbook(TEST_TWB_FILE)
        # Assume the first datasource in the file
        self.ds = self.wb.datasources[0]

    def test_datasource_fields_loaded_in_workbook(self):
        self.assertIsNotNone(self.ds.fields)
        self.assertIsNotNone(self.ds.fields.get('[Number of Records]', None))


class DataSourceFieldsFoundIn(unittest.TestCase):

    def setUp(self):
        self.wb = Workbook(TEST_TWB_FILE)
        # Assume the first datasource in the file
        self.ds = self.wb.datasources[0]

    def test_datasource_fields_found_in_returns_fields(self):
        actual_values = self.ds.fields.used_by_sheet('Sheet 1')
        self.assertIsNotNone(actual_values)
        self.assertEqual(1, len(actual_values))
        self.assertIn('A', (x.name for x in actual_values))

    def test_datasource_fields_found_in_does_not_return_fields_not_used_in_worksheet(self):
        actual_values = self.ds.fields.used_by_sheet('Sheet 1')
        self.assertIsNotNone(actual_values)
        self.assertEqual(1, len(actual_values))
        self.assertNotIn('X', (x.name for x in actual_values))

    def test_datasource_fields_found_in_returns_multiple_fields(self):
        actual_values = self.ds.fields.used_by_sheet('Sheet 2')
        self.assertIsNotNone(actual_values)
        self.assertEqual(2, len(actual_values))
        self.assertIn('A', (x.name for x in actual_values))
        self.assertIn('X', (x.name for x in actual_values))
        self.assertNotIn('Y', (x.name for x in actual_values))

    def test_datasource_fields_found_in_accepts_lists(self):
        actual_values = self.ds.fields.used_by_sheet(['Sheet 1', 'Sheet 2'])
        self.assertIsNotNone(actual_values)
        self.assertEqual(2, len(actual_values))
        self.assertIn('A', (x.name for x in actual_values))
        self.assertIn('X', (x.name for x in actual_values))
        self.assertNotIn('Y', (x.name for x in actual_values))
