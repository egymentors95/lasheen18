# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Product Auto Discount',
    'version': '18.0.0.1.0',
    'category': 'Point of Sale',
    'summary': 'POS Auto Discount on point of sale auto discount on pos product auto discount on point of sales auto discount apply automatic discount on pos discount apply product discount on pos apply product discount on point of sale product discount apply pos discount',
    'description' :"""
        Wants to apply discount automatically on point of sale products?, This odoo app helps user to add discount for products and show discount percentage of product on point of sale screen. When user selects the product then added discount automatically applied to order added discount also printed on point of sale order receipt and order back end view. User also can enable/disable auto discount configuration as per need.
    """,
    'author': 'BROWSEINFO',
    'website': 'https://www.browseinfo.com/demo-request?app=bi_pos_auto_discounts&version=18&edition=Community',
    "price": 10,
    "currency": 'EUR',
    'depends': ['base','point_of_sale'],
    'data': [
        'views/pos_config_view.xml',
        'views/product_discount_view.xml',
        'views/product_template_views.xml',
    ],
    'assets':{
        'point_of_sale._assets_pos': [
            'bi_pos_auto_discounts/static/src/css/product_discount.css',
            'bi_pos_auto_discounts/static/src/js/discount.js',
            'bi_pos_auto_discounts/static/src/xml/product_discount.xml',
        ],
    },
    'license':'OPL-1',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.browseinfo.com/demo-request?app=bi_pos_auto_discounts&version=18&edition=Community',
    "images":['static/description/Banner.gif'],
}
