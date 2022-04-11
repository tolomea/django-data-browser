# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_query_csv_pivot_permutations[----] key'] = [
]

snapshots['test_query_csv_pivot_permutations[---b] key'] = [
    [
        'ID count',
        'Size max'
    ],
    [
        '0.0',
        ''
    ]
]

snapshots['test_query_csv_pivot_permutations[--c-] key'] = [
    [
        'Created time month'
    ]
]

snapshots['test_query_csv_pivot_permutations[--cb] key'] = [
    [
        'Created time month'
    ],
    [
        '',
        'ID count',
        'Size max'
    ]
]

snapshots['test_query_csv_pivot_permutations[-r--] key'] = [
    [
        'Created time year'
    ]
]

snapshots['test_query_csv_pivot_permutations[-r-b] key'] = [
    [
        'Created time year',
        'ID count',
        'Size max'
    ]
]

snapshots['test_query_csv_pivot_permutations[-rc-] key'] = [
    [
        'Created time month'
    ],
    [
        'Created time year'
    ]
]

snapshots['test_query_csv_pivot_permutations[-rcb] key'] = [
    [
        'Created time month'
    ],
    [
        'Created time year',
        'ID count',
        'Size max'
    ]
]

snapshots['test_query_csv_pivot_permutations[d---] key'] = [
]

snapshots['test_query_csv_pivot_permutations[d--b] key'] = [
    [
        'ID count',
        'Size max'
    ],
    [
        '6.0',
        '6.0'
    ]
]

snapshots['test_query_csv_pivot_permutations[d-c-] key'] = [
    [
        'Created time month',
        'January',
        'February'
    ]
]

snapshots['test_query_csv_pivot_permutations[d-cb] key'] = [
    [
        'Created time month',
        'January',
        '',
        'February',
        ''
    ],
    [
        '',
        'ID count',
        'Size max',
        'ID count',
        'Size max'
    ],
    [
        '',
        '4.0',
        '6.0',
        '2.0',
        '3.0'
    ]
]

snapshots['test_query_csv_pivot_permutations[dr--] key'] = [
    [
        'Created time year'
    ],
    [
        '2020.0'
    ],
    [
        '2021.0'
    ]
]

snapshots['test_query_csv_pivot_permutations[dr-b] key'] = [
    [
        'Created time year',
        'ID count',
        'Size max'
    ],
    [
        '2020.0',
        '3.0',
        '3.0'
    ],
    [
        '2021.0',
        '3.0',
        '6.0'
    ]
]

snapshots['test_query_csv_pivot_permutations[drc-] key'] = [
    [
        'Created time month',
        'January',
        'February'
    ],
    [
        'Created time year'
    ],
    [
        '2020.0'
    ],
    [
        '2021.0'
    ]
]

snapshots['test_query_csv_pivot_permutations[drcb] key'] = [
    [
        'Created time month',
        'January',
        '',
        'February',
        ''
    ],
    [
        'Created time year',
        'ID count',
        'Size max',
        'ID count',
        'Size max'
    ],
    [
        '2020.0',
        '1.0',
        '1.0',
        '2.0',
        '3.0'
    ],
    [
        '2021.0',
        '3.0',
        '6.0',
        '',
        ''
    ]
]

