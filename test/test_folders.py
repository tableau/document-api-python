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

    @unittest.skip("Not yet implemented")
    def test_get_existing_folders(self):
        """ Test whether pre-existing folders in a TDS file are recognized.

        The test-TDS-file already contains a folder named "testfolder"
        This folder already contains a single field named "[price]"
        """
        folder = self.tds.folders["testfolder"]
        self.assertIsNotNone(folder)
        self.assertIn("[price]", folder.fields)

    @unittest.skip("Not yet implemented")
    def test_add_new_folder(self):
        """ The test-TDS-file should allow new folders to be added.
        """
        folder_name = "another_testfolder"
        state = self.current_hash()
        self.tds.add_folder(folder_name)
        self.assertNotEqual(state, self.current_hash())

        # the fields of this folder should be an empty dict
        folder = self.tds.folders[folder_name]
        self.assertIsNotNone(folder)
        self.assertEqual(folder.fields, {})

    @unittest.skip("Not yet implemented")
    def test_add_folder_duplicate(self):
        """ The test-TDS-file should NOT allow duplicated folders to be added.

        The test-TDS-file already contains a folder named "testfolder"
        This folder already contains a single field named "[price]"
        """
        folder_name = "testfolder"
        state = self.current_hash()
        with self.assertRaises(Exception):
            self.tds.add_folder(folder_name)
        self.assertEqual(state, self.current_hash())

    @unittest.skip("Not yet implemented")
    def test_add_to_folder(self):
        """ A folder should be able to accept new fields.

        The test-TDS-file already contains a folder named "testfolder"
        This folder already contains a single field named "[price]"
        """
        new_field_name = "[amount]"
        field = self.tds.fields[new_field_name]
        self.assertIsNotNone(field)
        folder = self.tds.folders["testfolder"]

        # Test adding a field
        state = self.current_hash()
        folder.add_field(field)
        # check whether object-representation has changed
        self.assertIn(new_field_name, folder.fields)
        # check whether xml-representation has changed
        self.assertNotEqual(state, self.current_hash())

    @unittest.skip("Not yet implemented")
    def test_add_duplicate_to_folder(self):
        """ A folder should disallow adding an already existing field.

        The test-TDS-file already contains a folder named "testfolder"
        This folder already contains a single field named "[price]"
        """
        new_field_name = "[price]"
        field = self.tds.fields[new_field_name]
        self.assertIsNotNone(field)
        folder = self.tds.folders["testfolder"]

        # check whether the field is already in the folder
        self.assertIn(new_field_name, folder.fields)
        # Test adding a field
        state = self.current_hash()
        with self.assertRaises(Exception):
            folder.add_field(field)
        # check whether xml-representation has not changed
        self.assertEqual(state, self.current_hash())

    @unittest.skip("Not yet implemented")
    def test_remove_from_folder(self):
        """ A folder should be able to delete fields from it.

        The test-TDS-file already contains a folder named "testfolder"
        This folder already contains a single field named "[price]"
        """
        # This field is already in the folder
        field_name = "[price]"
        field = self.tds.fields[field_name]
        self.assertIsNotNone(field)
        folder = self.tds.folders["testfolder"]
        self.assertIn(field_name, folder)

        # Test removing a field
        state = self.current_hash()
        folder.remove_field(field)
        # check whether object-representation has changed
        self.assertNotIn(field_name, folder.fields)
        # check whether xml-representation has changed
        self.assertNotEqual(state, self.current_hash())

if __name__ == '__main__':
    unittest.main()
