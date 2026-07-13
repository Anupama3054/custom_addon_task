# -*- coding: utf-8 -*-
{
    'name': "Invoice for Multiple Sale Order",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Anupama P",
    'category': "invoice_for_multiple_sale_order",
    'summary': "invoice_for_multiple_sale_order",
    'description': "invoice_for_multiple_sale_order",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','account','stock','sale','sale_management'],
    'data': [
        'views/account_move.xml',
    ]
}