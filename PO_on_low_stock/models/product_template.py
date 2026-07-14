# -*- coding: utf-8 -*-
from odoo import fields, models, Command


class ProductTemplate(models.Model):
    """This class is to inherit product.template model and add required fields"""
    _inherit = "product.template"

    min_threshold = fields.Float(string="Minimum Threshold")

    def auto_purchase(self):
        """To automatically create purchase order if qty_available goes below
        min_threshold"""
        products = self.search([('min_threshold', '>', 0)])
        for record in products:
            vendor_list = {}
            if record.min_threshold > record.qty_available:
                vendors = record.seller_ids.mapped('partner_id')
                if vendors:
                    for vendor in vendors:
                        if vendor.id not in vendor_list:
                            vendor_list[vendor.id] = []
                        vendor_list[vendor.id].append(
                            Command.create({
                                'name': record.display_name,
                                'product_id': record.product_variant_id.id,
                                'product_qty': record.min_threshold - record.qty_available,
                                'price_unit': record.standard_price,
                            }))
            for vendor_id, order_line in vendor_list.items():
                self.env['purchase.order'].create({
                    'partner_id': vendor_id,
                    'order_line': order_line,
                })
