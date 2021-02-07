from tableaudocumentapi import BaseObject


class Expression(BaseObject):

    def __init__(self, expxml):
        self._expressionXML = expxml
        self._op = expxml.get('op')
        self._expressions = self._extract_expressions() or None

    def _extract_expressions(self):
        return list(map(Expression, self._expressionXML.findall('./expression')))

    @property
    def op(self):
        return self._op

    @property
    def expressions(self):
        return self._expressions

    def to_dict(self):
        base = {
            'op': self.op
        }
        if self.expressions:
            base['expressions'] = [exp.to_dict() for exp in self.expressions]
        return base


class Clause(BaseObject):

    def __init__(self, clxml):
        self._clauseXML = clxml
        self._type = clxml.get('type')
        self._expression = self._extract_expression()

    def _extract_expression(self):
        expxml = self._clauseXML.find('./expression')
        if expxml is not None:
            return Expression(expxml)
        else:
            return None

    @property
    def type(self):
        return self._type

    @property
    def expression(self):
        return self._expression

    def to_dict(self):
        return {
            'type': self.type,
            'expression': self.expression.to_dict()
        }


class Relation(BaseObject):
    """A class representing relations inside Connections."""

    def __init__(self, relxml):
        self._relationXML = relxml
        self._type = relxml.get('type')
        self._connection = relxml.get('connection')
        self._name = relxml.get('name')
        self._table = relxml.get('table')
        self._text = self._extract_text()
        self._clause = self._extract_clause()
        self._relations = self._extract_relations()

    def _extract_clause(self):
        clxml = self._relationXML.find('./clause')
        if clxml is not None:
            return Clause(clxml)
        else:
            return None

    def _extract_relations(self):
        relxmls = self._relationXML.findall('./relation')
        if relxmls:
            return list(map(Relation, relxmls))
        else:
            return None

    def _extract_text(self):
        text = None
        if self._relationXML.text:
            if not self._relationXML.text.isspace():
                text = self._relationXML.text
        return text

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def connection(self):
        return self._connection

    @property
    def table(self):
        return self._table

    @property
    def text(self):
        return self._text

    @property
    def clause(self):
        return self._clause

    @property
    def relation(self):
        return self._relations

    def _base_dict(self):
        base_attrs = ['type', 'name', 'connection', 'table', 'text']
        return self._to_dict(
            base_attrs=base_attrs
        )

    def to_dict(self):
        to_dict_attrs = ['clause']
        to_dict_list_attrs = ['relation']
        base = self._base_dict()
        base.update(
            self._to_dict(
                to_dict_attrs=to_dict_attrs,
                to_dict_list_attrs=to_dict_list_attrs,
            )
        )
        return base
