# -*- coding: utf-8 -*-
{
    'name': "Material Request",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Anupama P",
    'category': "material_request",
    'summary': "Material Request",
    'description': "Material Request",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base', 'mail', 'account', 'purchase','stock'],
    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/material_request.xml",
        "views/material_request_menus.xml",
        "data/material_sequence.xml",
    ]}
