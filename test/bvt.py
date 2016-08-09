import os
import unittest

import xml.etree.ElementTree as ET

from tableaudocumentapi import Workbook, Datasource, Connection, ConnectionParser
from tableaudocumentapi.xfile import TableauInvalidFileException, TableauVersionNotSupportedException

TEST_DIR = os.path.dirname(__file__)

TABLEAU_82_TWB = os.path.join(TEST_DIR, 'assets', 'TABLEAU_82_TWB.twb')

TABLEAU_93_TWB = os.path.join(TEST_DIR, 'assets', 'TABLEAU_93_TWB.twb')

TABLEAU_93_TDS = os.path.join(TEST_DIR, 'assets', 'TABLEAU_93_TDS.tds')

TABLEAU_10_TDS = os.path.join(TEST_DIR, 'assets', 'TABLEAU_10_TDS.tds')

TABLEAU_10_TWB = os.path.join(TEST_DIR, 'assets', 'TABLEAU_10_TWB.twb')

TABLEAU_CONNECTION_XML = ET.parse(os.path.join(
    TEST_DIR, 'assets', 'CONNECTION.xml')).getroot()

TABLEAU_10_TWBX = os.path.join(TEST_DIR, 'assets', 'TABLEAU_10_TWBX.twbx')

TABLEAU_10_TDSX = os.path.join(TEST_DIR, 'assets', 'TABLEAU_10_TDSX.tdsx')

EMPTY_WORKBOOK = os.path.join(TEST_DIR, 'assets', 'empty_workbook.twb')


class ConnectionParserTests(unittest.TestCase):

    def test_can_extract_legacy_connection(self):
        parser = ConnectionParser(ET.parse(TABLEAU_93_TDS), '9.2')
        connections = parser.get_connections()
        self.assertIsInstance(connections, list)
        self.assertIsInstance(connections[0], Connection)
        self.assertEqual(connections[0].dbname, 'TestV1')

    def test_can_extract_federated_connections(self):
        parser = ConnectionParser(ET.parse(TABLEAU_10_TDS), '10.0')
        connections = parser.get_connections()
        self.assertIsInstance(connections, list)
        self.assertIsInstance(connections[0], Connection)
        self.assertEqual(connections[0].dbname, 'testv1')


class ConnectionModelTests(unittest.TestCase):

    def setUp(self):
        self.connection = TABLEAU_CONNECTION_XML

    def test_can_read_attributes_from_connection(self):
        conn = Connection(self.connection)
        self.assertEqual(conn.dbname, 'TestV1')
        self.assertEqual(conn.username, '')
        self.assertEqual(conn.server, 'mssql2012.test.tsi.lan')
        self.assertEqual(conn.dbclass, 'sqlserver')
        self.assertEqual(conn.authentication, 'sspi')

    def test_can_write_attributes_to_connection(self):
        conn = Connection(self.connection)
        conn.dbname = 'BubblesInMyDrink'
        conn.server = 'mssql2014.test.tsi.lan'
        conn.username = 'bob'
        self.assertEqual(conn.dbname, 'BubblesInMyDrink')
        self.assertEqual(conn.username, 'bob')
        self.assertEqual(conn.server, 'mssql2014.test.tsi.lan')

    def test_bad_dbclass_rasies_attribute_error(self):
        conn = Connection(self.connection)
        conn.dbclass = 'sqlserver'
        self.assertEqual(conn.dbclass, 'sqlserver')
        with self.assertRaises(AttributeError):
            conn.dbclass = 'NotReal'


