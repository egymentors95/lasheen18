# -*- coding: utf-8 -*-
# (C) 2025 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com

{
    'name': 'Multiple Manufacturing Orders',
    'sequence': 0,
    'version': '18.0',
    'summary': """App made by elmekkaoui.brahim@gmail.com""",
    'author': 'EL MEKKAOUI BRAHIM',
    'license': 'LGPL-3',
    'category': '',
    'description': """"App made by by elmekkaoui.brahim@gmail.com""",
    'website': "elmekkaoui.brahim@gmail.com",
    'images': [],
    'depends': [
        'mrp',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'views/views_multiple_manufacturing_orders.xml',

        # Views
        'data/ir_sequence.xml',
        # 'views/views_sale_order.xml',
        # 'views/views_stock_picking.xml',
        # 'views/views_purchase_order.xml',
        # 'views/views_account_move.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'pre_init_hook':  "pre_init_check",
}
