###############################################################################
#
# Workbook - A class for writing Tableau workbook files
#
###############################################################################
import os
import zipfile

import xml.etree.ElementTree as ET

from tableaudocumentapi import Datasource, containerfile

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
            self._workbookTree = containerfile.get_xml_from_archive(
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
        containerfile._save_file(self._filename, self._workbookTree)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        containerfile._save_file(
            self._filename, self._workbookTree, new_filename)

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
