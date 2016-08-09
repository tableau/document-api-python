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

    def test_multilookupdict_can_be_empty(self):
        mld = MultiLookupDict()
        self.assertIsNotNone(mld)

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

    def test_multilookupdict_gives_key_error_on_invalid_key(self):
        try:
            self.mld.get('foobar')
            self.fail('should have thrown key error')
        except KeyError as ex:
            self.assertEqual(str(ex), "'foobar'")

    def test_multilookupdict_get_returns_default_value(self):
        default_value = ('default', 'return', 'value')
        actual = self.mld.get('foobar', default_value)
        self.assertEqual(actual, default_value)

    def test_multilookupdict_get_returns_value(self):
        actual = self.mld.get('baz')
        self.assertEqual(1, actual['value'])

    def test_multilookupdict_can_set_item(self):
        before = self.mld['baz']
        self.mld['baz'] = 4
        self.assertEqual(4, self.mld['baz'])

    def test_multilookupdict_can_set_new_item(self):
        self.mld['wakka'] = 1
        self.assertEqual(1, self.mld['wakka'])

    def test_multilookupdict_can_set_with_alias(self):
        self.mld['bar'] = 2
        self.assertEqual(2, self.mld['[foo]'])
