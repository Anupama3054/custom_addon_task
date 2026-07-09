# -*- coding: utf-8 -*-
{
    'name': "Sale Order Payment",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Anupama P",
    'category': "sale_order",
    'summary': "Register payment from sale order",
    'description': "Register payment from sale order",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','account','sale','sale_management'],
    'data': [
        "views/sale_order.xml",
    ]
}
