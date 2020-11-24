class ActionLink(object):
    """Action datasource element"""

    def __init__(self,actiondataxml):
        self._xml = actiondataxml
        self._expression = self._xml.get('expression')

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def name(self, value):
        self._expression = value
        self._xml.set('expression', value)


class Action(object):
    """A class representing workbook actions."""

    def __init__(self, actionxml):
        self._xml = actionxml
        self._link = list(map(ActionLink, self._xml.findall('./link')))

    @property
    def link(self):
        return self._link
