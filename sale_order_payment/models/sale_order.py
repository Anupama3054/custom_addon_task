# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo import Command
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """This class is used for inheriting the sale.order model and adding the
    required fields to it."""
    _inherit = 'sale.order'

    paid = fields.Boolean(string="Paid", compute='_compute_paid')

    def _action_confirm(self):
        """To add more actions to be performed while clicking the confirm
        button."""
        super()._action_confirm()

        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'sale.order'),
            ('res_id', '=', self.id),
        ])
        mimetypes = (
            'application/pdf',
            'image/jpeg'
        )
        for record in attachments:
            mime = record.mimetype
            if mime not in mimetypes:
                raise ValidationError("Only pdf and jpeg files are supported")

        if self.message_attachment_count == 0:
            raise ValidationError("Add attachment before confirming!!")

    def action_register_payment(self):
        """To open the payment wizard from the sale order itself and also to
        automatically create the invoice."""
        for record in self:
            invoice_line = []
            for rec in record.order_line:
                invoice_line.append(
                    Command.create({
                        'product_id': rec.product_id.id,
                        'quantity': rec.product_uom_qty,
                        'price_unit': rec.price_unit,
                        'sale_line_ids': [Command.link(rec.id)],
                    })
                )

            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.partner_id.id,
                'invoice_line_ids': invoice_line,
                'invoice_origin': record.name,
                'currency_id': record.currency_id.id,
            })
            invoice.action_post()

            return {
                'name': 'Register Payment',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment.register',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'active_model': 'account.move',
                    'active_ids': invoice.ids,
                }}

    @api.depends('invoice_ids.payment_state', 'invoice_ids.state')
    def _compute_paid(self):
        """To compute if the invoice is paid inorder to make the register
        payment button invisible after payment."""
        for record in self:
            record.paid = False
            for rec in record.invoice_ids:
                if rec.payment_state == 'paid' and rec.state == 'posted':
                    record.paid = True
                else:
                    record.paid = False
