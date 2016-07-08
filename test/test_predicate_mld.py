import unittest
import os.path
import functools

from tableaudocumentapi.multilookup_dict import PredicatedDictionary, MultiLookupDict


class PMLDTests(unittest.TestCase):
    def setUp(self):
        self.mld = MultiLookupDict({
            '[foo]': {
                'alias': 'bar',
                'caption': 'baz',
                'value': 1
            },
            '[bar]': {
                'caption': 'foo',
                'value': 2
            },
            '[baz]': {
                'value': 3
            }
        })
        self.pd = PredicatedDictionary(lambda x: x['value'] != 3, self.mld)

    def test_predicatedmutlilookupdict_returns_items_that_pass_predicate(self):
        actual = self.pd['[bar]']
        self.assertEqual(2, actual['value'])

    def test_predicatedmultilookupdict_throws_key_error_for_items_that_do_not_pass_predicate(self):
        try:
            actual = self.pd['[baz]']
        except KeyError:
            return

        self.fail('[baz] should throw a KeyError because it failed the predicate')
