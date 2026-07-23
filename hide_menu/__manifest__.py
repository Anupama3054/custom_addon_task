# -*- coding: utf-8 -*-
{
    'name': "Hide Menus For Users",
    'version': "19.0.1.0.0",
    'license': "LGPL-3",
    'author': "Anupama P",
    'category': "hide_menus",
    'summary': "hide menus for user",
    'description': "hide_menus",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
    'depends': ['base','account','stock','contacts'],
    'data': [
        'views/res_users.xml',
    ]
}
