# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    """To inherit account.payment.register add transfer name to the memo in
    payment wizard"""
    _inherit = "account.payment.register"

    def _compute_communication(self):
        """To compute the communication field"""
        super()._compute_communication()
        for wizard in self:
            lines = wizard.line_ids
            wizard.communication = '%s,%s' % (wizard._get_communication(lines),
                                              self.line_ids.move_id.transfer_id.name)
