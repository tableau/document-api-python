import unittest
import io
import os
import xml.etree.ElementTree as ET

from tableaudocumentapi import Workbook, Datasource, Connection, ConnectionParser


TABLEAU_93_WORKBOOK = '''<?xml version='1.0' encoding='utf-8' ?><workbook source-build='9.3.1 (9300.16.0510.0100)' source-platform='mac' version='9.3' xmlns:user='http://www.tableausoftware.com/xml/user'><datasources><datasource caption='xy (TestV1)' inline='true' name='sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo' version='9.3'><connection authentication='sspi' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username=''></connection></datasource></datasources></workbook>'''

TABLEAU_93_TDS = '''<?xml version='1.0' encoding='utf-8' ?><datasource formatted-name='sqlserver.17u3bqc16tjtxn14e2hxh19tyvpo' inline='true' source-platform='mac' version='9.3' xmlns:user='http://www.tableausoftware.com/xml/user'><connection authentication='sspi' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username=''></connection></datasource>'''

TABLEAU_10_TDS = '''<?xml version='1.0' encoding='utf-8' ?><datasources><datasource caption='xy+ (Multiple Connections)' inline='true' name='federated.1s4nxn20cywkdv13ql0yk0g1mpdx' version='10.0'><connection class='federated'><named-connections><named-connection caption='mysql55.test.tsi.lan' name='mysql.1ewmkrw0mtgsev1dnurma1blii4x'><connection class='mysql' dbname='testv1' odbc-native-protocol='yes' port='3306' server='mysql55.test.tsi.lan' source-charset='' username='test' /></named-connection><named-connection caption='mssql2012.test.tsi.lan' name='sqlserver.1erdwp01uqynlb14ul78p0haai2r'><connection authentication='sqlserver' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username='test' /></named-connection></named-connections></connection></datasource></datasources>'''

TABLEAU_10_WORKBOOK = '''<?xml version='1.0' encoding='utf-8' ?><workbook source-build='0.0.0 (0000.16.0510.1300)' source-platform='mac' version='10.0' xmlns:user='http://www.tableausoftware.com/xml/user'><datasources><datasource caption='xy+ (Multiple Connections)' inline='true' name='federated.1s4nxn20cywkdv13ql0yk0g1mpdx' version='10.0'><connection class='federated'><named-connections><named-connection caption='mysql55.test.tsi.lan' name='mysql.1ewmkrw0mtgsev1dnurma1blii4x'><connection class='mysql' dbname='testv1' odbc-native-protocol='yes' port='3306' server='mysql55.test.tsi.lan' source-charset='' username='test' /></named-connection><named-connection caption='mssql2012.test.tsi.lan' name='sqlserver.1erdwp01uqynlb14ul78p0haai2r'><connection authentication='sqlserver' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username='test' /></named-connection></named-connections></connection></datasource></datasources></workbook>'''

TABLEAU_CONNECTION_XML = ET.fromstring(
    '''<connection authentication='sspi' class='sqlserver' dbname='TestV1' odbc-native-protocol='yes' one-time-sql='' server='mssql2012.test.tsi.lan' username=''></connection>''')

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

    def test_can_write_attributes_to_connection(self):
        conn = Connection(self.connection)
        conn.dbname = 'BubblesInMyDrink'
        conn.server = 'mssql2014.test.tsi.lan'
        self.assertEqual(conn.dbname, 'BubblesInMyDrink')
        self.assertEqual(conn.username, '')
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
        self.assertEqual(new_wb.datasources[0].connections[0].dbname, 'newdb.test.tsi.lan')


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
        self.assertEqual(new_wb.datasources[0].connections[0].dbname, 'newdb.test.tsi.lan')

if __name__ == '__main__':
    unittest.main()