class DatasourceModelTests(unittest.TestCase):

    def setUp(self):
        with open(TABLEAU_93_TDS, 'rb') as in_file, open('test.tds', 'wb') as out_file:
            out_file.write(in_file.read())
            self.tds_file = out_file

    def tearDown(self):
        self.tds_file.close()
        os.unlink(self.tds_file.name)

    def test_can_extract_datasource_from_file(self):
        ds = Datasource.from_file(self.tds_file.name)
        self.assertEqual(ds.name, 'sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo')
        self.assertEqual(ds.version, '9.3')

    def test_can_extract_connection(self):
        ds = Datasource.from_file(self.tds_file.name)
        self.assertIsInstance(ds.connections[0], Connection)
        self.assertIsInstance(ds.connections, list)

    def test_can_save_tds(self):
        original_tds = Datasource.from_file(self.tds_file.name)
        original_tds.connections[0].dbname = 'newdb.test.tsi.lan'
        original_tds.save()

        new_tds = Datasource.from_file(self.tds_file.name)
        self.assertEqual(new_tds.connections[0].dbname, 'newdb.test.tsi.lan')

    def test_save_has_xml_declaration(self):
        original_tds = Datasource.from_file(self.tds_file.name)
        original_tds.connections[0].dbname = 'newdb.test.tsi.lan'

        original_tds.save()

        with open(self.tds_file.name) as f:
            first_line = f.readline().strip()  # first line should be xml tag
            self.assertEqual(
                first_line, "<?xml version='1.0' encoding='utf-8'?>")


class DatasourceModelV10Tests(unittest.TestCase):

    def setUp(self):
        with open(TABLEAU_10_TDS, 'rb') as in_file, open('test.twb', 'wb') as out_file:
            out_file.write(in_file.read())
            self.tds_file = out_file

    def tearDown(self):
        self.tds_file.close()
        os.unlink(self.tds_file.name)

    def test_can_extract_datasource_from_file(self):
        ds = Datasource.from_file(self.tds_file.name)
        self.assertEqual(ds.name, 'federated.1s4nxn20cywkdv13ql0yk0g1mpdx')
        self.assertEqual(ds.version, '10.0')

    def test_can_extract_connection(self):
        ds = Datasource.from_file(self.tds_file.name)
        self.assertIsInstance(ds.connections[0], Connection)
        self.assertIsInstance(ds.connections, list)

    def test_can_save_tds(self):
        original_tds = Datasource.from_file(self.tds_file.name)
        original_tds.connections[0].dbname = 'newdb.test.tsi.lan'
        original_tds.save()

        new_tds = Datasource.from_file(self.tds_file.name)
        self.assertEqual(new_tds.connections[0].dbname, 'newdb.test.tsi.lan')


class DatasourceModelV10TDSXTests(unittest.TestCase):

    def setUp(self):
        with open(TABLEAU_10_TDSX, 'rb') as in_file, open('test.tdsx', 'wb') as out_file:
            out_file.write(in_file.read())
            self.tdsx_file = out_file

    def tearDown(self):
        self.tdsx_file.close()
        os.unlink(self.tdsx_file.name)

    def test_can_open_tdsx(self):
        ds = Datasource.from_file(self.tdsx_file.name)
        self.assertTrue(ds.connections)
        self.assertTrue(ds.name)

    def test_can_open_tdsx_and_save_changes(self):
        original_tdsx = Datasource.from_file(self.tdsx_file.name)
        original_tdsx.connections[0].server = 'newdb.test.tsi.lan'
        original_tdsx.save()

        new_tdsx = Datasource.from_file(self.tdsx_file.name)
        self.assertEqual(new_tdsx.connections[
                         0].server, 'newdb.test.tsi.lan')

    def test_can_open_tdsx_and_save_as_changes(self):
        new_tdsx_filename = 'newtdsx.tdsx'
        original_wb = Datasource.from_file(self.tdsx_file.name)
        original_wb.connections[0].server = 'newdb.test.tsi.lan'
        original_wb.save_as(new_tdsx_filename)

        new_wb = Datasource.from_file(new_tdsx_filename)
        self.assertEqual(new_wb.connections[
                         0].server, 'newdb.test.tsi.lan')
        os.unlink(new_tdsx_filename)


class WorkbookModelTests(unittest.TestCase):

    def setUp(self):
        with open(TABLEAU_93_TWB, 'rb') as in_file, open('test.twb', 'wb') as out_file:
            out_file.write(in_file.read())
            self.workbook_file = out_file

    def tearDown(self):
        self.workbook_file.close()
        os.unlink(self.workbook_file.name)

    def test_can_extract_datasource(self):
        wb = Workbook(self.workbook_file.name)
        self.assertEqual(len(wb.datasources), 1)
        self.assertIsInstance(wb.datasources[0], Datasource)
        self.assertEqual(wb.datasources[0].name,
                         'sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo')

    def test_can_get_worksheets(self):
        wb = Workbook(self.workbook_file.name)
        self.assertIsNotNone(wb.worksheets)

    def test_has_filename(self):
        wb = Workbook(self.workbook_file.name)
        self.assertEqual(wb.filename, self.workbook_file.name)

    def test_can_update_datasource_connection_and_save(self):
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].dbname = 'newdb.test.tsi.lan'
        original_wb.save()

        new_wb = Workbook(self.workbook_file.name)
        self.assertEqual(new_wb.datasources[0].connections[
                         0].dbname, 'newdb.test.tsi.lan')


