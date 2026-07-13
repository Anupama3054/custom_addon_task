# -*- coding: utf-8 -*-
from odoo import fields, models

class PartnerRecords(models.Model):
    """This class is used for inheriting the res.partner model and adding the
    required fields to it."""
    _inherit = 'res.partner'

    last_reference_date=fields.Datetime(string="Last Reference Date")