snapshots['test_query_ctx config'] = {
    'allModelFields': {
        'auth.Group': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected groups'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected groups'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'name'
            ]
        },
        'auth.User': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected users'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'date_joined': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Date joined',
                    'toMany': False,
                    'type': 'datetime'
                },
                'email': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Email address',
                    'toMany': False,
                    'type': 'string'
                },
                'first_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'First name',
                    'toMany': False,
                    'type': 'string'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected users'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'is_active': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Active',
                    'toMany': False,
                    'type': 'boolean'
                },
                'is_staff': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Staff status',
                    'toMany': False,
                    'type': 'boolean'
                },
                'is_superuser': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Superuser status',
                    'toMany': False,
                    'type': 'boolean'
                },
                'last_login': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Last login',
                    'toMany': False,
                    'type': 'datetime'
                },
                'last_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Last name',
                    'toMany': False,
                    'type': 'string'
                },
                'password': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Password',
                    'toMany': False,
                    'type': 'string'
                },
                'username': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Username',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'is_active',
                'date_joined',
                'email',
                'first_name',
                'last_login',
                'last_name',
                'password',
                'is_staff',
                'is_superuser',
                'username'
            ]
        },
        'boolean': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'is_null',
                'sum'
            ]
        },
        'booleanarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'core.Address': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected addresss'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'andrew': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Andrew',
                    'toMany': False,
                    'type': 'string'
                },
                'bob': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Bob',
                    'toMany': False,
                    'type': 'html'
                },
                'city': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'City',
                    'toMany': False,
                    'type': 'string'
                },
                'fred': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Fred',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected addresss'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'producer': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Producer',
                    'prettyName': 'Producer',
                    'toMany': False,
                    'type': None
                },
                'tom': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Tom',
                    'toMany': False,
                    'type': 'html'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'andrew',
                'bob',
                'city',
                'fred',
                'producer',
                'tom'
            ]
        },
        'core.InAdmin': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected in admins'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected in admins'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'name'
            ]
        },
        'core.InlineAdmin': {
            'defaultFilters': [
            ],
            'fields': {
                'id': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'in_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InAdmin',
                    'prettyName': 'In admin',
                    'toMany': False,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'in_admin',
                'name'
            ]
        },
        'core.Normal': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected normals'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected normals'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'in_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InAdmin',
                    'prettyName': 'In admin',
                    'toMany': False,
                    'type': None
                },
                'inline_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InlineAdmin',
                    'prettyName': 'Inline admin',
                    'toMany': False,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'not_in_admin': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Not in admin',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'in_admin',
                'inline_admin',
                'name',
                'not_in_admin'
            ]
        },
        'core.Producer': {
            'defaultFilters': [
            ],
            'fields': {
                'address': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Address',
                    'prettyName': 'Address',
                    'toMany': False,
                    'type': None
                },
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected producers'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'frank': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Frank',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected producers'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'address',
                'frank',
                'name'
            ]
        },
        'core.Product': {
            'defaultFilters': [
                {
                    'lookup': 'a_lookup',
                    'pathStr': 'a_field',
                    'value': 'a_value'
                },
                {
                    'lookup': 'not_equals',
                    'pathStr': 'name',
                    'value': 'not a thing'
                },
                {
                    'lookup': 'a_lookup',
                    'pathStr': 'a_field',
                    'value': 'true'
                }
            ],
            'fields': {
                '_underscore': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': ' underscore',
                    'toMany': False,
                    'type': 'number'
                },
                'admin': {
                    'actions': [
                        {
                            'name': 'an_action',
                            'prettyName': 'An action'
                        },
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected products'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'annotated': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Annotated',
                    'toMany': False,
                    'type': 'string'
                },
                'boat': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Boat',
                    'toMany': False,
                    'type': 'number'
                },
                'calculated_boolean': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Calculated boolean',
                    'toMany': False,
                    'type': 'boolean'
                },
                'created_time': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Created time',
                    'toMany': False,
                    'type': 'datetime'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'date',
                    'prettyName': 'Date',
                    'toMany': False,
                    'type': 'date'
                },
                'default_sku': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.SKU',
                    'prettyName': 'Default sku',
                    'toMany': False,
                    'type': None
                },
                'duration': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'duration',
                    'prettyName': 'Duration',
                    'toMany': False,
                    'type': 'duration'
                },
                'extra_inline': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Extra inline',
                    'toMany': False,
                    'type': 'string'
                },
                'extra_model': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Extra model',
                    'toMany': False,
                    'type': 'string'
                },
                'fake': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'unknown',
                    'prettyName': 'Fake',
                    'toMany': False,
                    'type': 'unknown'
                },
                'funky': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Funky',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'an_action',
                            'prettyName': 'An action'
                        },
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected products'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'image': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'url',
                    'prettyName': 'Image',
                    'toMany': False,
                    'type': 'url'
                },
                'is_onsale': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Is onsale',
                    'toMany': False,
                    'type': 'html'
                },
                'lambda': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Lambda',
                    'toMany': False,
                    'type': 'html'
                },
                'model_not_in_admin': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Model not in admin',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'number_choice': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'A',
                        'B'
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberchoice',
                    'prettyName': 'Number choice',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'only_in_list_view': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Only in list view',
                    'toMany': False,
                    'type': 'string'
                },
                'onsale': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Onsale',
                    'toMany': False,
                    'type': 'boolean'
                },
                'other_annotation': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Other annotation',
                    'toMany': False,
                    'type': 'string'
                },
                'producer': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Producer',
                    'prettyName': 'Producer',
                    'toMany': False,
                    'type': None
                },
                'size': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Size',
                    'toMany': False,
                    'type': 'number'
                },
                'size_unit': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Size unit',
                    'toMany': False,
                    'type': 'string'
                },
                'stealth_annotation': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Stealth annotation',
                    'toMany': False,
                    'type': 'string'
                },
                'string_choice': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'A',
                        'B'
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringchoice',
                    'prettyName': 'String choice',
                    'toMany': False,
                    'type': 'stringchoice'
                },
                'url': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'url',
                    'prettyName': 'Url',
                    'toMany': False,
                    'type': 'url'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                '_underscore',
                'annotated',
                'boat',
                'calculated_boolean',
                'created_time',
                'date',
                'default_sku',
                'duration',
                'extra_inline',
                'extra_model',
                'fake',
                'funky',
                'image',
                'is_onsale',
                'lambda',
                'model_not_in_admin',
                'name',
                'number_choice',
                'only_in_list_view',
                'onsale',
                'other_annotation',
                'producer',
                'size',
                'size_unit',
                'stealth_annotation',
                'string_choice',
                'url'
            ]
        },
        'core.SKU': {
            'defaultFilters': [
            ],
            'fields': {
                'bob': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Bob',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'product': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Product',
                    'prettyName': 'Product',
                    'toMany': False,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'bob',
                'name',
                'product'
            ]
        },
        'core.Tag': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected tags'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'name': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected tags'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'name',
                'admin'
            ]
        },
        'data_browser.View': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected views'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'created_time': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Created time',
                    'toMany': False,
                    'type': 'datetime'
                },
                'description': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Description',
                    'toMany': False,
                    'type': 'string'
                },
                'fields': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Fields',
                    'toMany': False,
                    'type': 'string'
                },
                'google_sheets_formula': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Google sheets formula',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected views'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Id',
                    'toMany': False,
                    'type': 'string'
                },
                'limit': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Limit',
                    'toMany': False,
                    'type': 'number'
                },
                'model_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Model name',
                    'toMany': False,
                    'type': 'string'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'open_view': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Open view',
                    'toMany': False,
                    'type': 'html'
                },
                'owner': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'auth.User',
                    'prettyName': 'Owner',
                    'toMany': False,
                    'type': None
                },
                'public': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Public',
                    'toMany': False,
                    'type': 'boolean'
                },
                'public_link': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Public link',
                    'toMany': False,
                    'type': 'html'
                },
                'public_slug': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Public slug',
                    'toMany': False,
                    'type': 'string'
                },
                'query': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Query',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'created_time',
                'description',
                'fields',
                'google_sheets_formula',
                'limit',
                'model_name',
                'name',
                'open_view',
                'owner',
                'public',
                'public_link',
                'public_slug',
                'query'
            ]
        },
        'date': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'date'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'date'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'day',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'month',
                'month_start',
                'quarter',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'datetime': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'date',
                    'toMany': False,
                    'type': 'date'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'hour': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'hour',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'datetime'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'datetime'
                },
                'minute': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'minute',
                    'toMany': False,
                    'type': 'number'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'second': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'second',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'date',
                'day',
                'hour',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'minute',
                'month',
                'month_start',
                'quarter',
                'second',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datetimearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'duration': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'duration'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'duration'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'duration'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'duration'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'sum'
            ]
        },
        'durationarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'html': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'isnull': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'json': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'number': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'number'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'number'
                },
                'std_dev': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'std dev',
                    'toMany': False,
                    'type': 'number'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                },
                'variance': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'variance',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'std_dev',
                'sum',
                'variance'
            ]
        },
        'numberarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'numberchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'numberchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'numberarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'regex': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'string': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringable': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'stringchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'stringarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'unknown': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'url': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'uuid': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        }
    },
    'baseUrl': '/data_browser/',
    'canMakePublic': True,
    'defaultRowLimit': 1000,
    'sentryDsn': None,
    'sortedModels': [
        'auth.Group',
        'auth.User',
        'core.Address',
        'core.InAdmin',
        'core.InlineAdmin',
        'core.Normal',
        'core.Producer',
        'core.Product',
        'core.SKU',
        'core.Tag',
        'data_browser.View'
    ],
    'types': {
        'boolean': {
            'defaultLookup': 'equals',
            'defaultValue': True,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'boolean'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'boolean'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'booleanarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'boolean'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'booleanarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'boolean'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'booleanarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'date': {
            'defaultLookup': 'equals',
            'defaultValue': 'today',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'date'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'date'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'date'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'date'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'date'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'date'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'datetime': {
            'defaultLookup': 'equals',
            'defaultValue': 'now',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetime'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'datetime'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'datetime'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'datetime'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetime'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datetimearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'datetime'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetimearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetimearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'duration': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'duration'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'duration'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'duration'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'duration'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'duration'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'durationarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'duration'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'durationarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'durationarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'html': {
            'defaultLookup': 'is_null',
            'defaultValue': '',
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'isnull': {
            'defaultLookup': 'equals',
            'defaultValue': 'IsNull',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'equals'
            ]
        },
        'json': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'json'
                },
                'field_equals': {
                    'prettyName': 'field equals',
                    'type': 'jsonfield'
                },
                'has_key': {
                    'prettyName': 'has key',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'json'
                },
                'not_field_equals': {
                    'prettyName': 'not field equals',
                    'type': 'jsonfield'
                },
                'not_has_key': {
                    'prettyName': 'not has key',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'has_key',
                'field_equals',
                'not_equals',
                'not_has_key',
                'not_field_equals',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultLookup': 'equals',
            'defaultValue': '|',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'jsonfield'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'jsonfield'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'number': {
            'defaultLookup': 'equals',
            'defaultValue': 0,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'number'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'number'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'number'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'number'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'numberarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'number'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'numberchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'numberchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'numberchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'numberchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'regex': {
            'defaultLookup': 'equals',
            'defaultValue': '.*',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'regex'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'regex'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'string': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'string'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'string'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'stringable': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringable'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringable'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringable'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringablearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringable'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringablearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'unknown': {
            'defaultLookup': 'is_null',
            'defaultValue': None,
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'url': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'url'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'url'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'url'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'url'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'urlarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'urlarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'uuid': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuid'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuid'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'uuid'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuidarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'uuid'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuidarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        }
    }
}

snapshots['test_query_ctx_m2m config'] = {
    'allModelFields': {
        'auth.Group': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected groups'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected groups'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'user': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'auth.User',
                    'prettyName': 'User set',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'name',
                'user'
            ]
        },
        'auth.User': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected users'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'date_joined': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Date joined',
                    'toMany': False,
                    'type': 'datetime'
                },
                'email': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Email address',
                    'toMany': False,
                    'type': 'string'
                },
                'first_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'First name',
                    'toMany': False,
                    'type': 'string'
                },
                'groups': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'auth.Group',
                    'prettyName': 'Groups',
                    'toMany': True,
                    'type': None
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected users'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'is_active': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Active',
                    'toMany': False,
                    'type': 'boolean'
                },
                'is_staff': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Staff status',
                    'toMany': False,
                    'type': 'boolean'
                },
                'is_superuser': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Superuser status',
                    'toMany': False,
                    'type': 'boolean'
                },
                'last_login': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Last login',
                    'toMany': False,
                    'type': 'datetime'
                },
                'last_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Last name',
                    'toMany': False,
                    'type': 'string'
                },
                'password': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Password',
                    'toMany': False,
                    'type': 'string'
                },
                'username': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Username',
                    'toMany': False,
                    'type': 'string'
                },
                'view': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'data_browser.View',
                    'prettyName': 'View set',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'is_active',
                'date_joined',
                'email',
                'first_name',
                'groups',
                'last_login',
                'last_name',
                'password',
                'is_staff',
                'is_superuser',
                'username',
                'view'
            ]
        },
        'boolean': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'is_null',
                'sum'
            ]
        },
        'booleanarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'core.Address': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected addresss'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'andrew': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Andrew',
                    'toMany': False,
                    'type': 'string'
                },
                'bob': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Bob',
                    'toMany': False,
                    'type': 'html'
                },
                'city': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'City',
                    'toMany': False,
                    'type': 'string'
                },
                'fred': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Fred',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected addresss'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'producer': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Producer',
                    'prettyName': 'Producer',
                    'toMany': False,
                    'type': None
                },
                'tom': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Tom',
                    'toMany': False,
                    'type': 'html'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'andrew',
                'bob',
                'city',
                'fred',
                'producer',
                'tom'
            ]
        },
        'core.InAdmin': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected in admins'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected in admins'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'inlineadmin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InlineAdmin',
                    'prettyName': 'Inlineadmin set',
                    'toMany': True,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'normal': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Normal',
                    'prettyName': 'Normal set',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'inlineadmin',
                'name',
                'normal'
            ]
        },
        'core.InlineAdmin': {
            'defaultFilters': [
            ],
            'fields': {
                'id': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'in_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InAdmin',
                    'prettyName': 'In admin',
                    'toMany': False,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'normal': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Normal',
                    'prettyName': 'Normal set',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'in_admin',
                'name',
                'normal'
            ]
        },
        'core.Normal': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected normals'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected normals'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'in_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InAdmin',
                    'prettyName': 'In admin',
                    'toMany': False,
                    'type': None
                },
                'inline_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InlineAdmin',
                    'prettyName': 'Inline admin',
                    'toMany': False,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'not_in_admin': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Not in admin',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'in_admin',
                'inline_admin',
                'name',
                'not_in_admin'
            ]
        },
        'core.Producer': {
            'defaultFilters': [
            ],
            'fields': {
                'address': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Address',
                    'prettyName': 'Address',
                    'toMany': False,
                    'type': None
                },
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected producers'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'frank': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Frank',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected producers'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'products': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Product',
                    'prettyName': 'Product set',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'address',
                'frank',
                'name',
                'products'
            ]
        },
        'core.Product': {
            'defaultFilters': [
                {
                    'lookup': 'a_lookup',
                    'pathStr': 'a_field',
                    'value': 'a_value'
                },
                {
                    'lookup': 'not_equals',
                    'pathStr': 'name',
                    'value': 'not a thing'
                },
                {
                    'lookup': 'a_lookup',
                    'pathStr': 'a_field',
                    'value': 'true'
                }
            ],
            'fields': {
                '_underscore': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': ' underscore',
                    'toMany': False,
                    'type': 'number'
                },
                'admin': {
                    'actions': [
                        {
                            'name': 'an_action',
                            'prettyName': 'An action'
                        },
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected products'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'annotated': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Annotated',
                    'toMany': False,
                    'type': 'string'
                },
                'boat': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Boat',
                    'toMany': False,
                    'type': 'number'
                },
                'calculated_boolean': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Calculated boolean',
                    'toMany': False,
                    'type': 'boolean'
                },
                'created_time': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Created time',
                    'toMany': False,
                    'type': 'datetime'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'date',
                    'prettyName': 'Date',
                    'toMany': False,
                    'type': 'date'
                },
                'default_sku': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.SKU',
                    'prettyName': 'Default sku',
                    'toMany': False,
                    'type': None
                },
                'duration': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'duration',
                    'prettyName': 'Duration',
                    'toMany': False,
                    'type': 'duration'
                },
                'extra_inline': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Extra inline',
                    'toMany': False,
                    'type': 'string'
                },
                'extra_model': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Extra model',
                    'toMany': False,
                    'type': 'string'
                },
                'fake': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'unknown',
                    'prettyName': 'Fake',
                    'toMany': False,
                    'type': 'unknown'
                },
                'funky': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Funky',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'an_action',
                            'prettyName': 'An action'
                        },
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected products'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'image': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'url',
                    'prettyName': 'Image',
                    'toMany': False,
                    'type': 'url'
                },
                'is_onsale': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Is onsale',
                    'toMany': False,
                    'type': 'html'
                },
                'lambda': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Lambda',
                    'toMany': False,
                    'type': 'html'
                },
                'model_not_in_admin': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Model not in admin',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'number_choice': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'A',
                        'B'
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberchoice',
                    'prettyName': 'Number choice',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'only_in_list_view': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Only in list view',
                    'toMany': False,
                    'type': 'string'
                },
                'onsale': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Onsale',
                    'toMany': False,
                    'type': 'boolean'
                },
                'other_annotation': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Other annotation',
                    'toMany': False,
                    'type': 'string'
                },
                'producer': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Producer',
                    'prettyName': 'Producer',
                    'toMany': False,
                    'type': None
                },
                'size': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Size',
                    'toMany': False,
                    'type': 'number'
                },
                'size_unit': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Size unit',
                    'toMany': False,
                    'type': 'string'
                },
                'sku': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.SKU',
                    'prettyName': 'Sku set',
                    'toMany': True,
                    'type': None
                },
                'stealth_annotation': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Stealth annotation',
                    'toMany': False,
                    'type': 'string'
                },
                'string_choice': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'A',
                        'B'
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringchoice',
                    'prettyName': 'String choice',
                    'toMany': False,
                    'type': 'stringchoice'
                },
                'tags': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Tag',
                    'prettyName': 'Tags',
                    'toMany': True,
                    'type': None
                },
                'url': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'url',
                    'prettyName': 'Url',
                    'toMany': False,
                    'type': 'url'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                '_underscore',
                'annotated',
                'boat',
                'calculated_boolean',
                'created_time',
                'date',
                'default_sku',
                'duration',
                'extra_inline',
                'extra_model',
                'fake',
                'funky',
                'image',
                'is_onsale',
                'lambda',
                'model_not_in_admin',
                'name',
                'number_choice',
                'only_in_list_view',
                'onsale',
                'other_annotation',
                'producer',
                'size',
                'size_unit',
                'sku',
                'stealth_annotation',
                'string_choice',
                'tags',
                'url'
            ]
        },
        'core.SKU': {
            'defaultFilters': [
            ],
            'fields': {
                'bob': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Bob',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'product': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Product',
                    'prettyName': 'Product',
                    'toMany': False,
                    'type': None
                },
                'products': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Product',
                    'prettyName': 'Products',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'bob',
                'name',
                'product',
                'products'
            ]
        },
        'core.Tag': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected tags'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'name': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected tags'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'product': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Product',
                    'prettyName': 'Product set',
                    'toMany': True,
                    'type': None
                }
            },
            'sortedFields': [
                'name',
                'admin',
                'product'
            ]
        },
        'data_browser.View': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected views'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'created_time': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Created time',
                    'toMany': False,
                    'type': 'datetime'
                },
                'description': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Description',
                    'toMany': False,
                    'type': 'string'
                },
                'fields': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Fields',
                    'toMany': False,
                    'type': 'string'
                },
                'google_sheets_formula': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Google sheets formula',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected views'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Id',
                    'toMany': False,
                    'type': 'string'
                },
                'limit': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Limit',
                    'toMany': False,
                    'type': 'number'
                },
                'model_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Model name',
                    'toMany': False,
                    'type': 'string'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'open_view': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Open view',
                    'toMany': False,
                    'type': 'html'
                },
                'owner': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'auth.User',
                    'prettyName': 'Owner',
                    'toMany': False,
                    'type': None
                },
                'public': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Public',
                    'toMany': False,
                    'type': 'boolean'
                },
                'public_link': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Public link',
                    'toMany': False,
                    'type': 'html'
                },
                'public_slug': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Public slug',
                    'toMany': False,
                    'type': 'string'
                },
                'query': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Query',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'created_time',
                'description',
                'fields',
                'google_sheets_formula',
                'limit',
                'model_name',
                'name',
                'open_view',
                'owner',
                'public',
                'public_link',
                'public_slug',
                'query'
            ]
        },
        'date': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'date'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'date'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'day',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'month',
                'month_start',
                'quarter',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'datetime': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'date',
                    'toMany': False,
                    'type': 'date'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'hour': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'hour',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'datetime'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'datetime'
                },
                'minute': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'minute',
                    'toMany': False,
                    'type': 'number'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'second': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'second',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'date',
                'day',
                'hour',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'minute',
                'month',
                'month_start',
                'quarter',
                'second',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datetimearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'duration': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'duration'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'duration'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'duration'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'duration'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'sum'
            ]
        },
        'durationarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'html': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'isnull': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'json': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'number': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'number'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'number'
                },
                'std_dev': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'std dev',
                    'toMany': False,
                    'type': 'number'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                },
                'variance': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'variance',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'std_dev',
                'sum',
                'variance'
            ]
        },
        'numberarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'numberchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'numberchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'numberarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'regex': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'string': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringable': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'stringchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'stringarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'unknown': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'url': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'uuid': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        }
    },
    'baseUrl': '/data_browser/',
    'canMakePublic': True,
    'defaultRowLimit': 1000,
    'sentryDsn': None,
    'sortedModels': [
        'auth.Group',
        'auth.User',
        'core.Address',
        'core.InAdmin',
        'core.InlineAdmin',
        'core.Normal',
        'core.Producer',
        'core.Product',
        'core.SKU',
        'core.Tag',
        'data_browser.View'
    ],
    'types': {
        'boolean': {
            'defaultLookup': 'equals',
            'defaultValue': True,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'boolean'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'boolean'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'booleanarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'boolean'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'booleanarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'boolean'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'booleanarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'date': {
            'defaultLookup': 'equals',
            'defaultValue': 'today',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'date'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'date'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'date'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'date'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'date'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'date'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'datetime': {
            'defaultLookup': 'equals',
            'defaultValue': 'now',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetime'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'datetime'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'datetime'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'datetime'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetime'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datetimearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'datetime'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetimearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetimearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'duration': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'duration'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'duration'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'duration'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'duration'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'duration'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'durationarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'duration'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'durationarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'durationarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'html': {
            'defaultLookup': 'is_null',
            'defaultValue': '',
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'isnull': {
            'defaultLookup': 'equals',
            'defaultValue': 'IsNull',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'equals'
            ]
        },
        'json': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'json'
                },
                'field_equals': {
                    'prettyName': 'field equals',
                    'type': 'jsonfield'
                },
                'has_key': {
                    'prettyName': 'has key',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'json'
                },
                'not_field_equals': {
                    'prettyName': 'not field equals',
                    'type': 'jsonfield'
                },
                'not_has_key': {
                    'prettyName': 'not has key',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'has_key',
                'field_equals',
                'not_equals',
                'not_has_key',
                'not_field_equals',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultLookup': 'equals',
            'defaultValue': '|',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'jsonfield'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'jsonfield'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'number': {
            'defaultLookup': 'equals',
            'defaultValue': 0,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'number'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'number'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'number'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'number'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'numberarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'number'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'numberchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'numberchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'numberchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'numberchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'regex': {
            'defaultLookup': 'equals',
            'defaultValue': '.*',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'regex'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'regex'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'string': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'string'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'string'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'stringable': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringable'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringable'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringable'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringablearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringable'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringablearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'unknown': {
            'defaultLookup': 'is_null',
            'defaultValue': None,
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'url': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'url'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'url'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'url'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'url'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'urlarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'urlarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'uuid': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuid'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuid'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'uuid'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuidarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'uuid'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuidarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        }
    }
}

snapshots['test_query_html config'] = {
    'allModelFields': {
        'auth.Group': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected groups'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected groups'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'name'
            ]
        },
        'auth.User': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected users'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'date_joined': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Date joined',
                    'toMany': False,
                    'type': 'datetime'
                },
                'email': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Email address',
                    'toMany': False,
                    'type': 'string'
                },
                'first_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'First name',
                    'toMany': False,
                    'type': 'string'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected users'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'is_active': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Active',
                    'toMany': False,
                    'type': 'boolean'
                },
                'is_staff': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Staff status',
                    'toMany': False,
                    'type': 'boolean'
                },
                'is_superuser': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Superuser status',
                    'toMany': False,
                    'type': 'boolean'
                },
                'last_login': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Last login',
                    'toMany': False,
                    'type': 'datetime'
                },
                'last_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Last name',
                    'toMany': False,
                    'type': 'string'
                },
                'password': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Password',
                    'toMany': False,
                    'type': 'string'
                },
                'username': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Username',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'is_active',
                'date_joined',
                'email',
                'first_name',
                'last_login',
                'last_name',
                'password',
                'is_staff',
                'is_superuser',
                'username'
            ]
        },
        'boolean': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'is_null',
                'sum'
            ]
        },
        'booleanarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'core.Address': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected addresss'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'andrew': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Andrew',
                    'toMany': False,
                    'type': 'string'
                },
                'bob': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Bob',
                    'toMany': False,
                    'type': 'html'
                },
                'city': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'City',
                    'toMany': False,
                    'type': 'string'
                },
                'fred': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Fred',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected addresss'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'producer': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Producer',
                    'prettyName': 'Producer',
                    'toMany': False,
                    'type': None
                },
                'tom': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Tom',
                    'toMany': False,
                    'type': 'html'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'andrew',
                'bob',
                'city',
                'fred',
                'producer',
                'tom'
            ]
        },
        'core.InAdmin': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected in admins'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected in admins'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'name'
            ]
        },
        'core.InlineAdmin': {
            'defaultFilters': [
            ],
            'fields': {
                'id': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'in_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InAdmin',
                    'prettyName': 'In admin',
                    'toMany': False,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'in_admin',
                'name'
            ]
        },
        'core.Normal': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected normals'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected normals'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'in_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InAdmin',
                    'prettyName': 'In admin',
                    'toMany': False,
                    'type': None
                },
                'inline_admin': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.InlineAdmin',
                    'prettyName': 'Inline admin',
                    'toMany': False,
                    'type': None
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'not_in_admin': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Not in admin',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'in_admin',
                'inline_admin',
                'name',
                'not_in_admin'
            ]
        },
        'core.Producer': {
            'defaultFilters': [
            ],
            'fields': {
                'address': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Address',
                    'prettyName': 'Address',
                    'toMany': False,
                    'type': None
                },
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected producers'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'frank': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Frank',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected producers'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'address',
                'frank',
                'name'
            ]
        },
        'core.Product': {
            'defaultFilters': [
                {
                    'lookup': 'a_lookup',
                    'pathStr': 'a_field',
                    'value': 'a_value'
                },
                {
                    'lookup': 'not_equals',
                    'pathStr': 'name',
                    'value': 'not a thing'
                },
                {
                    'lookup': 'a_lookup',
                    'pathStr': 'a_field',
                    'value': 'true'
                }
            ],
            'fields': {
                '_underscore': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': ' underscore',
                    'toMany': False,
                    'type': 'number'
                },
                'admin': {
                    'actions': [
                        {
                            'name': 'an_action',
                            'prettyName': 'An action'
                        },
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected products'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'annotated': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Annotated',
                    'toMany': False,
                    'type': 'string'
                },
                'boat': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Boat',
                    'toMany': False,
                    'type': 'number'
                },
                'calculated_boolean': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Calculated boolean',
                    'toMany': False,
                    'type': 'boolean'
                },
                'created_time': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Created time',
                    'toMany': False,
                    'type': 'datetime'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'date',
                    'prettyName': 'Date',
                    'toMany': False,
                    'type': 'date'
                },
                'default_sku': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.SKU',
                    'prettyName': 'Default sku',
                    'toMany': False,
                    'type': None
                },
                'duration': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'duration',
                    'prettyName': 'Duration',
                    'toMany': False,
                    'type': 'duration'
                },
                'extra_inline': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Extra inline',
                    'toMany': False,
                    'type': 'string'
                },
                'extra_model': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Extra model',
                    'toMany': False,
                    'type': 'string'
                },
                'fake': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'unknown',
                    'prettyName': 'Fake',
                    'toMany': False,
                    'type': 'unknown'
                },
                'funky': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Funky',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'an_action',
                            'prettyName': 'An action'
                        },
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected products'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'image': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'url',
                    'prettyName': 'Image',
                    'toMany': False,
                    'type': 'url'
                },
                'is_onsale': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Is onsale',
                    'toMany': False,
                    'type': 'html'
                },
                'lambda': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Lambda',
                    'toMany': False,
                    'type': 'html'
                },
                'model_not_in_admin': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Model not in admin',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'number_choice': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'A',
                        'B'
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberchoice',
                    'prettyName': 'Number choice',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'only_in_list_view': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Only in list view',
                    'toMany': False,
                    'type': 'string'
                },
                'onsale': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Onsale',
                    'toMany': False,
                    'type': 'boolean'
                },
                'other_annotation': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Other annotation',
                    'toMany': False,
                    'type': 'string'
                },
                'producer': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Producer',
                    'prettyName': 'Producer',
                    'toMany': False,
                    'type': None
                },
                'size': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Size',
                    'toMany': False,
                    'type': 'number'
                },
                'size_unit': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Size unit',
                    'toMany': False,
                    'type': 'string'
                },
                'stealth_annotation': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Stealth annotation',
                    'toMany': False,
                    'type': 'string'
                },
                'string_choice': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'A',
                        'B'
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringchoice',
                    'prettyName': 'String choice',
                    'toMany': False,
                    'type': 'stringchoice'
                },
                'url': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'url',
                    'prettyName': 'Url',
                    'toMany': False,
                    'type': 'url'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                '_underscore',
                'annotated',
                'boat',
                'calculated_boolean',
                'created_time',
                'date',
                'default_sku',
                'duration',
                'extra_inline',
                'extra_model',
                'fake',
                'funky',
                'image',
                'is_onsale',
                'lambda',
                'model_not_in_admin',
                'name',
                'number_choice',
                'only_in_list_view',
                'onsale',
                'other_annotation',
                'producer',
                'size',
                'size_unit',
                'stealth_annotation',
                'string_choice',
                'url'
            ]
        },
        'core.SKU': {
            'defaultFilters': [
            ],
            'fields': {
                'bob': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Bob',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'ID',
                    'toMany': False,
                    'type': 'number'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'product': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'core.Product',
                    'prettyName': 'Product',
                    'toMany': False,
                    'type': None
                }
            },
            'sortedFields': [
                'id',
                'bob',
                'name',
                'product'
            ]
        },
        'core.Tag': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected tags'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'name': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected tags'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'name',
                'admin'
            ]
        },
        'data_browser.View': {
            'defaultFilters': [
            ],
            'fields': {
                'admin': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected views'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Admin',
                    'toMany': False,
                    'type': 'html'
                },
                'created_time': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': 'datetime',
                    'prettyName': 'Created time',
                    'toMany': False,
                    'type': 'datetime'
                },
                'description': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Description',
                    'toMany': False,
                    'type': 'string'
                },
                'fields': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Fields',
                    'toMany': False,
                    'type': 'string'
                },
                'google_sheets_formula': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Google sheets formula',
                    'toMany': False,
                    'type': 'html'
                },
                'id': {
                    'actions': [
                        {
                            'name': 'delete_selected',
                            'prettyName': 'Delete selected views'
                        }
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Id',
                    'toMany': False,
                    'type': 'string'
                },
                'limit': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'Limit',
                    'toMany': False,
                    'type': 'number'
                },
                'model_name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Model name',
                    'toMany': False,
                    'type': 'string'
                },
                'name': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Name',
                    'toMany': False,
                    'type': 'string'
                },
                'open_view': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Open view',
                    'toMany': False,
                    'type': 'html'
                },
                'owner': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': 'auth.User',
                    'prettyName': 'Owner',
                    'toMany': False,
                    'type': None
                },
                'public': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'boolean',
                    'prettyName': 'Public',
                    'toMany': False,
                    'type': 'boolean'
                },
                'public_link': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': False,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'Public link',
                    'toMany': False,
                    'type': 'html'
                },
                'public_slug': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Public slug',
                    'toMany': False,
                    'type': 'string'
                },
                'query': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'Query',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'id',
                'admin',
                'created_time',
                'description',
                'fields',
                'google_sheets_formula',
                'limit',
                'model_name',
                'name',
                'open_view',
                'owner',
                'public',
                'public_link',
                'public_slug',
                'query'
            ]
        },
        'date': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'date'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'date'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'day',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'month',
                'month_start',
                'quarter',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'datetime': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'date',
                    'toMany': False,
                    'type': 'date'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'hour': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'hour',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'datetime'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'datetime'
                },
                'minute': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'minute',
                    'toMany': False,
                    'type': 'number'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'second': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'second',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'date',
                'day',
                'hour',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'minute',
                'month',
                'month_start',
                'quarter',
                'second',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datetimearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'duration': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'duration'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'duration'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'duration'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'duration'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'sum'
            ]
        },
        'durationarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'html': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'isnull': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'json': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'number': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'number'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'number'
                },
                'std_dev': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'std dev',
                    'toMany': False,
                    'type': 'number'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                },
                'variance': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'variance',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'std_dev',
                'sum',
                'variance'
            ]
        },
        'numberarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'numberchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'numberchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'numberarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'regex': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'string': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringable': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'stringchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'stringarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'unknown': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'url': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'uuid': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        }
    },
    'baseUrl': '/data_browser/',
    'canMakePublic': True,
    'defaultRowLimit': 1000,
    'sentryDsn': None,
    'sortedModels': [
        'auth.Group',
        'auth.User',
        'core.Address',
        'core.InAdmin',
        'core.InlineAdmin',
        'core.Normal',
        'core.Producer',
        'core.Product',
        'core.SKU',
        'core.Tag',
        'data_browser.View'
    ],
    'types': {
        'boolean': {
            'defaultLookup': 'equals',
            'defaultValue': True,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'boolean'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'boolean'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'booleanarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'boolean'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'booleanarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'boolean'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'booleanarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'date': {
            'defaultLookup': 'equals',
            'defaultValue': 'today',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'date'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'date'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'date'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'date'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'date'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'date'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'datetime': {
            'defaultLookup': 'equals',
            'defaultValue': 'now',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetime'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'datetime'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'datetime'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'datetime'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetime'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datetimearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'datetime'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetimearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetimearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'duration': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'duration'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'duration'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'duration'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'duration'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'duration'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'durationarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'duration'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'durationarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'durationarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'html': {
            'defaultLookup': 'is_null',
            'defaultValue': '',
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'isnull': {
            'defaultLookup': 'equals',
            'defaultValue': 'IsNull',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'equals'
            ]
        },
        'json': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'json'
                },
                'field_equals': {
                    'prettyName': 'field equals',
                    'type': 'jsonfield'
                },
                'has_key': {
                    'prettyName': 'has key',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'json'
                },
                'not_field_equals': {
                    'prettyName': 'not field equals',
                    'type': 'jsonfield'
                },
                'not_has_key': {
                    'prettyName': 'not has key',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'has_key',
                'field_equals',
                'not_equals',
                'not_has_key',
                'not_field_equals',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultLookup': 'equals',
            'defaultValue': '|',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'jsonfield'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'jsonfield'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'number': {
            'defaultLookup': 'equals',
            'defaultValue': 0,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'number'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'number'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'number'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'number'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'numberarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'number'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'numberchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'numberchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'numberchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'numberchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'regex': {
            'defaultLookup': 'equals',
            'defaultValue': '.*',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'regex'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'regex'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'string': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'string'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'string'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'stringable': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringable'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringable'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringable'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringablearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringable'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringablearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'unknown': {
            'defaultLookup': 'is_null',
            'defaultValue': None,
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'url': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'url'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'url'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'url'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'url'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'urlarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'urlarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'uuid': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuid'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuid'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'uuid'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuidarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'uuid'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuidarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        }
    }
}

snapshots['test_query_html_no_perms config'] = {
    'allModelFields': {
        'boolean': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'is_null',
                'sum'
            ]
        },
        'booleanarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'date': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'date'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'date'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'day',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'month',
                'month_start',
                'quarter',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'datetime': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'date': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'date',
                    'toMany': False,
                    'type': 'date'
                },
                'day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'day',
                    'toMany': False,
                    'type': 'number'
                },
                'hour': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'hour',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'iso_week': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso week',
                    'toMany': False,
                    'type': 'number'
                },
                'iso_year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'iso year',
                    'toMany': False,
                    'type': 'number'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'datetime'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'datetime'
                },
                'minute': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'minute',
                    'toMany': False,
                    'type': 'number'
                },
                'month': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'January',
                        'February',
                        'March',
                        'April',
                        'May',
                        'June',
                        'July',
                        'August',
                        'September',
                        'October',
                        'November',
                        'December'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'month_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'month start',
                    'toMany': False,
                    'type': 'date'
                },
                'quarter': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'quarter',
                    'toMany': False,
                    'type': 'number'
                },
                'second': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'second',
                    'toMany': False,
                    'type': 'number'
                },
                'week_day': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                        'Sunday',
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                        'Saturday'
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week day',
                    'toMany': False,
                    'type': 'numberchoice'
                },
                'week_start': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'week start',
                    'toMany': False,
                    'type': 'date'
                },
                'year': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': 'asc',
                    'model': None,
                    'prettyName': 'year',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'date',
                'day',
                'hour',
                'is_null',
                'iso_week',
                'iso_year',
                'max',
                'min',
                'minute',
                'month',
                'month_start',
                'quarter',
                'second',
                'week_day',
                'week_start',
                'year'
            ]
        },
        'datetimearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'duration': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'duration'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'duration'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'duration'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'duration'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'sum'
            ]
        },
        'durationarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'html': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'isnull': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'json': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'number': {
            'defaultFilters': [
            ],
            'fields': {
                'average': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'average',
                    'toMany': False,
                    'type': 'number'
                },
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'max': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'max',
                    'toMany': False,
                    'type': 'number'
                },
                'min': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'min',
                    'toMany': False,
                    'type': 'number'
                },
                'std_dev': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'std dev',
                    'toMany': False,
                    'type': 'number'
                },
                'sum': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'sum',
                    'toMany': False,
                    'type': 'number'
                },
                'variance': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'variance',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'average',
                'count',
                'is_null',
                'max',
                'min',
                'std_dev',
                'sum',
                'variance'
            ]
        },
        'numberarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'numberchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'number',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'numberchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'numberarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'numberarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'regex': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'string': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringable': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'stringchoice': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'string',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'string'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'raw'
            ]
        },
        'stringchoicearray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                },
                'raw': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': 'stringarray',
                    'prettyName': 'raw',
                    'toMany': False,
                    'type': 'stringarray'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length',
                'raw'
            ]
        },
        'unknown': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'url': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        },
        'uuid': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                }
            },
            'sortedFields': [
                'count',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultFilters': [
            ],
            'fields': {
                'count': {
                    'actions': [
                    ],
                    'canPivot': False,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'count',
                    'toMany': False,
                    'type': 'number'
                },
                'is_null': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'is null',
                    'toMany': False,
                    'type': 'isnull'
                },
                'length': {
                    'actions': [
                    ],
                    'canPivot': True,
                    'choices': [
                    ],
                    'concrete': True,
                    'defaultSort': None,
                    'model': None,
                    'prettyName': 'length',
                    'toMany': False,
                    'type': 'number'
                }
            },
            'sortedFields': [
                'count',
                'is_null',
                'length'
            ]
        }
    },
    'baseUrl': '/data_browser/',
    'canMakePublic': False,
    'defaultRowLimit': 1000,
    'sentryDsn': None,
    'sortedModels': [
    ],
    'types': {
        'boolean': {
            'defaultLookup': 'equals',
            'defaultValue': True,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'boolean'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'boolean'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'booleanarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'boolean'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'booleanarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'boolean'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'booleanarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'date': {
            'defaultLookup': 'equals',
            'defaultValue': 'today',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'date'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'date'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'date'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'date'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'date'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'date'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'date'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'datetime': {
            'defaultLookup': 'equals',
            'defaultValue': 'now',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetime'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'datetime'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'datetime'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'datetime'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetime'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'datetimearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'datetime'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'datetimearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'datetime'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'datetimearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'duration': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'duration'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'duration'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'duration'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'duration'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'duration'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'durationarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'duration'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'durationarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'duration'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'durationarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'html': {
            'defaultLookup': 'is_null',
            'defaultValue': '',
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'isnull': {
            'defaultLookup': 'equals',
            'defaultValue': 'IsNull',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'equals'
            ]
        },
        'json': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'json'
                },
                'field_equals': {
                    'prettyName': 'field equals',
                    'type': 'jsonfield'
                },
                'has_key': {
                    'prettyName': 'has key',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'json'
                },
                'not_field_equals': {
                    'prettyName': 'not field equals',
                    'type': 'jsonfield'
                },
                'not_has_key': {
                    'prettyName': 'not has key',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'has_key',
                'field_equals',
                'not_equals',
                'not_has_key',
                'not_field_equals',
                'is_null'
            ]
        },
        'jsonfield': {
            'defaultLookup': 'equals',
            'defaultValue': '|',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'jsonfield'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'jsonfield'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'number': {
            'defaultLookup': 'equals',
            'defaultValue': 0,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'number'
                },
                'gt': {
                    'prettyName': '>',
                    'type': 'number'
                },
                'gte': {
                    'prettyName': '>=',
                    'type': 'number'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'lt': {
                    'prettyName': '<',
                    'type': 'number'
                },
                'lte': {
                    'prettyName': '<=',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'gt',
                'gte',
                'lt',
                'lte',
                'is_null'
            ]
        },
        'numberarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'number'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'number'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'numberchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'numberchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'numberchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'numberchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'numberchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'numberchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'regex': {
            'defaultLookup': 'equals',
            'defaultValue': '.*',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'regex'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'regex'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'string': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'string'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'string'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'string'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'string'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'stringable': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringable'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringable'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringablearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringable'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringablearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringable'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringablearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'string'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'string'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'stringchoice': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoice'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoice'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'stringchoicearray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'stringchoice'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'stringchoicearray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'stringchoice'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'stringchoicearray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'unknown': {
            'defaultLookup': 'is_null',
            'defaultValue': None,
            'lookups': {
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                }
            },
            'sortedLookups': [
                'is_null'
            ]
        },
        'url': {
            'defaultLookup': 'equals',
            'defaultValue': '',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'ends_with': {
                    'prettyName': 'ends with',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'url'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_ends_with': {
                    'prettyName': 'not ends with',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'url'
                },
                'not_regex': {
                    'prettyName': 'not regex',
                    'type': 'regex'
                },
                'not_starts_with': {
                    'prettyName': 'not starts with',
                    'type': 'url'
                },
                'regex': {
                    'prettyName': 'regex',
                    'type': 'regex'
                },
                'starts_with': {
                    'prettyName': 'starts with',
                    'type': 'url'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'starts_with',
                'ends_with',
                'regex',
                'not_equals',
                'not_contains',
                'not_starts_with',
                'not_ends_with',
                'not_regex',
                'is_null'
            ]
        },
        'urlarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'url'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'urlarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'url'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'urlarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        },
        'uuid': {
            'defaultLookup': 'equals',
            'defaultValue': None,
            'lookups': {
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuid'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuid'
                }
            },
            'sortedLookups': [
                'equals',
                'not_equals',
                'is_null'
            ]
        },
        'uuidarray': {
            'defaultLookup': 'equals',
            'defaultValue': '[]',
            'lookups': {
                'contains': {
                    'prettyName': 'contains',
                    'type': 'uuid'
                },
                'equals': {
                    'prettyName': 'equals',
                    'type': 'uuidarray'
                },
                'is_null': {
                    'prettyName': 'is null',
                    'type': 'isnull'
                },
                'length': {
                    'prettyName': 'length',
                    'type': 'number'
                },
                'not_contains': {
                    'prettyName': 'not contains',
                    'type': 'uuid'
                },
                'not_equals': {
                    'prettyName': 'not equals',
                    'type': 'uuidarray'
                },
                'not_length': {
                    'prettyName': 'not length',
                    'type': 'number'
                }
            },
            'sortedLookups': [
                'equals',
                'contains',
                'length',
                'not_equals',
                'not_contains',
                'not_length',
                'is_null'
            ]
        }
    }
}

