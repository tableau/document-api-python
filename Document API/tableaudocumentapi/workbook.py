###############################################################################
#
# Workbook - A class for writing Tableau workbook files
#
###############################################################################
import os
import xml.etree.ElementTree as ET
from tableaudocumentapi import Datasource

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
        # We have a valid type of input file
        if self._is_valid_file(filename):
            # set our filename, open .twb, initialize things
            self._filename = filename
            self._workbookTree = ET.parse(filename)
            self._workbookRoot = self._workbookTree.getroot()
            
            # prepare our datasource objects
            self._datasources = self._prepare_datasources(self._workbookRoot)  #self.workbookRoot.find('datasources')
        else:
            print('Invalid file type. Must be .twb or .tds.')
            raise Exception()
            
    @classmethod
    def from_file(cls, filename):
        "Initialize datasource from file (.tds)"
        if self._is_valid_file(filename):
            self._filename = filename
            dsxml = ET.parse(filename).getroot()
            return cls(dsxml)
        else:
            print('Invalid file type. Must be .twb or .tds.')
            raise Exception()
            
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
        self._workbookTree.write(self._filename)
        
    def save_as(self, value):
        """
        Save our file with the name provided.

        Args:
            value:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        
        # We have a valid type of input file
        if self._is_valid_file(value):
            # save the file
            self._workbookTree.write(value)
        else:
            print('Invalid file type. Must be .twb or .tds.')
            raise Exception()

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
        
    def _is_valid_file(self, filename):
        valid = 0
        fileExtension = os.path.splitext(filename)[-1].lower()
        
        if fileExtension == ".twb":
            valid = 1
        elif fileExtension == ".tds":
            valid = 1
            
        return valid
