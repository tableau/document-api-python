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
        # We should never hit this.
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

    def _get_real_key(self, key):
        if key in self._indexes['alias']:
            return self._indexes['alias'][key]
        if key in self._indexes['caption']:
            return self._indexes['caption'][key]

        return key

    def __setitem__(self, key, value):
        real_key = self._get_real_key(key)

        dict.__setitem__(self, real_key, value)

    def get(self, key, default_value=_no_default_value):
        try:
            return self[key]
        except KeyError:
            if default_value is not _no_default_value:
                return default_value
            raise

    def __getitem__(self, key):
        real_key = self._get_real_key(key)
        return dict.__getitem__(self, real_key)
