# -*- coding: utf-8 -*-
{
    'name': "Block_PO",
    'version': "19.0.1.0",
    'license': "LGPL-3",
    'author': "Anupama_P",
    'category': "purchase_order",
    'summary': "Block PO",
    'description': "Block PO",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base', 'mail', 'account','purchase'],
    'data': [
        "views/res_partner.xml",
    ]
}
