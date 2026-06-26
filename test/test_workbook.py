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

WORKSHEET_NO_DATASOURCES_FILE = os.path.join(
    TEST_ASSET_DIR,
    'worksheet_no_datasources.twb'
)

WORKSHEET_NO_SHELVES_FILE = os.path.join(
    TEST_ASSET_DIR,
    'worksheet_no_shelves.twb'
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

    def test_worksheet_fields_returns_list_not_method(self):
        # fields property was returning the method object instead of self._fields
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        fields = ws.fields
        self.assertIsInstance(fields, list, "fields should return a list, not a method object")

    def test_worksheet_fields_are_field_objects(self):
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        from tableaudocumentapi import Field
        for f in ws.fields:
            self.assertIsInstance(f, Field)

    def test_worksheet_datasources_not_empty(self):
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        self.assertGreater(len(ws.datasources), 0)

    def test_worksheet_rows_returns_list(self):
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        # Sheet 1 has two fields on rows shelf
        self.assertIsNotNone(ws.rows)
        self.assertIsInstance(ws.rows, list)
        self.assertEqual(len(ws.rows), 2)

    def test_worksheet_cols_empty_shelf_returns_none_or_list(self):
        # Sheet 1 has an empty <cols /> element - should not crash
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        result = ws.cols
        self.assertTrue(result is None or isinstance(result, list))

    def test_worksheet_rows_field_names(self):
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        # Sheet 1 rows: Calculation_88946136969252864 (caption: SHOW) and "Burst Out Set list"
        # _ds_fields_to_items resolves via datasource.fields, so we get Field objects or raw strings
        from tableaudocumentapi import Field
        names = [f.caption if isinstance(f, Field) else f for f in ws.rows]
        self.assertIn('SHOW', names)  # Calculation resolved to its caption

    def test_all_datasource_dependencies_collected(self):
        # return inside loop meant only first datasource-dependencies block was processed
        wb = Workbook(DASHBOARDS_FILE)
        ws = wb.worksheet_items[0]
        # Sheet 1 has 3 columns in its datasource-dependencies block
        self.assertEqual(len(ws.fields), 3)

    def test_worksheet_with_no_datasources_element_does_not_crash(self):
        # _prepare_datasources iterates the result of find(), which is None if element absent
        wb = Workbook(WORKSHEET_NO_DATASOURCES_FILE)
        ws = wb.worksheet_items[0]
        self.assertEqual(ws.datasources, [])

    def test_worksheet_with_no_rows_element_does_not_crash(self):
        # _prepare_rows calls .text on find() result without None check
        wb = Workbook(WORKSHEET_NO_SHELVES_FILE)
        ws = wb.worksheet_items[0]
        self.assertIsNone(ws.rows)

    def test_worksheet_with_no_cols_element_does_not_crash(self):
        # _prepare_cols calls .text on find() result without None check
        wb = Workbook(WORKSHEET_NO_SHELVES_FILE)
        ws = wb.worksheet_items[0]
        self.assertIsNone(ws.cols)