snapshots['test_query_is_null_date_filter data'] = {
    'body': [
        [
            {
            },
            {
            },
            {
            }
        ]
    ],
    'cols': [
        {
        }
    ],
    'fields': [
        {
            'pathStr': 'name',
            'pivoted': False,
            'priority': 0,
            'sort': 'asc'
        }
    ],
    'filterErrors': [
        None
    ],
    'filters': [
        {
            'lookup': 'is_null',
            'pathStr': 'created_time',
            'value': 'NotNull'
        }
    ],
    'formatHints': {
        'name': {
        }
    },
    'length': 3,
    'limit': 1000,
    'model': 'core.Product',
    'parsedFilterValues': [
        'NotNull'
    ],
    'rows': [
        {
            'name': 'a'
        },
        {
            'name': 'b'
        },
        {
            'name': 'c'
        }
    ]
}

snapshots['test_query_json data'] = {
    'body': [
        [
            {
            },
            {
            }
        ]
    ],
    'cols': [
        {
        }
    ],
    'fields': [
        {
            'pathStr': 'size',
            'pivoted': False,
            'priority': 0,
            'sort': 'dsc'
        },
        {
            'pathStr': 'name',
            'pivoted': False,
            'priority': 1,
            'sort': 'asc'
        },
        {
            'pathStr': 'size_unit',
            'pivoted': False,
            'priority': None,
            'sort': None
        }
    ],
    'filterErrors': [
        None,
        None
    ],
    'filters': [
        {
            'lookup': 'lt',
            'pathStr': 'size',
            'value': '2'
        },
        {
            'lookup': 'gt',
            'pathStr': 'id',
            'value': '0'
        }
    ],
    'formatHints': {
        'name': {
        },
        'size': {
            'highCutOff': 10000000000.0,
            'lowCutOff': 0.0001,
            'maximumFractionDigits': 0,
            'minimumFractionDigits': 0,
            'significantFigures': 3
        },
        'size_unit': {
        }
    },
    'length': 2,
    'limit': 1000,
    'model': 'core.Product',
    'parsedFilterValues': [
        2.0,
        0.0
    ],
    'rows': [
        {
            'name': 'a',
            'size': 1.0,
            'size_unit': 'g'
        },
        {
            'name': 'b',
            'size': 1.0,
            'size_unit': 'g'
        }
    ]
}

