# -*- coding: utf-8 -*-

from odoo import api,models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    """This class is used for inheriting the purchase.order model and adding the
    required fields to it."""
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super().button_confirm()
        for record in self:
            last_ref_date = record.partner_id.last_reference_date.date()
            today = record.date_order.date()
            diff = (today - last_ref_date).days
            if diff > 90:
                raise ValidationError(
                    "PO confirmed from this vendor before 90 days")
            record.partner_id.last_reference_date = today
        return res


    @api.onchange('partner_id')
    def partner_credit(self):
        """ Checks if the selected vendor has any existing credit balances
        and triggers a warning"""
        if self.partner_id.credit > 0:
            return {
                'warning': {
                    'title':"Credit Warning",
                    'message':f"This vendor has a credit of {self.partner_id.credit}."
                }
            }





































