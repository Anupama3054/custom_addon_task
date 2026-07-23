# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResUsers(models.Model):
    """This class is used for inheriting the res.users model and adding the
    required fields to it."""
    _inherit = 'res.users'

    hidden_menu_ids=fields.Many2many('ir.ui.menu',String="Hidden Menus")