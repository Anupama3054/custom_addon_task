# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrder(models.Model):
    """To inherit purchase.order and add required fields"""
    _inherit = "purchase.order"

    material_id = fields.Many2one('material.req.ref', string='material_id')

