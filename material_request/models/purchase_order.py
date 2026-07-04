# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    material_id = fields.Many2one('material.req.ref',string='material_id')
