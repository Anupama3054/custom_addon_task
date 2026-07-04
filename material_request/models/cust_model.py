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
    po_id=fields.One2many('purchase.order','material_id',string='Purchase Order')
    po_count=fields.Integer(string="Purchase Order Count",compute="_compute_po_count")
    transfer_id=fields.One2many("stock.picking","internal_id",string="Internal Transfer")
    internal_transfers_count=fields.Integer(string="Internal Transfer Count",compute="_compute_internal_transfers_count")


    @api.depends('line_ids')
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

        if not self.env.user.has_group(
                'property_management.group_property_head') and self.status == 'Confirmed':
            po=[]
            for record in self:
                if record.line_ids.prod_source=='Purchase Order':
                    for rec in record.line_ids:
                        po.append((0,0,{
                            'name':rec.product_id.name,
                            'product_qty':rec.product_qty,
                            'price_unit':rec.price_unit,
                        }))
                    purchase=self.env['purchase.order'].create({
                        'partner_id':rec.vendor_id.id,
                        'material_id':self.id,
                        'order_line':po,
                    })
            return{
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'res_id': purchase.id,
                'view_mode': 'form',
                'target': 'current'
            }

    def action_submit(self):
        self.status = "To Approve by Manager"

    def action_reject(self):
        if self.status=="To Approve by Manager":
            raise UserError("You can only perform this operation after manager approval!")
        else:
            self.status = "Rejected"

    def _compute_po_count(self):
        for record in self:
            po_count = len(record.po_id)
            record.po_count = po_count

    def action_open_po(self):
        return{
            "name": "PO",
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "purchase.order",
            "domain": [("material_id", "=", self.po_id)]
        }

    def _compute_internal_transfers_count(self):
        for record in self:
            internal_transfers_count=len(record.transfer_id)
            record.internal_transfers_count=internal_transfers_count


    def action_open_internal_transfers(self):
        pass


