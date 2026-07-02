# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.orm.fields_temporal import Date


class Move(models.Model):
    """This class is for inheriting the account.move model for invoice
     creation."""
    _inherit = 'account.move'
    property = fields.Many2one('property.management', string='Property')
    lease_id = fields.Many2one('rental.lease.management', string='lease_id')

    def action_post(self):
        """This function is for updating the already existing action_post function
        in account.move."""
        res = super().action_post()

        for record in self:
            if record.move_type == 'out_invoice' and record.lease_id:
                record.lease_id.message_post(body=_("Invoice Posted"))

        return res

    def late_payment_follow_up(self):
        """This function is for searching the invoices that are over_due and not
        paid and send a follow-up email."""
        over_due_invoice = self.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', '=', 'not_paid'),
            ('invoice_date_due', '<', Date.today())
        ])

        if over_due_invoice:
            for record in over_due_invoice:
                template = record.env.ref(
                    'property_management.paylate_email_template')
                template.with_context(
                    to_email=record.lease_id.tenant_id.email).send_mail(
                    record.id, force_send=True)
