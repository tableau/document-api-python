class Filter:
    def __init__(self, xml):
        self._xml = xml
        self._class = xml.get('class')
        self._column = xml.get('column')
