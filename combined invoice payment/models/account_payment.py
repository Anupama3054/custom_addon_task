# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPaymentRegister(models.Model):
    """To inherit the account.payment model and add the required fields"""
    _inherit = "account.payment"

    table_ids = fields.One2many('payment.table.line', 'wizard_id',
                                string="Invoices")


    def action_post(self):
        """To super action_post method and add the required fields """
        res = super().action_post()
        for payment in self:
            for rec in payment.table_ids:
                invoice = rec.invoice_id
                amount_to_reduce = rec.amount

                payment = self.env[
                    'account.payment.register'].with_context(
                    active_model='account.move',
                    active_ids=invoice.ids,
                ).create({
                    'amount': amount_to_reduce
                })
                payment.action_create_payments()

        return res


