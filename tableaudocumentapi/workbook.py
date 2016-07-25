###############################################################################
#
# Workbook - A class for writing Tableau workbook files
#
###############################################################################
import os
import zipfile
import weakref

import xml.etree.ElementTree as ET

from tableaudocumentapi import Datasource, xfile
from tableaudocumentapi.xfile import xml_open


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

        self._workbookTree = xml_open(self._filename)

        self._workbookRoot = self._workbookTree.getroot()
        # prepare our datasource objects
        self._datasources = self._prepare_datasources(
            self._workbookRoot)  # self.workbookRoot.find('datasources')

        self._datasource_index = self._prepare_datasource_index(self._datasources)

        self._worksheets = self._prepare_worksheets(
            self._workbookRoot, self._datasource_index
        )

    ###########
    # datasources
    ###########
    @property
    def datasources(self):
        return self._datasources

    ###########
    # worksheets
    ###########
    @property
    def worksheets(self):
        return self._worksheets

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
        xfile._save_file(self._filename, self._workbookTree)

    def save_as(self, new_filename):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        xfile._save_file(
            self._filename, self._workbookTree, new_filename)

    ###########################################################################
    #
    # Private API.
    #
    ###########################################################################
    @staticmethod
    def _prepare_datasource_index(datasources):
        retval = weakref.WeakValueDictionary()
        for datasource in datasources:
            retval[datasource.name] = datasource

        return retval

    @staticmethod
    def _prepare_datasources(xml_root):
        datasources = []

        # loop through our datasources and append
        datasource_elements = xml_root.find('datasources')
        if datasource_elements is None:
            return []

        for datasource in datasource_elements:
            ds = Datasource(datasource)
            datasources.append(ds)

        return datasources

    @staticmethod
    def _prepare_worksheets(xml_root, ds_index):
        worksheets = []
        worksheets_element = xml_root.find('.//worksheets')
        if worksheets_element is None:
            return worksheets

        for worksheet_element in worksheets_element:
            worksheet_name = worksheet_element.attrib['name']
            worksheets.append(worksheet_name)  # TODO: A real worksheet object, for now, only name

            dependencies = worksheet_element.findall('.//datasource-dependencies')

            for dependency in dependencies:
                datasource_name = dependency.attrib['datasource']
                datasource = ds_index[datasource_name]
                for column in dependency.findall('.//column'):
                    column_name = column.attrib['name']
                    if column_name in datasource.fields:
                        datasource.fields[column_name].add_used_in(worksheet_name)

        return worksheets
