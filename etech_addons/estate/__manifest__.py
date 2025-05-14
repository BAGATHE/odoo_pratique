{
    'name': 'Estate',
    'summary': 'Pratique creation module estate',
    'description': """Module de formation : gestion immobiliere""",
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'application': True,
    'installable': True,
}
