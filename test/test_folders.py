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
    'folder_test.tds'
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

    def test_folders(self):
        """ Test if creating a folder works.
        """
        name = "MyTestFolder"
        role = "dimensions"
        fields = ["[name]", "[price]"]
        fields2 = ["[typ]"]
        state = self.current_hash()

        self.tds.add_folder(name, role, fields)
        # check hash
        new_state = self.current_hash()
        self.assertNotEqual(state, new_state)
        state = new_state

        self.tds.add_to_folder(name, fields2)
        # check hash
        new_state = self.current_hash()
        self.assertNotEqual(state, new_state)

    def test_folder_fail(self):
        state = self.current_hash()

        with self.assertRaises(ValueError):
            self.tds.add_to_folder("not_existing_folder", [])
        # check hash
        new_state = self.current_hash()
        self.assertEqual(state, new_state)
        state = new_state

if __name__ == '__main__':
    unittest.main()
