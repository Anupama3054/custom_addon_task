# -*- coding: utf-8 -*-
from odoo import fields, models


class Facilities(models.Model):
    """This class is for adding facilities for properties"""
    _name = 'property.facilities'
    _description = 'property facilities'
    _rec_name = 'facilities'

    facilities = fields.Char(string='Facilities')
