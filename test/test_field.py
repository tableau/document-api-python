import unittest
import os.path

from tableaudocumentapi import Datasource, Field
from tableaudocumentapi.field import _find_metadata_record

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
TEST_TDS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'datasource_test.tds'
)
TEST_UNICODE_FILE = os.path.join(
    TEST_ASSET_DIR,
    'unicode.tds'
)


class FieldsUnitTest(unittest.TestCase):
    def test_field_throws_if_no_data_passed_in(self):
        with self.assertRaises(AttributeError):
            Field()


class FindMetaDataRecordEdgeTest(unittest.TestCase):
    class MockXmlWithNoFind(object):
        def find(self, *args, **kwargs):
            return None

    def test_find_metadata_record_returns_none(self):
        self.assertIsNone(_find_metadata_record(self.MockXmlWithNoFind(), 'foo'))


class FieldsHandleUnicode(unittest.TestCase):
    def test_description_unicode(self):
        ds = Datasource.from_file(TEST_UNICODE_FILE)
        self.assertIsNotNone(ds.fields['A'].description)
