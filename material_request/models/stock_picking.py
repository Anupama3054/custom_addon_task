# -*- coding: utf-8 -*-
from odoo import models, fields

class InternalTransfer(models.Model):
    """To inherit stock.picking and add required fields"""
    _inherit = "stock.picking"

    internal_id = fields.Many2one("material.req.ref",string="internal id")