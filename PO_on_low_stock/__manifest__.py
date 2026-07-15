# -*- coding: utf-8 -*-
{
    'name': "Automatic Purchase From Low Stock",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Anupama P",
    'category': "po_on_low_stock",
    'summary': "po_on_low_stock",
    'description': "po_on_low_stock",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['product','base','account','purchase'],
    'data': [
        'views/product_template.xml',
    ]
}