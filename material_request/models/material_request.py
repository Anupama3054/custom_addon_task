# -*- coding: utf-8 -*-
from addons.web.controllers import domain
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
                                   default='Purchase Order',
                                   string="Requisition Action")
    location_id = fields.Many2one('stock.location', string='Source Location')
    location_dest_id = fields.Many2one('stock.location',
                                       string='Destination Location')
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    stock_location_ids = fields.Many2many('stock.location',
                                          compute='_compute_stock_locations')

    @api.onchange('product_id')
    def onchange_product_id(self):
        """To autofill the price in the product in the product line and filter
        locations based on stock"""
        self.price_unit = self.product_id.list_price

    @api.depends('product_id', 'product_qty')
    def _compute_stock_locations(self):
        """This is for computing the available locations in the location_id
        field based on the product stock."""
        for record in self:
            if record.product_id:
                stock = self.env['stock.quant'].search([
                    ('product_id', '=', record.product_id.id),
                    ('quantity', '>', record.product_qty),
                ])
                record.stock_location_ids = stock.mapped('location_id')
            else:
                record.stock_location_ids = False
