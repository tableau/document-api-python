import weakref


_no_default_value = object()


def _resolve_value(key, value):
    retval = None
    try:
        if hasattr(value, 'get'):
            retval = value.get(key, None)

        if retval is None:
            retval = getattr(value, key, None)
    except AttributeError:
        retval = None
    return retval


def _build_index(key, d):
    return {_resolve_value(key, v): k
            for k, v in d.items()
            if _resolve_value(key, v) is not None}


# TODO: Improve this to be more generic
class MultiLookupDict(dict):
    def __init__(self, args=None):
        if args is None:
            args = {}
        super(MultiLookupDict, self).__init__(args)
        self._indexes = {
            'alias': weakref.WeakValueDictionary(),
            'caption': weakref.WeakValueDictionary()
        }
        self._populate_indexes()

    def _populate_indexes(self):
        self._indexes['alias'] = _build_index('alias', self)
        self._indexes['caption'] = _build_index('caption', self)

    def __setitem__(self, key, value):
        alias = _resolve_value('alias', value)
        caption = _resolve_value('caption', value)
        if alias is not None:
            self._indexes['alias'][alias] = key
        if caption is not None:
            self._indexes['caption'][caption] = key

        dict.__setitem__(self, key, value)

    def get(self, key, default_value=_no_default_value):
        try:
            return self[key]
        except KeyError:
            if default_value is not _no_default_value:
                return default_value
            raise

    def __getitem__(self, key):
        if key in self._indexes['alias']:
            key = self._indexes['alias'][key]
        elif key in self._indexes['caption']:
            key = self._indexes['caption'][key]

        return dict.__getitem__(self, key)
