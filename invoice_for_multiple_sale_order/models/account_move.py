# -*- coding: utf-8 -*-
from odoo import fields, models, api, Command


class AccountMove(models.Model):
    """This class is to inherit account.move model and add required fields"""
    _inherit = "account.move"

    related_so_ids = fields.Many2many('sale.order', string="Related SO")
    allowed_so_ids = fields.Many2many('sale.order', compute="_compute_allowed_so")

    @api.onchange('partner_id')
    def _compute_allowed_so(self):
        """To make only the sale order related to the customer selected in the
        invoice visible in the related_so field"""
        for record in self:
            record.allowed_so_ids = self.env['sale.order'].search([
                ('partner_id', '=', self.partner_id.id),
                ('invoice_status', '=', 'to invoice'),
            ])

    @api.onchange('partner_id')
    def empty(self):
        """To empty the related_co field and the order line values once the
        customer is changed."""
        self.invoice_line_ids = False
        self.related_so_ids = False

    @api.onchange('related_so_ids')
    def action_fill_invoice_lines(self):
        """To fill the invoice lines automatically add the sale order's order
        lines to the invoice lines when the sale order is selected."""
        for record in self:
            if record.related_so_ids:
                invoice_lines = [Command.clear()]
                dict={}
                for rec in record.related_so_ids.order_line:
                    if rec.product_id:
                        if rec.product_id.id in dict:
                            dict[rec.product_id.id]['quantity']+=rec.product_uom_qty
                            dict[rec.product_id.id]['price_unit']=rec.product_id.lst_price
                        else:
                            dict[rec.product_id.id] = {
                                    'product_id': rec.product_id.id,
                                    'quantity': rec.product_uom_qty,
                                    'price_unit': rec.price_unit,
                                }

                for rec in dict.values():
                    print(rec)
                    invoice_lines.append(Command.create(rec))

                record.invoice_line_ids = invoice_lines
            else:

                record.invoice_line_ids = False
