# -*- coding: utf-8 -*-
{
    'name': "invoicing",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Anupama P",
    'category': "invoicing",
    'summary': "invoicing",
    'description': "invoicing",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','account','stock','sale','sale_management'],
    'data': [
        'views/account_move.xml',
    ]
}


