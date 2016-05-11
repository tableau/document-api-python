import unittest

from tableaudocumentapi import Workbook

class HelperMethodTests(unittest.TestCase):

    def test_is_valid_file_with_valid_inputs(self):
        self.assertTrue(Workbook._is_valid_file('file1.tds'))
        self.assertTrue(Workbook._is_valid_file('file2.twb'))
        self.assertTrue(Workbook._is_valid_file('tds.twb'))

    def test_is_valid_file_with_invalid_inputs(self):
        self.assertFalse(Workbook._is_valid_file(''))
        self.assertFalse(Workbook._is_valid_file('file1.tds2'))
        self.assertFalse(Workbook._is_valid_file('file2.twb3'))

if __name__ == '__main__':
    unittest.main()
