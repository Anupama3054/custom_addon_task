# -*- coding: utf-8 -*-

from odoo import fields, models,api

class OwnerRecords(models.Model):
    """This class is used for inheriting the res.partner model and adding the
    required fields to it."""
    _inherit = 'res.partner'

    property=fields.One2many('property.management','owner_id',string='Property')