class WorkbookModelV10Tests(unittest.TestCase):

    def setUp(self):
        with open(TABLEAU_10_TWB, 'rb') as in_file, open('test.twb', 'wb') as out_file:
            out_file.write(in_file.read())
            self.workbook_file = out_file

    def tearDown(self):
        self.workbook_file.close()
        os.unlink(self.workbook_file.name)

    def test_can_extract_datasourceV10(self):
        wb = Workbook(self.workbook_file.name)
        self.assertEqual(len(wb.datasources), 1)
        self.assertEqual(len(wb.datasources[0].connections), 2)
        self.assertIsInstance(wb.datasources[0].connections, list)
        self.assertIsInstance(wb.datasources[0], Datasource)
        self.assertEqual(wb.datasources[0].name,
                         'federated.1s4nxn20cywkdv13ql0yk0g1mpdx')

    def test_can_update_datasource_connection_and_saveV10(self):
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].dbname = 'newdb.test.tsi.lan'

        original_wb.save()

        new_wb = Workbook(self.workbook_file.name)
        self.assertEqual(new_wb.datasources[0].connections[
                         0].dbname, 'newdb.test.tsi.lan')

    def test_save_has_xml_declaration(self):
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].dbname = 'newdb.test.tsi.lan'

        original_wb.save()

        with open(self.workbook_file.name) as f:
            first_line = f.readline().strip()  # first line should be xml tag
            self.assertEqual(
                first_line, "<?xml version='1.0' encoding='utf-8'?>")


class WorkbookModelV10TWBXTests(unittest.TestCase):

    def setUp(self):
        with open(TABLEAU_10_TWBX, 'rb') as in_file, open('test.twbx', 'wb') as out_file:
            out_file.write(in_file.read())
            self.workbook_file = out_file

    def tearDown(self):
        self.workbook_file.close()
        os.unlink(self.workbook_file.name)

    def test_can_open_twbx(self):
        wb = Workbook(self.workbook_file.name)
        self.assertTrue(wb.datasources)
        self.assertTrue(wb.datasources[0].connections)

    def test_can_open_twbx_and_save_changes(self):
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].server = 'newdb.test.tsi.lan'
        original_wb.save()

        new_wb = Workbook(self.workbook_file.name)
        self.assertEqual(new_wb.datasources[0].connections[
                         0].server, 'newdb.test.tsi.lan')

    def test_can_open_twbx_and_save_as_changes(self):
        new_twbx_filename = 'newtwbx.twbx'
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].server = 'newdb.test.tsi.lan'
        original_wb.save_as(new_twbx_filename)

        new_wb = Workbook(new_twbx_filename)
        self.assertEqual(new_wb.datasources[0].connections[
                         0].server, 'newdb.test.tsi.lan')

        os.unlink(new_twbx_filename)


class EmptyWorkbookWillLoad(unittest.TestCase):

    def test_no_exceptions_thrown(self):
        wb = Workbook(EMPTY_WORKBOOK)
        self.assertIsNotNone(wb)


class LoadOnlyValidFileTypes(unittest.TestCase):

    def test_exception_when_workbook_given_tdsx(self):
        with self.assertRaises(TableauInvalidFileException):
            wb = Workbook(TABLEAU_10_TDSX)

    def test_exception_when_datasource_given_twbx(self):
        with self.assertRaises(TableauInvalidFileException):
            ds = Datasource.from_file(TABLEAU_10_TWBX)


class SupportedWorkbookVersions(unittest.TestCase):

    def test_82_workbook_throws_exception(self):
        with self.assertRaises(TableauVersionNotSupportedException):
            wb = Workbook(TABLEAU_82_TWB)

if __name__ == '__main__':
    unittest.main()
