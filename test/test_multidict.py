import unittest
import os.path
import functools

from tableaudocumentapi.multilookup_dict import MultiLookupDict


class MLDTests(unittest.TestCase):
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

    def test_multilookupdict_name_only(self):
        actual = self.mld['[baz]']
        self.assertEqual(3, actual['value'])

    def test_multilookupdict_alias_overrides_everything(self):
        actual = self.mld['bar']
        self.assertEqual(1, actual['value'])

    def test_mutlilookupdict_caption_overrides_id(self):
        actual = self.mld['foo']
        self.assertEqual(2, actual['value'])

    def test_mutlilookupdict_can_still_find_id_even_with_alias(self):
        actual = self.mld['[foo]']
        self.assertEqual(1, actual['value'])

    def test_mutlilookupdict_can_still_find_caption_even_with_alias(self):
        actual = self.mld['baz']
        self.assertEqual(1, actual['value'])

    def test_mutlilookupdict_can_still_find_id_even_with_caption(self):
        actual = self.mld['[bar]']
        self.assertEqual(2, actual['value'])