snapshots['test_query_json_pivot data'] = {
    'body': [
        [
            {
                'id__count': 1.0,
                'size__max': 1.0
            },
            {
                'id__count': 3.0,
                'size__max': 6.0
            }
        ],
        [
            {
                'id__count': 2.0,
                'size__max': 3.0
            },
            None
        ]
    ],
    'cols': [
        {
            'created_time__month': 'January'
        },
        {
            'created_time__month': 'February'
        }
    ],
    'fields': [
        {
            'pathStr': 'created_time__year',
            'pivoted': False,
            'priority': 0,
            'sort': 'asc'
        },
        {
            'pathStr': 'created_time__month',
            'pivoted': True,
            'priority': 1,
            'sort': 'asc'
        },
        {
            'pathStr': 'id__count',
            'pivoted': False,
            'priority': None,
            'sort': None
        },
        {
            'pathStr': 'size__max',
            'pivoted': False,
            'priority': None,
            'sort': None
        }
    ],
    'filterErrors': [
    ],
    'filters': [
    ],
    'formatHints': {
        'created_time__month': {
        },
        'created_time__year': {
            'highCutOff': 10000000000.0,
            'lowCutOff': 0.0001,
            'maximumFractionDigits': 0,
            'minimumFractionDigits': 0,
            'significantFigures': 3,
            'useGrouping': False
        },
        'id__count': {
            'highCutOff': 10000000000.0,
            'lowCutOff': 0.0001,
            'maximumFractionDigits': 0,
            'minimumFractionDigits': 0,
            'significantFigures': 3
        },
        'size__max': {
            'highCutOff': 10000000000.0,
            'lowCutOff': 0.0001,
            'maximumFractionDigits': 0,
            'minimumFractionDigits': 0,
            'significantFigures': 3
        }
    },
    'length': 3,
    'limit': 1000,
    'model': 'core.Product',
    'parsedFilterValues': [
    ],
    'rows': [
        {
            'created_time__year': 2020.0
        },
        {
            'created_time__year': 2021.0
        }
    ]
}

