# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MaterialRequest(models.Model):
    """This class is for giving the fields to be added in the product line in
    model material.req.ref"""
    _name = "material.request"
    _description = "Material Request"

    order_id = fields.Many2one('material.req.ref', string='Order Reference')
    product_id = fields.Many2one('product.product', string='Product')
    prod_source = fields.Selection([('Purchase Order', 'Purchase Order'),
                                    ('Internal Transfer', 'Internal Transfer')],
                                   default='Purchase Order',string="Requisition Action")
    location_id=fields.Many2one('stock.location', string='Source Location')
    location_dest_id=fields.Many2one('stock.location', string='Destination Location')
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')


    @api.onchange('product_id')
    def onchange_product_id(self):
        """To map the vendors in the product to the product line"""
        self.price_unit = self.product_id.list_price



