###############################################################################
#
# Datasource - A class for writing datasources to Tableau files
#
###############################################################################
import contextlib
import os
import shutil
import tempfile
import zipfile

import xml.etree.ElementTree as ET
from tableaudocumentapi import Connection


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)


def find_tds_in_zip(zip):
    for filename in zip.namelist():
        if os.path.splitext(filename)[-1].lower() == '.tds':
            return filename


def get_tds_xml_from_tdsx(filename):
    with temporary_directory() as temp:
        with zipfile.ZipFile(filename) as zf:
            zf.extractall(temp)
            tds_file = find_tds_in_zip(zf)
            tds_xml = ET.parse(os.path.join(temp, tds_file))

    return tds_xml


def build_tdsx_file(tdsx_contents, zip):
    for root_dir, _, files in os.walk(tdsx_contents):
        relative_dir = os.path.relpath(root_dir, tdsx_contents)
        for f in files:
            temp_file_full_path = os.path.join(
                tdsx_contents, relative_dir, f)
            zipname = os.path.join(relative_dir, f)
            zip.write(temp_file_full_path, arcname=zipname)


class ConnectionParser(object):

    def __init__(self, datasource_xml, version):
        self._dsxml = datasource_xml
        self._dsversion = version

    def _extract_federated_connections(self):
        return list(map(Connection, self._dsxml.findall('.//named-connections/named-connection/*')))

    def _extract_legacy_connection(self):
        return list(map(Connection, self._dsxml.findall('connection')))

    def get_connections(self):
        if float(self._dsversion) < 10:
            connections = self._extract_legacy_connection()
        else:
            connections = self._extract_federated_connections()
        return connections


class Datasource(object):
    """
    A class for writing datasources to Tableau files.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################
    def __init__(self, dsxml, filename=None):
        """
        Constructor.  Default is to create datasource from xml.

        """
        self._filename = filename
        self._datasourceXML = dsxml
        self._datasourceTree = ET.ElementTree(self._datasourceXML)
        self._name = self._datasourceXML.get('name') or self._datasourceXML.get(
            'formatted-name')  # TDS files don't have a name attribute
        self._version = self._datasourceXML.get('version')
        self._connection_parser = ConnectionParser(
            self._datasourceXML, version=self._version)
        self._connections = self._connection_parser.get_connections()

    @classmethod
    def from_file(cls, filename):
        "Initialize datasource from file (.tds)"

        if zipfile.is_zipfile(filename):
            dsxml = get_tds_xml_from_tdsx(filename).getroot()
        else:
            dsxml = ET.parse(filename).getroot()
        return cls(dsxml, filename)

    def _save_into_tdsx(self, filename=None):
        # Save reuses existing filename, 'save as' takes a new one
        if filename is None:
            filename = self._filename

        # Saving a tdsx means extracting the contents into a temp folder,
        # saving the changes over the tds in that folder, and then
        # packaging it back up into a specifically formatted zip with the correct
        # relative file paths

        # Extract to temp directory
        with temporary_directory() as temp_path:
            with zipfile.ZipFile(self._filename) as zf:
                tds_file = find_tds_in_zip(zf)
                zf.extractall(temp_path)
            # Write the new version of the tds to the temp directory
            self._datasourceTree.write(os.path.join(
                temp_path, tds_file), encoding="utf-8", xml_declaration=True)

            # Write the new tdsx with the contents of the temp folder
            with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as new_tdsx:
                build_tdsx_file(temp_path, new_tdsx)

    def save(self):
        """
        Call finalization code and save file.

        Args:
            None.

        Returns:
            Nothing.

        """

        # save the file

        if zipfile.is_zipfile(self._filename):
            self._save_into_tdsx(self._filename)
        else:
            self._datasourceTree.write(
                self._filename, encoding="utf-8", xml_declaration=True)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        if zipfile.is_zipfile(self._filename):
            self._save_into_tdsx(new_filename)
        else:
            self._datasourceTree.write(
                new_filename, encoding="utf-8", xml_declaration=True)

    ###########
    # name
    ###########
    @property
    def name(self):
        return self._name

    ###########
    # version
    ###########
    @property
    def version(self):
        return self._version

    ###########
    # connections
    ###########
    @property
    def connections(self):
        return self._connections
