class MetadataRecord(object):
    """A class representing metadata record (in the datasource-connection or in the datasource-extract."""

    def __init__(self, metadata_recordxml):
        """Instantiate metadata record.
        """
        self._mtdrecord = metadata_recordxml
        self._remote_name = self._mtdrecord.find('remote-name').text
        self._local_name = self._mtdrecord.find('local-name').text
        self._remote_alias = self._mtdrecord.find('remote-alias').text
    
    @property
    def mtd_record(self):
        """The metadata record."""
        return self._mtdrecord
        
    @property
    def remote_name(self):
        """The remote name of the field to which metadata record belongs."""
        return self._remote_name

    @property
    def local_name(self):
        """The local name of the field to which metadata record belongs."""
        return self._local_name.strip('[').strip(']')

    @property
    def remote_alias(self):
        """The remote alias of the field to which metadata record belongs"""
        return self._remote_alias

    @remote_name.setter
    def remote_name(self, value):
        """
        Sets the new remote name for the metadata record.

        Args:
            value: new remote name. String.

        Returns:
            Nothing.

        """
        self._remote_name = value
        self._mtdrecord.find('remote-name').text = value

    @local_name.setter
    def local_name(self, value):
        """
        Sets the new remote name for the metadata record.
    
        Args:
            value: new remote name. String.
    
        Returns:
            Nothing.
    
        """
        # local name is in brackets in the XML
        value_processed = value.strip('[').strip(']')
        self._local_name = value_processed
        self._mtdrecord.find('local-name').text = "[{}]".format(value_processed)
        
    @remote_alias.setter
    def remote_alias(self, value):
        """
        Sets the new remote name for the metadata record.
    
        Args:
            value: new remote name. String.
    
        Returns:
            Nothing.
    
        """
        self._remote_alias = value
        self._mtdrecord.find('remote-alias').text = value