snapshots['test_query_qs_variants content'] = [
    '# This is an approximation of the main queryset.',
    '# Pages with pivoted or calculated data may do additional queries.',
    '',
    'tests.core.admin.ProductAdmin(model, admin_site).get_queryset(request).annotate(',
    '    ddb_size_is_null=ExpressionWrapper(',
    '        Q(size=None),',
    '        output_field=BooleanField(),',
    '    ),',
    ').annotate(',
    '    ddb_annotated=Subquery(',
    '        tests.core.admin.ProductAdmin(model, admin_site).get_queryset(request).filter(',
    '            pk=OuterRef(',
    "                'pk',",
    '            ),',
    '        ).values(',
    "            'annotated',",
    '        )[: 1],',
    '        output_field=TextField(),',
    '    ),',
    ').values(',
    "    'ddb_size_is_null',",
    "    'ddb_annotated',",
    ').distinct().annotate(',
    "    ddb_size_count=Count(F('size'), distinct=True),",
    ').order_by(',
    "    'ddb_annotated',",
    "    'ddb_size_count',",
    "    'ddb_size_is_null',",
    ')[: 1000]'
]

snapshots['test_query_query query'] = {
    'fields': [
        {
            'pathStr': 'size',
            'pivoted': False,
            'priority': 0,
            'sort': 'dsc'
        },
        {
            'pathStr': 'name',
            'pivoted': False,
            'priority': 1,
            'sort': 'asc'
        },
        {
            'pathStr': 'size_unit',
            'pivoted': False,
            'priority': None,
            'sort': None
        }
    ],
    'filterErrors': [
        None,
        None
    ],
    'filters': [
        {
            'lookup': 'lt',
            'pathStr': 'size',
            'value': '2'
        },
        {
            'lookup': 'gt',
            'pathStr': 'id',
            'value': '0'
        }
    ],
    'limit': 1000,
    'model': 'core.Product',
    'parsedFilterValues': [
        2.0,
        0.0
    ]
}
