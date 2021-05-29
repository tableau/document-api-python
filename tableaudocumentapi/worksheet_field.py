class WorksheetField:
    def __init__(self, xml, datasource):
        self._xml = xml
        self.datasource = datasource
        self.name = self._xml.get('name')
        self.column = self._xml.get('column')
        self.derivation = self._xml.get('derivation')
        self.pivot = self._xml.get('pivot')
        self.type = self._xml.get('type')
