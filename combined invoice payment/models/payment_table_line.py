# -*- coding: utf-8 -*-
from odoo import fields, models, api

class PaymentTableLine(models.Model):
    _name = "payment.table.line"
    _description = "Payment Table Line"

    wizard_id = fields.Many2one('account.payment', string="Wizard")
    invoice_id = fields.Many2one('account.move', string="Invoice")
    amount = fields.Float(string="Amount")
    inv_ids = fields.Many2many('account.move',
                               compute='_compute_inv_ids')

    @api.depends('wizard_id.partner_id', 'wizard_id.amount')
    def _compute_inv_ids(self):
        """To make only the invoices related to the customer visible"""
        self.amount = self.wizard_id.amount
        for record in self:
            if record.wizard_id.partner_id:
                invoices = self.env['account.move'].search([
                    ('partner_id', '=', record.wizard_id.partner_id.id),
                    ('move_type', '=', 'out_invoice'),
                    ('status_in_payment', 'not in',
                     ('draft', 'paid', 'cancel')),
                ])
                record.inv_ids = invoices
            else:
                record.inv_ids = False
