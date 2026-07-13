# -*- coding: utf-8 -*-
from odoo import fields, models,Command

class AccountMove(models.Model):
    """This class inherits account.move and automatically fills the invoice
     lines if transfer is selected and assign button is clicked."""
    _inherit = "account.move"

    transfer_id=fields.Many2one('stock.picking',string="Transfers")

    def action_fill_invoice_line(self):
        """To autofill the invoice line with the order lines in the transfer
        selected while clicking the assign button."""
        invoice_line = []
        self.invoice_line_ids.unlink()
        for record in self.transfer_id.move_ids:
            invoice_line.append(
                Command.create({
                    'id': record.id,
                    'product_id':record.product_id.id,
                    'quantity':record.quantity,
                }))
        self.invoice_line_ids=invoice_line








