import unittest
import os.path
import functools

from tableaudocumentapi import Datasource

TEST_TDS_FILE = os.path.join(
    os.path.dirname(__file__),
    'assets',
    'datasource_test.tds'
)


class DataSourceColumns(unittest.TestCase):
    def setUp(self):
        self.ds = Datasource.from_file(TEST_TDS_FILE)

    def test_datasource_returns_correct_columns(self):
        self.assertIsNotNone(self.ds.columns)
        self.assertIsNotNone(self.ds.columns.get('[Number of Records]', None))

    def test_datasource_returns_calulcation_from_column(self):
        self.assertEqual('1', self.ds.columns['[Number of Records]'].calculation)

    def test_datasource_uses_metadata_record(self):
        self.assertEqual('Sum', self.ds.columns['[x]'].aggregation)
