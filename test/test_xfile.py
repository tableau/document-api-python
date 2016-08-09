import os.path
import unittest
import zipfile
from tableaudocumentapi.xfile import find_file_in_zip

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
BAD_ZIP_FILE = os.path.join(
    TEST_ASSET_DIR,
    'BadZip.zip'
)


class XFileEdgeTests(unittest.TestCase):
    def test_find_file_in_zip_no_xml_file(self):
        badzip = zipfile.ZipFile(BAD_ZIP_FILE)
        self.assertIsNone(find_file_in_zip(badzip))
