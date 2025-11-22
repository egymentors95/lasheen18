# -*- coding: utf-8 -*-
# (C) 2025 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com

{
    'name': 'Cheapest Product',
    'sequence': 100,
    'version': '18.0',
    'summary': """App made by elmekkaoui.brahim@gmail.com""",
    'author': 'EL MEKKAOUI BRAHIM',
    'license': 'LGPL-3',
    'category': '',
    'description': """"App made by by elmekkaoui.brahim@gmail.com""",
    'website': "elmekkaoui.brahim@gmail.com",
    'images': [],
    'depends': [
        'pos_loyalty',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cheapest_product/static/src/js/overrides/models/pos_order.js',
        ]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'pre_init_hook':  "pre_init_check",
}
