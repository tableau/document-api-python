# -*- coding: utf-8 -*-

import os.path
import unittest
import xml.etree.ElementTree as ET

from tableaudocumentapi import Datasource
from tableaudocumentapi.folder import (AlreadyMemberOfThisFolderException,
                                       Folder, FolderItem,
                                       MemberOfMultipleFoldersException)

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
TEST_TDS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'folder_test.tds'
)
TEST_TDS_TEMP_FILE = os.path.join(
    TEST_ASSET_DIR,
    'folder_test_temp.tds'
)


class TestFolders(unittest.TestCase):

    def setUp(self):
        self.tds = Datasource.from_file(TEST_TDS_FILE)

    def current_hash(self):
        """ Return a hash of the current state of the XML.

        Allows us to easily identify whether the underlying XML-structure
        of a TDS-file has actually changed. Avoids false positives if,
        for example, a fields value has changed but the XML hasn't.
        """
        return hash(ET.tostring(self.tds._datasourceTree.getroot()))

    def test_get_existing_folders(self):
        """ Test whether pre-existing folders in a TDS file are recognized.

        The test-TDS-file already contains a folder named "MyTestFolder"
        This folder already contains a field named "[price]"
        """
        folder = self.tds.folders["MyTestFolder"]
        self.assertIsNotNone(folder)
        self.assertTrue(folder.has_item('[price]'))

    def test_fields_in_folders(self):
        """ Test whether folder-items of a folder can be extracted.
        Allowed types are: FolderItem, String and Field
        """
        folder = self.tds.folders["MyTestFolder"]

        # check String
        self.assertTrue(folder.has_item('[price]'))
        self.assertFalse(folder.has_item('[bananas]'))

        # check FolderItem
        self.assertTrue(folder.has_item(folder.folder_items[0]))

        # check Field
        field = self.tds.fields['[price]']
        self.assertTrue(folder.has_item(field))

        # should fail for invalid types
        with self.assertRaises(ValueError):
            folder.has_item(404)

    def test_add_to_folder(self):
        """ A folder should be able to accept new fields.

        The test-TDS-file already contains a folder named "MyTestFolder"
        This folder already contains a single field named "[price]"
        """
        field_already_in_folder = '[price]'
        field_already_in_other_folder = '[name]'
        field_not_in_a_folder = '[typ]'

        # if a field is already in a folder
        field = self.tds.fields[field_already_in_folder]
        self.assertIsNotNone(field)
        folder = self.tds.folders["MyTestFolder"]
        with self.assertRaises(AlreadyMemberOfThisFolderException):
            folder.add_field(field)

        # if a field is already in another folder
        field = self.tds.fields[field_already_in_other_folder]
        self.assertIsNotNone(field)
        folder = self.tds.folders["MyTestFolder"]
        with self.assertRaises(MemberOfMultipleFoldersException):
            folder.add_field(field)

        # a field that can actually be added
        field = self.tds.fields[field_not_in_a_folder]
        self.assertIsNotNone(field)
        folder = self.tds.folders["MyTestFolder"]
        folder.add_field(field)
        self.assertTrue(folder.has_item(field))

        # check persistence
        self.tds.save_as(TEST_TDS_TEMP_FILE)
        persisted_tds = Datasource.from_file(TEST_TDS_TEMP_FILE)
        persisted_folder = persisted_tds.folders['MyTestFolder']
        self.assertTrue(persisted_folder.has_item(field_not_in_a_folder))

    def test_remove_from_folder(self):
        """ A folder should be able to delete fields.

        The test-TDS-file already contains a folder named "MyTestFolder"
        This folder already contains a single field named "[price]"
        """
        field_already_in_folder = '[price]'
        field_not_in_a_folder = '[typ]'

        # if a field is not in a folder
        field = self.tds.fields[field_not_in_a_folder]
        self.assertIsNotNone(field)
        folder = self.tds.folders["MyTestFolder"]
        with self.assertRaises(ValueError):
            folder.remove_field(field)

        # a field that can actually be removed
        field = self.tds.fields[field_already_in_folder]
        self.assertIsNotNone(field)
        folder = self.tds.folders["MyTestFolder"]
        folder.remove_field(field)
        self.assertFalse(folder.has_item(field))

        # check persistence
        self.tds.save_as(TEST_TDS_TEMP_FILE)
        persisted_tds = Datasource.from_file(TEST_TDS_TEMP_FILE)
        persisted_folder = persisted_tds.folders['MyTestFolder']
        self.assertFalse(persisted_folder.has_item(field_already_in_folder))

    def test_change_attributes(self):
        name = "蚵仔煎"
        folder = self.tds.folders["MyTestFolder"]
        folder.name = name
        folder.role = "measures"

        self.tds.save_as(TEST_TDS_TEMP_FILE)
        persisted_tds = Datasource.from_file(TEST_TDS_TEMP_FILE)
        persisted_folder = persisted_tds.folders[name]
        self.assertIsNotNone(persisted_folder)
        self.assertEqual(persisted_folder.name, name)
        self.assertEqual(persisted_folder.role, "measures")

    def test_add_new_folder(self):
        """ The test-TDS-file should allow new folders to be added.
        """
        folder_name = "蚵仔煎"
        folder_role = "dimensions"
        field_not_in_a_folder = '[typ]'

        new_folder = self.tds.add_folder(folder_name, folder_role)

        # add a new field to that folder
        field = self.tds.fields[field_not_in_a_folder]
        new_folder.add_field(field)

        # check if the folder is there
        folder = self.tds.folders[folder_name]
        self.assertIsNotNone(folder)

        # test persistence
        self.tds.save_as(TEST_TDS_TEMP_FILE)
        persisted_tds = Datasource.from_file(TEST_TDS_TEMP_FILE)
        persisted_folder = persisted_tds.folders[folder_name]
        self.assertIsNotNone(persisted_folder)
        self.assertTrue(persisted_folder.has_item(field))

    def test_add_folder_fails(self):
        """ The test-TDS-file should NOT allow duplicated folders to be added.

        The test-TDS-file already contains a folder named "testfolder"
        This folder already contains a single field named "[price]"
        """
        folder_name = "another_testfolder"
        folder_role = "dimensions"
        field_not_in_a_folder = '[typ]'

        with self.assertRaises(ValueError):
            self.tds.add_folder(folder_name, "dimenzzionss")

        with self.assertRaises(ValueError):
            self.tds.add_folder("MyTestFolder", folder_role)


if __name__ == '__main__':
    unittest.main()
