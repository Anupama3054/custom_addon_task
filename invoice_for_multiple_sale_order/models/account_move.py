# -*- coding: utf-8 -*-

from odoo import fields, models, api,Command


class AccountMove(models.Model):
    _inherit = "account.move"

    related_so = fields.Many2many('sale.order', string="Related SO")
    so_ids = fields.Many2many('sale.order',
                              compute="_compute_so")

    @api.depends('partner_id')
    def _compute_so(self):
        for record in self:
            if record.partner_id:
                related1 = self.env['sale.order'].search([
                    ('partner_id', '=', record.partner_id.complete_name),
                    ('invoice_status', '=', 'to invoice')
                ])
                record.so_ids = related1.mapped('related_so')
            else:
                return {
                    'warning': {
                        'title': "Customer not selected",
                        'message': "Please select customer first"
                    }
                }



    @api.onchange('related_so')
    def action_fill_invoice_lines(self):
        invoice_line=[]
        if not self.invoice_line_ids:
            for record in self.related_so.order_line:
                invoice_line.append(
                    Command.create({
                        'id': record.id,
                        'product_id': record.product_id.id,
                        'quantity': record.product_uom_qty,
                        'price_unit': record.price_unit,
                        'price_subtotal': record.price_subtotal,

                    }))
                self.invoice_line_ids = invoice_line
        else:
            for record in self.related_so[-1].order_line:
                invoice_line.append(
                    Command.create({
                        'id': record.id,
                        'product_id': record.product_id.id,
                        'quantity': record.product_uom_qty,
                        'price_unit': record.price_unit,
                        'price_subtotal':record.price_subtotal,

                    }))
                self.invoice_line_ids = invoice_line

