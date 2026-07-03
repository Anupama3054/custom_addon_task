# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class MyCustomModel(models.Model):
    _name = 'material.req.ref'
    _description = 'Material request reference'

    employee_id = fields.Many2one('res.partner', string="Employee")
    status = fields.Selection(
        [("Draft", "Draft"), ("To Approve by Manager", "To Approve by Manager"),
         ("To Approve by Head", "To Approve by Head"),("Rejected", "Rejected"),
         ("Confirmed", "Confirmed")], default="Draft", tracking=True)
    date = fields.Datetime(string="Date", default=fields.Date.today())
    line_ids = fields.One2many('material.request', 'order_id',
                               string='Order Lines')

    def action_approve(self):
        if self.status=="Draft":
            raise UserError("Only records in 'To Approve' stage can be approved!")
        elif self.status == "To Approve by Manager" and self.env.user.has_group(
                'material_request.group_requisition_manager'):
            self.status="To Approve by Head"
        elif self.status == "To Approve by Manager" and not self.env.user.has_group(
                'material_request.group_requisition_manager'):
            raise UserError("You can only perform this operation after manager approval!")
        elif self.status=="To Approve by Head" and self.env.user.has_group(
                'material_request.group_requisition_head'):
            self.status="Confirmed"
        else:
            pass

    def action_submit(self):
        self.status = "To Approve by Manager"

    def action_reject(self):
        if self.status=="To Approve by Manager":
            raise UserError("You can only perform this operation after manager approval!")
        else:
            self.status = "Rejected"


