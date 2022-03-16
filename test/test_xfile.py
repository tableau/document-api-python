from test.assets.index import *

import unittest
import zipfile
from tableaudocumentapi.xfile import find_file_in_zip
from tableaudocumentapi import Workbook, Datasource

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)

BAD_ZIP_FILE = os.path.join(
    TEST_ASSET_DIR,
    'BadZip.zip'
)

TWBX_WITH_CACHE_FILES = os.path.join(
    TEST_ASSET_DIR,
    'Cache.twbx'
)


class XFileEdgeTests(unittest.TestCase):
    def test_find_file_in_zip_no_xml_file(self):
        badzip = zipfile.ZipFile(BAD_ZIP_FILE)
        self.assertIsNone(find_file_in_zip(badzip))

    def test_only_find_twbs(self):
        twb_from_twbx_with_cache = zipfile.ZipFile(TWBX_WITH_CACHE_FILES)
        self.assertEqual(find_file_in_zip(twb_from_twbx_with_cache), 'Superstore.twb')


class Namespacing(unittest.TestCase):

    def assertContainsUserNamespace(self, filename):
        with open(filename, 'r') as in_file:
            # the namespace is in the first five lines for all the docs I've checked
            lineCount = 0
            doc_beginning_excerpt = ""
            while lineCount < 5:
                doc_beginning_excerpt += (in_file.readline().strip())  # first line should be xml tag
                lineCount += 1
            found = doc_beginning_excerpt.rfind("xmlns:user=")
            # print(doc_beginning_excerpt[found:found+10])
            self.assertRegex(doc_beginning_excerpt, "xmlns:user=")

    def test_save_preserves_namespace_twb(self):
        filename = COMPLEX_TWB
        self.assertContainsUserNamespace(filename)
        wb = Workbook(filename)
        new_name = 'saved-as-twb.twb'
        wb.save_as(new_name)
        self.assertContainsUserNamespace(new_name)

    def demo_bug_ns_not_preserved_if_not_used(self):
        filename = TABLEAU_10_TDS
        self.assertContainsUserNamespace(filename)
        wb = Datasource.from_file(filename)
        new_name = 'saved-as-tds.tds'
        wb.save_as(new_name)
        self.assertContainsUserNamespace(new_name)
