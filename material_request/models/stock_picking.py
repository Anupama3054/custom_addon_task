# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InternalTransfer(models.Model):
    _inherit = "stock.picking"

    internal_id = fields.Many2one("material.req.ref",string="internal_id")