# This file contains local-typ to value mappings for metadata-records
# TODO: This might or might not be database-specific.
postgres = {
    'integer': {
        'local-type': 'integer',
        'remote-type': '3',
        'aggregation': 'Sum',
        'precision': '10',
        'contains-null': 'true',
        '__extra__': {
            'attributes': {
                'DebugRemoteType': 'SQL_INTEGER',
                'DebugWireType': 'SQL_C_SLONG'
            }
        }
    },
    'string': {
        'local-type': 'string',
        'remote-type': '130',
        'aggregation': 'Count',
        'cast-to-local-type': 'true',
        'width': '8190',
        'contains-null': 'true',
        '__extra__': {
            'collation': {
                'flag': '0',
                'name': 'LEN_RUS'
            },
            'attributes': {
                'DebugRemoteType': 'SQL_WLONGVARCHAR',
                'DebugWireType': 'SQL_C_WCHAR'
            }
        }
    },
    'boolean': {
        'local-type': 'boolean',
        'remote-type': '11',
        'aggregation': 'Count',
        'contains-null': 'true',
        '__extra__': {
            'attributes': {
                'DebugRemoteType': 'SQL_BIT',
                'DebugWireType': 'SQL_C_BIT'
            }
        }
    },
    'date': {
        'local-type': 'date',
        'remote-type': '7',
        'aggregation': 'Year',
        'contains-null': 'true',
        '__extra__': {
            'attributes': {
                'DebugRemoteType': 'SQL_TYPE_DATE',
                'DebugWireType': 'SQL_C_TYPE_DATE'
            }
        }
    },
    'real': {
        'local-type': 'real',
        'remote-type': '131',
        'aggregation': 'Sum',
        'precision': '28',
        'contains-null': 'true',
        '__extra__': {
            'attributes': {
                'DebugRemoteType': 'SQL_NUMERIC',
                'DebugWireType': 'SQL_C_NUMERIC'
            }
        }
    }
}
