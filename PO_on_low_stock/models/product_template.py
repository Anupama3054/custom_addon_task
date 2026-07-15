# -*- coding: utf-8 -*-
from odoo import fields, models, Command


class ProductTemplate(models.Model):
    """This class is to inherit product.template model and add required fields"""
    _inherit = "product.template"

    min_threshold = fields.Float(string="Minimum Threshold")

    def auto_purchase(self):
        """To automatically create purchase order if qty_available goes below
        min_threshold"""
        for record in self:
            if record.min_threshold <= 0 or record.qty_available >= record.min_threshold:
                continue
            vendor_list = {}
            vendors = record.seller_ids.mapped('partner_id')
            if not vendors:
                continue
            for vendor in vendors:
                existing = self.env['purchase.order.line'].search([
                    ('product_id', '=', record.product_variant_id.id),
                    ('order_id.partner_id', '=', vendor.id),
                    ('order_id.state', 'in', ['draft', 'sent', 'to approve'])
                ], limit=1)
                if existing:
                    continue
                vendor_list.setdefault(vendor.id, [])
                vendor_list[vendor.id].append(
                    Command.create({
                        'name': record.display_name,
                        'product_id': record.product_variant_id.id,
                        'product_qty': record.min_threshold - record.qty_available,
                        'price_unit': record.standard_price,
                    })
                )

            for vendor_id, order_lines in vendor_list.items():
                if order_lines:
                    po=self.env['purchase.order'].create({
                        'partner_id': vendor_id,
                        'order_line': order_lines,
                    })
                    po.button_confirm()
