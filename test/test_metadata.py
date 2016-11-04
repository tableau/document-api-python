import unittest
import os.path

from tableaudocumentapi import Datasource
import xml.etree.ElementTree as ET


TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
TEST_TDS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'field_change_test.tds'
)
TEST_TDS_FILE_OUTPUT = os.path.join(
    TEST_ASSET_DIR,
    'field_change_test_output.tds'
)


class TestFieldChange(unittest.TestCase):

    def setUp(self):
        self.tds = Datasource.from_file(TEST_TDS_FILE)

    def current_hash(self):
        """ Return a hash of the current state of the XML.

        Allows us to easily identify whether the underlying XML-structure
        of a TDS-file has actually changed. Avoids false positives if,
        for example, a fields value has changed but the XML hasn't.
        """
        return hash(ET.tostring(self.tds._datasourceTree.getroot()))

    def test_metadata_creation(self):
        """ Test if a metadata-record column can be created
        """
        state = self.current_hash()
        self.tds.add_metadata_record("my_new_attr", "my_data", "string")
        self.assertNotEqual(state, self.current_hash())

    def tearDown(self):
        """ Test if the file can be saved.
        Output file will be ignored by git, but can be used to verify the results.
        """
        self.tds.save_as(TEST_TDS_FILE_OUTPUT)


if __name__ == '__main__':
    unittest.main()
