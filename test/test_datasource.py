import unittest
import os.path

from tableaudocumentapi import Datasource
from tableaudocumentapi import Workbook

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


class DataSourceFieldsTWB(unittest.TestCase):
    def setUp(self):
        self.wb = Workbook(TEST_TWB_FILE)
        self.ds = self.wb.datasources[0]  # Assume the first datasource in the file

    def test_datasource_fields_loaded_in_workbook(self):
        self.assertIsNotNone(self.ds.fields)
        self.assertIsNotNone(self.ds.fields.get('[Number of Records]', None))

    def test_datasource_fields_in_use(self):
        self.assertIsNotNone(self.ds.usedFields)
        self.assertIsNone(self.ds.usedFields.get('[Number of Records]', None))
        self.assertIsNone(self.ds.usedFields.get('[a]', None))
