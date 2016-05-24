###############################################################################
#
# Workbook - A class for writing Tableau workbook files
#
###############################################################################
import contextlib
import os
import shutil
import tempfile
import zipfile

import xml.etree.ElementTree as ET

from tableaudocumentapi import Datasource

###########################################################################
#
# Utility Functions
#
###########################################################################


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)


def find_twb_in_zip(zip):
    for filename in zip.namelist():
        if os.path.splitext(filename)[-1].lower() == '.twb':
            return filename


def get_twb_xml_from_twbx(filename):
    with temporary_directory() as temp:
        with zipfile.ZipFile(filename) as zf:
            zf.extractall(temp)
            twb_file = find_twb_in_zip(zf)
            twb_xml = ET.parse(os.path.join(temp, twb_file))

    return twb_xml


def build_twbx_file(twbx_contents, zip):
    for root_dir, _, files in os.walk(twbx_contents):
        relative_dir = os.path.relpath(root_dir, twbx_contents)
        for f in files:
            temp_file_full_path = os.path.join(
                twbx_contents, relative_dir, f)
            zipname = os.path.join(relative_dir, f)
            zip.write(temp_file_full_path, arcname=zipname)


class Workbook(object):
    """
    A class for writing Tableau workbook files.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################
    def __init__(self, filename):
        """
        Constructor.

        """
        self._filename = filename

        # Determine if this is a twb or twbx and get the xml root
        if zipfile.is_zipfile(self._filename):
            self._workbookTree = get_twb_xml_from_twbx(self._filename)
        else:
            self._workbookTree = ET.parse(self._filename)

        self._workbookRoot = self._workbookTree.getroot()
        # prepare our datasource objects
        self._datasources = self._prepare_datasources(
            self._workbookRoot)  # self.workbookRoot.find('datasources')

    ###########
    # datasources
    ###########
    @property
    def datasources(self):
        return self._datasources

    ###########
    # filename
    ###########
    @property
    def filename(self):
        return self._filename

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
            self._save_into_twbx(self._filename)
        else:
            self._workbookTree.write(self._filename)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        if zipfile.is_zipfile(self._filename):
            self._save_into_twbx(new_filename)
        else:
            self._workbookTree.write(new_filename)

    ###########################################################################
    #
    # Private API.
    #
    ###########################################################################
    def _prepare_datasources(self, xmlRoot):
        datasources = []

        # loop through our datasources and append
        for datasource in xmlRoot.find('datasources'):
            ds = Datasource(datasource)
            datasources.append(ds)

        return datasources

    def _save_into_twbx(self, filename=None):
        # Save reuses existing filename, 'save as' takes a new one
        if filename is None:
            filename = self._filename

        # Saving a twbx means extracting the contents into a temp folder,
        # saving the changes over the twb in that folder, and then
        # packaging it back up into a specifically formatted zip with the correct
        # relative file paths

        # Extract to temp directory
        with temporary_directory() as temp_path:
            with zipfile.ZipFile(self._filename) as zf:
                twb_file = find_twb_in_zip(zf)
                zf.extractall(temp_path)
            # Write the new version of the twb to the temp directory
            self._workbookTree.write(os.path.join(temp_path, twb_file))

            # Write the new twbx with the contents of the temp folder
            with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as new_twbx:
                build_twbx_file(temp_path, new_twbx)

    @staticmethod
    def _is_valid_file(filename):
        fileExtension = os.path.splitext(filename)[-1].lower()
        return fileExtension in ('.twb', '.tds')
