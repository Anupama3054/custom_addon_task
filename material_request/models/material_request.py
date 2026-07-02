# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"

    order_id = fields.Many2one('material.req.ref', string='Order Reference')
    product_id = fields.Many2one('product.template', string='Product')
    prod_source = fields.Selection([('Purchase Order', 'Purchase Order'),
                                    ('Internal Transfer', 'Internal Transfer')],
                                   default='Purchase Order',string="Source")
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit = self.product_id.list_price
