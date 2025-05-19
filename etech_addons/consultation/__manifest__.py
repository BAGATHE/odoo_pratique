# -*- coding: utf-8 -*-
{
    'name': "consultation",

    'summary': "Consultation chez le médecin",

    'description': """
     Le but est de créer un module qui gère la consultation chez le médecin. Un
     client consulte un médecin à une date et se voit attribuer des médicaments.
     Les médicaments coûtent un certain prix et peuvent être délivrer en une
     certaine quantité
    """,
    'license': 'LGPL-3',
    'author': "LOLO",
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
         'views/medecin_view.xml',
         'views/client_view.xml' ,
         'views/medicament_view.xml' ,
         'views/consultation_menus.xml',
    ],
    'application': True,
    'installable': True,
}

