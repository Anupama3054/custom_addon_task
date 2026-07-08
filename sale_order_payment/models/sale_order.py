# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import Command


class SaleOrder(models.Model):
    """This class is used for inheriting the sale.order model and adding the
    required fields to it."""
    _inherit = 'sale.order'

    def action_register_payment(self):
        for record in self:
            invoice_line = []
            for rec in record.order_line:
                invoice_line.append(
                    Command.create({
                        'product_id': rec.product_id.id,
                        'quantity': rec.product_uom_qty,
                        'price_unit': rec.price_unit,
                        'sale_line_ids': [Command.link(rec.id)],
                        'currency_id': record.currency_id.id,
                    })
                )

            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.partner_id.id,
                'invoice_line_ids': invoice_line,
                'invoice_origin': record.name,
                'currency_id': record.currency_id.id,
            })
            return {
                'name': 'Register Payment',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment.register',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'active_model': 'account.move',
                    'active_ids': invoice.ids,
                    'default_currency_id': record.currency_id.id,
                    'default_payment_type': 'inbound',
                    'default_partner_id': record.partner_id.id,
                    'default_amount': invoice.amount_residual,
                }}


