###############################################################################
#
# Workbook - A class for writing Tableau workbook files
#
###############################################################################
import os
import zipfile

import xml.etree.ElementTree as ET

from tableaudocumentapi import Datasource, archivefile

###########################################################################
#
# Utility Functions
#
###########################################################################


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
            self._workbookTree = archivefile.get_xml_from_archive(
                self._filename)
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
            archivefile.save_into_archive(
                self._workbookTree, filename=self._filename)
        else:
            self._workbookTree.write(
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
            archivefile.save_into_archive(
                self._workbookTree, self._filename, new_filename)
        else:
            self._workbookTree.write(
                new_filename, encoding="utf-8", xml_declaration=True)

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

    @staticmethod
    def _is_valid_file(filename):
        fileExtension = os.path.splitext(filename)[-1].lower()
        return fileExtension in ('.twb', '.tds')
