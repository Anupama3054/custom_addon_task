# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"

    order_id = fields.Many2one('material.req.ref', string='Order Reference')
    product_id = fields.Many2one('product.template', string='Product')
    prod_source = fields.Selection([('Purchase Order', 'Purchase Order'),
                                    ('Internal Transfer', 'Internal Transfer')],
                                   default='Purchase Order',string="Requisition Action")
    vendor_id=fields.Many2many('res.partner',string='Vendor')
    location_id=fields.Many2one('stock.location', string='Source Location')
    location_dest_id=fields.Many2one('stock.location', string='Destination Location')
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    vendor_id=fields.Many2one('product.supplierinfo', string='Vendor',readonly=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price_unit = self.product_id.list_price

    @api.onchange('prod_source')
    def _onchange_prod_source(self):
        if self.prod_source == 'Internal Transfer':
            self.vendor_id = False

    @api.onchange('product_id')
    def onchange_product_id(self):
        for record in self:
            if record.product_id:
                vendors=record.product_id.seller_ids.mapped('partner_id')
                record.vendor_id=vendors.ids
            else:
                record.vendor_id=False



