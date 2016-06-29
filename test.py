import base64
import io
import os
import unittest

import xml.etree.ElementTree as ET

from tableaudocumentapi import Workbook, Datasource, Connection, ConnectionParser


TABLEAU_93_WORKBOOK = '''<?xml version='1.0' encoding='utf-8' ?><workbook source-build='9.3.1 (9300.16.0510.0100)' source-platform='mac' version='9.3' xmlns:user='http://www.tableausoftware.com/xml/user'><datasources><datasource caption='xy (TestV1)' inline='true' name='sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo' version='9.3'><connection authentication='sspi' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username=''></connection></datasource></datasources></workbook>'''

TABLEAU_93_TDS = '''<?xml version='1.0' encoding='utf-8' ?><datasource formatted-name='sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo' inline='true' source-platform='mac' version='9.3' xmlns:user='http://www.tableausoftware.com/xml/user'><connection authentication='sspi' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username=''></connection></datasource>'''

TABLEAU_10_TDS = '''<?xml version='1.0' encoding='utf-8' ?><datasource caption='xy+ (Multiple Connections)' inline='true' name='federated.1s4nxn20cywkdv13ql0yk0g1mpdx' version='10.0'><connection class='federated'><named-connections><named-connection caption='mysql55.test.tsi.lan' name='mysql.1ewmkrw0mtgsev1dnurma1blii4x'><connection class='mysql' dbname='testv1' odbc-native-protocol='yes' port='3306' server='mysql55.test.tsi.lan' source-charset='' username='test' /></named-connection><named-connection caption='mssql2012.test.tsi.lan' name='sqlserver.1erdwp01uqynlb14ul78p0haai2r'><connection authentication='sqlserver' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username='test' /></named-connection></named-connections></connection></datasource>'''

TABLEAU_10_WORKBOOK = '''<?xml version='1.0' encoding='utf-8' ?><workbook source-build='0.0.0 (0000.16.0510.1300)' source-platform='mac' version='10.0' xmlns:user='http://www.tableausoftware.com/xml/user'><datasources><datasource caption='xy+ (Multiple Connections)' inline='true' name='federated.1s4nxn20cywkdv13ql0yk0g1mpdx' version='10.0'><connection class='federated'><named-connections><named-connection caption='mysql55.test.tsi.lan' name='mysql.1ewmkrw0mtgsev1dnurma1blii4x'><connection class='mysql' dbname='testv1' odbc-native-protocol='yes' port='3306' server='mysql55.test.tsi.lan' source-charset='' username='test' /></named-connection><named-connection caption='mssql2012.test.tsi.lan' name='sqlserver.1erdwp01uqynlb14ul78p0haai2r'><connection authentication='sqlserver' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username='test' /></named-connection></named-connections></connection></datasource></datasources></workbook>'''

TABLEAU_CONNECTION_XML = ET.fromstring(
    '''<connection authentication='sspi' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username=''></connection>''')

TABLEAU_10_TWBX = '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'


class HelperMethodTests(unittest.TestCase):

    def test_is_valid_file_with_valid_inputs(self):
        self.assertTrue(Workbook._is_valid_file('file1.tds'))
        self.assertTrue(Workbook._is_valid_file('file2.twb'))
        self.assertTrue(Workbook._is_valid_file('tds.twb'))

    def test_is_valid_file_with_invalid_inputs(self):
        self.assertFalse(Workbook._is_valid_file(''))
        self.assertFalse(Workbook._is_valid_file('file1.tds2'))
        self.assertFalse(Workbook._is_valid_file('file2.twb3'))


class ConnectionParserTests(unittest.TestCase):

    def test_can_extract_legacy_connection(self):
        parser = ConnectionParser(ET.fromstring(TABLEAU_93_TDS), '9.2')
        connections = parser.get_connections()
        self.assertIsInstance(connections, list)
        self.assertIsInstance(connections[0], Connection)
        self.assertEqual(connections[0].dbname, 'TestV1')

    def test_can_extract_federated_connections(self):
        parser = ConnectionParser(ET.fromstring(TABLEAU_10_TDS), '10.0')
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


class DatasourceModelTests(unittest.TestCase):

    def setUp(self):
        self.tds_file = io.FileIO('test.tds', 'w')
        self.tds_file.write(TABLEAU_93_TDS.encode('utf8'))
        self.tds_file.seek(0)

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
        self.tds_file = io.FileIO('test10.tds', 'w')
        self.tds_file.write(TABLEAU_10_TDS.encode('utf8'))
        self.tds_file.seek(0)

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


class WorkbookModelTests(unittest.TestCase):

    def setUp(self):
        self.workbook_file = io.FileIO('test.twb', 'w')
        self.workbook_file.write(TABLEAU_93_WORKBOOK.encode('utf8'))
        self.workbook_file.seek(0)

    def tearDown(self):
        self.workbook_file.close()
        os.unlink(self.workbook_file.name)

    def test_can_extract_datasource(self):
        wb = Workbook(self.workbook_file.name)
        self.assertEqual(len(wb.datasources), 1)
        self.assertIsInstance(wb.datasources[0], Datasource)
        self.assertEqual(wb.datasources[0].name,
                         'sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo')

    def test_can_update_datasource_connection_and_save(self):
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].dbname = 'newdb.test.tsi.lan'
        original_wb.save()

        new_wb = Workbook(self.workbook_file.name)
        self.assertEqual(new_wb.datasources[0].connections[
                         0].dbname, 'newdb.test.tsi.lan')


class WorkbookModelV10Tests(unittest.TestCase):

    def setUp(self):
        self.workbook_file = io.FileIO('testv10.twb', 'w')
        self.workbook_file.write(TABLEAU_10_WORKBOOK.encode('utf8'))
        self.workbook_file.seek(0)

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
        self.workbook_file = io.FileIO('testtwbx.twbx', 'wb')
        self.workbook_file.write(base64.b64decode(TABLEAU_10_TWBX))
        self.workbook_file.seek(0)

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
        new_twbx_filename = self.workbook_file.name + "_TEST_SAVE_AS"
        original_wb = Workbook(self.workbook_file.name)
        original_wb.datasources[0].connections[0].server = 'newdb.test.tsi.lan'
        original_wb.save_as(new_twbx_filename)

        new_wb = Workbook(new_twbx_filename)
        self.assertEqual(new_wb.datasources[0].connections[
                         0].server, 'newdb.test.tsi.lan')

        os.unlink(new_twbx_filename)

if __name__ == '__main__':
    unittest.main()
