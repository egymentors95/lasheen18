# -*- coding: utf-8 -*-
{
    'name': "Dashboard Real Estate",
    'version': '18.0.1.0.0',
    'description': """ 
        A dashboard for Real Estate management in Odoo.
    """,
    'author': "EgyMentors - Mohamed Elahmady Ali",
    'website': "https://www.egymentors.com/",
    'depends': ['itsys_real_estate', 'web'],
    'data': [ 
        "views/dashboard.xml",
        # "static/src/xml/tst.xml",
    ], 
   'assets': {
        'web.assets_backend': [   
            'https://cdn.jsdelivr.net/npm/chart.js',  
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'mentors_real_estate_dashboard_18/static/src/css/style.css',            
            'mentors_real_estate_dashboard_18/static/src/js/test_dashboard.js',
            'mentors_real_estate_dashboard_18/static/src/xml/tst.xml',
            
        ],
        'web.assets_qweb': [
            # 'mentors_real_estate_dashboard_18/static/src/xml/tst.xml',
        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
    'application': True,
}
