import unittest
import os.path

from tableaudocumentapi import Datasource, Workbook

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
EPHEMERAL_FIELD_FILE = os.path.join(
    TEST_ASSET_DIR,
    'ephemeral_field.twb'
)


class EphemeralFields(unittest.TestCase):
    def test_ephemeral_fields_do_not_cause_errors(self):
        wb = Workbook(EPHEMERAL_FIELD_FILE)
        self.assertIsNotNone(wb)
