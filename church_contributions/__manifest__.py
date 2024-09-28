{
    'name': 'Church Contributions',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Manage church contributions',
    'description': """
        This module allows churches to manage member contributions.
    """,
    'depends': ['base', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/diocese_views.xml',
        'views/archdeaconry_views.xml',
        'views/parish_views.xml',
        'views/subparish_views.xml',
        'views/member_views.xml',
        'views/menu_views.xml',
        'views/payment_views.xml',
        'views/member_portal_templates.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}