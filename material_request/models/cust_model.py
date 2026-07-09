# -*- coding: utf-8 -*-
from odoo import models, fields, api,Command
from odoo.exceptions import UserError


class MyCustomModel(models.Model):
    """This class is for creating the form for material request."""
    _name = 'material.req.ref'
    _description = 'Material request reference'
    _rec_name = "material_request_id"

    employee_id = fields.Many2one('res.partner', string="Employee",
                                  required=True)
    status = fields.Selection(
        [("Draft", "Draft"), ("To Approve by Manager", "To Approve by Manager"),
         ("To Approve by Head", "To Approve by Head"), ("Rejected", "Rejected"),
         ("Confirmed", "Confirmed")], default="Draft", tracking=True)

    date = fields.Datetime(string="Date", default=fields.Date.today())
    line_ids = fields.One2many('material.request', 'order_id',
                               string='Order Lines')
    po_id = fields.One2many('purchase.order', 'material_id',
                            string='Purchase Order')
    po_count = fields.Integer(string="Purchase Order Count",
                              compute="_compute_po_count")
    transfer_id = fields.One2many("stock.picking", "internal_id",
                                  string="Internal Transfer")
    internal_transfers_count = fields.Integer(string="Internal Transfer Count",
                                              compute="_compute_internal_transfers_count")
    material_request_id = fields.Char(string="Material request id",
                                      required=True,
                                      copy=False, readonly=True,
                                      default=lambda self: 'New')

    @api.model_create_multi
    def create(self, vals_list):
        """ This function is used to create a sequence for each form.Before saving
        the form,the sequence will be set to 'New' and on saving,the sequence
        will be automatically updated based on the prefix,padding and increment
        we already specified."""
        for vals in vals_list:
            if vals.get('material_request_id', 'New') == 'New':
                vals['material_request_id'] = self.env[
                                                  'ir.sequence'].next_by_code(
                    'request_seq') or 'New'
        return super(MyCustomModel, self).create(vals_list)

    @api.depends('line_ids')
    def action_approve_manager(self):
        """This function is for approving the records. and for creating POs and
        internal transfers while approval."""
        self.status = "To Approve by Head"

    @api.depends('line_ids')
    def action_approve_head(self):
        """This function is for approving the records. and for creating POs and
        internal transfers while approval."""
        self.status = "Confirmed"

        for record in self:
            purchase_lines = record.line_ids.filtered(
                lambda a: a.prod_source == 'Purchase Order')
            internal_lines = record.line_ids.filtered(
                lambda b: b.prod_source == 'Internal Transfer')

            if purchase_lines:
                vendor_list = {}
                for rec in purchase_lines:
                    if rec.product_id:
                        vendors = rec.product_id.seller_ids.mapped(
                            'partner_id')
                        for vendor in vendors:
                            if vendor.id not in vendor_list:
                                vendor_list[vendor.id] = []
                            vendor_list[vendor.id].append (
                                Command.create({
                                    'name': rec.product_id.display_name,
                                    'product_id': rec.product_id.id,
                                    'product_qty': rec.product_qty,
                                    'price_unit': rec.price_unit,
                            }))
                for vendor_id, order_line in vendor_list.items():
                    self.env['purchase.order'].create({
                        'partner_id': vendor_id,
                        'material_id': record.id,
                        'origin': self.id,
                        'order_line': order_line,
                    })

            if internal_lines:
                picking_type = self.env['stock.picking.type'].search([
                    ('code', '=', 'internal')])
                for rec in internal_lines:
                    picking = self.env['stock.picking'].create({
                        'partner_id': record.employee_id.id,
                        'picking_type_id': picking_type.id,
                        'location_id': rec.location_id.id,
                        'location_dest_id': rec.location_dest_id.id,
                        'internal_id': record.id,
                        'origin': self.id,

                    })

                    self.env['stock.move'].create({
                        'product_id': rec.product_id.id,
                        'product_uom_qty': rec.product_qty,
                        'location_final_id': rec.location_dest_id.id,
                        'picking_id': picking.id,

                    })

    def action_submit(self):
        """This function is for changing the status while clicking button"""
        self.status = "To Approve by Manager"

    def action_reject(self):
        """This function is for rejecting the request"""
        self.status = "Rejected"

    def _compute_po_count(self):
        """This function is for computing the count of PO records"""
        for record in self:
            po_count = len(record.po_id)
            record.po_count = po_count

    def action_open_po(self):
        """This function is for opening the PO records"""
        return {
            "name": "PO",
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "purchase.order",
            "domain": [("origin", "=", self.id)]
        }

    def _compute_internal_transfers_count(self):
        """This function is for counting  the number of internal transfers"""
        for record in self:
            internal_transfer_count = len(record.transfer_id)
            record.internal_transfers_count = internal_transfer_count

    def action_open_internal_transfers(self):
        """This function is for opening the internal transfers"""
        return {
            "name": "Internal",
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "stock.picking",
            "domain": [("origin", "=", self.id)]
        }
