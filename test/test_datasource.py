import unittest
import os.path
import functools

from tableaudocumentapi import Datasource

TEST_TDS_FILE = os.path.join(
    os.path.dirname(__file__),
    'assets',
    'datasource_test.tds'
)


class DataSourceFields(unittest.TestCase):
    def setUp(self):
        self.ds = Datasource.from_file(TEST_TDS_FILE)

    def test_datasource_returns_correct_fields(self):
        self.assertIsNotNone(self.ds.fields)
        self.assertIsNotNone(self.ds.fields.get('[Number of Records]', None))

    def test_datasource_returns_calculation_from_fields(self):
        self.assertEqual('1', self.ds.fields['[Number of Records]'].calculation)

    def test_datasource_uses_metadata_record(self):
        self.assertEqual('Sum', self.ds.fields['[x]'].aggregation)
