# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MyCustomModel(models.Model):
    _name = 'material.req.ref'
    _description = 'Material request reference'

    employee_id = fields.Many2one('res.partner', string="Employee")
    date = fields.Datetime(string="Date", default=fields.Date.today())
    line_ids = fields.One2many('material.request', 'order_id',
                               string='Order Lines')
