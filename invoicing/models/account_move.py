# -*- coding: utf-8 -*-
from odoo import fields, models,api,Command

class AccountMove(models.Model):
    _inherit = "account.move"

    transfer_id=fields.Many2one('stock.picking',string="Transfers")

    @api.depends('transfer_id','invoice_line_ids')
    def action_fill_invoice_line(self):
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








