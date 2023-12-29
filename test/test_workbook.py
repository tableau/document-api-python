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

SHAPES_FILE = os.path.join(
    TEST_ASSET_DIR,
    'shapes_test.twb'
)

DASHBOARDS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'filtering.twb'
)


class EphemeralFields(unittest.TestCase):
    def test_ephemeral_fields_do_not_cause_errors(self):
        wb = Workbook(EPHEMERAL_FIELD_FILE)
        self.assertIsNotNone(wb)


class Shapes(unittest.TestCase):
    def test_shape_exist(self):
        wb = Workbook(SHAPES_FILE)
        self.assertEqual(wb.shapes, ['Bug Tracking/bug.png',
                                     'Bug Tracking/icon-scheduleitem.png',
                                     'Bug Tracking/light.png',
                                     'Bug Tracking/mail.png',
                                     ]
                         )

    def test_shape_count(self):
        wb = Workbook(SHAPES_FILE)
        self.assertEqual(len(wb.shapes), 4)


class Dashboards(unittest.TestCase):
    def test_dashboards_setup(self):
        wb = Workbook(DASHBOARDS_FILE)
        self.assertIsNotNone(wb)
        self.assertEqual(wb.dashboards, ['setTest'])

class Worksheets(unittest.TestCase):
    def test_worksheets_setup(self):
        wb = Workbook(DASHBOARDS_FILE)
        self.assertEqual(len(wb.worksheet_items), 2)
        worksheet_names = [ws.name for ws in wb.worksheet_items]
        worksheet_names.sort()
        self.assertEqual(worksheet_names[0], 'Sheet 1')