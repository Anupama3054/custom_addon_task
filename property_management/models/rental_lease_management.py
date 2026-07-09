# -*- coding: utf-8 -*-
from operator import inv

from dateutil.utils import today
from docutils.nodes import target
from openpyxl.cell import read_only

from odoo import fields, models, api,Command
from datetime import timedelta
from odoo.exceptions import UserError

from odoo.orm.fields_temporal import Date, Datetime


class RentorLeaseManagement(models.Model):
    """This is model designed for providing the property for rent/lease.
    Initially the name and description of the model is provided followed by the
     fields"""
    _name = 'rental.lease.management'
    _description = 'Rental or Lease Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "rent_lease_id"

    property = fields.Many2many('property.management', string="Property",
                                ondelete='cascade')
    type = fields.Selection([("Rent", "Rent"), ("Lease", "Lease")],
                            default="Rent")
    tenant_id = fields.Many2one('res.partner', string='Tenant', required=True)
    amount = fields.Float(string="Rent/Lease Amount")
    start_date = fields.Date(String="from")
    end_date = fields.Date(String="to")
    due_date = fields.Date(string="due", compute="_compute_due_date")
    number_of_days = fields.Integer(string="Number of days",
                                    compute="_compute_number_of_days",
                                    store=True)
    status = fields.Selection(
        [("Draft", "Draft"), ("To Approve", "To Approve"),
         ("Confirmed", "Confirmed"), ("Closed", "Closed"),
         ("Returned", "Returned"), ("Expired", "Expired")], default="Draft",
        tracking=True)
    rent_lease_id = fields.Char(string="Rental Lease Id", required=True,
                                copy=False, readonly=True,
                                default=lambda self: 'New', ondelete="cascade")
    total_amount = fields.Float(related="property.legal_amount",
                                string='Total Amount', readonly=False)
    company = fields.Many2one('res.company', string="Company",
                              default=lambda self: self.env.user.company_id.id)
    document_id = fields.Many2one('ir.attachment',
                                  string="Related Attachments", required=True)
    invoice_id = fields.One2many('account.move', 'lease_id', string="Invoices")
    invoice_count = fields.Integer(string="Invoice Count",
                                   compute='_compute_invoice_count')
    is_paid = fields.Boolean(string="Paid", compute="_compute_is_paid")

    @api.model_create_multi
    def create(self, vals_list):
        """This function is for creating automatic sequence for each rent/lease
        record"""
        for vals in vals_list:
            if vals.get('rent_lease_id', 'New') == 'New':
                vals['rent_lease_id'] = self.env['ir.sequence'].next_by_code(
                    'rent_lease_seq') or 'New'
        return super(RentorLeaseManagement, self).create(vals_list)

    @api.depends('start_date', 'end_date')
    def _compute_number_of_days(self):
        """This function is used to automatically compute the number of days we
        want to get the property for rent/lease.The number of days will be
        calculated from the start date and end date of the rent lease."""
        for record in self:
            if record.start_date and record.end_date:
                total = record.end_date - record.start_date
                record.number_of_days = total.days
            else:
                record.number_of_days = 0


    def draft(self):
        """To set the state to draft while clicking the draft button"""
        self.status = 'Draft'
        template = self.env.ref('property_management.email_template')
        email_values = {'email_to': self.tenant_id.email}
        template.with_context(context={'status': 'Draft'}).send_mail(self.id,
                                                                     force_send=True,
                                                                     email_values=email_values)


    def confirm(self):
        """To set the state to confirmed while clicking the confirm button"""
        if self.env.user.has_group('property_management.group_property_manager'):
            self.status = 'Confirmed'
            template = self.env.ref('property_management.email_template')
            email_values = {'email_to': self.tenant_id.email}
            template.with_context(context={'status': 'Confirmed'}).send_mail(
                self.id, force_send=True, email_values=email_values)
        else:
            self.status = 'To Approve'
            template = self.env.ref('property_management.email_template')
            email_values = {'email_to': self.tenant_id.email}
            template.with_context(context={'status': 'To Approve'}).send_mail(
                self.id, force_send=True, email_values=email_values)


    def approve(self):
        """This function is for allowing the manager to approve the rent/lease
        records"""
        self.status = 'Confirmed'


    def close(self):
        """To set the state to closed while clicking the close button"""
        self.status = 'Closed'
        template = self.env.ref('property_management.email_template')
        email_values = {'email_to': self.tenant_id.email}
        template.with_context(context={'status': 'Closed'}).send_mail(
            self.id,
            force_send=True,
            email_values=email_values)


    def returned(self):
        """To set the state to returned while clicking the return button"""
        self.status = 'Returned'
        template = self.env.ref('property_management.email_template')
        email_values = {'email_to': self.tenant_id.email}
        template.with_context(context={'status': 'Returned'}).send_mail(self.id,
                                                                            force_send=True,
                                                                            email_values=email_values)


    def expired(self):
        """To set the state to expired while clicking the expire button"""
        self.status = 'Expired'
        template = self.env.ref('property_management.email_template')
        email_values = {'email_to': self.tenant_id.email}
        template.with_context(context={'status': 'Expired'}).send_mail(self.id,
                                                                       force_send=True,
                                                                       email_values=email_values)


    def action_open_invoice_wizard(self):
        """This function is for opening the invoice form when the create invoice
        button is clicked."""
        if not self.env.user.has_group(
                'property_management.group_property_manager') and self.status == 'To Approve':
            raise UserError("Get the record approved by manager to do this action")
        else:
            invoice_line = []
            for record in self:
                for rec in record.property:
                    invoice_line.append(
                        Command.create({
                            'name': rec.property_ref_id,
                            'quantity': 1,
                            'price_unit': record.amount,
                        })
                    )
                draft_invoice = self.env['account.move'].search([
                    ('move_type', '=', 'out_invoice'),
                    ('lease_id', '=', self.id),
                    ('state', '=', 'draft')
                ])
                if draft_invoice:
                    draft_invoice.invoice_line_ids.unlink()
                    for rec in record.property:
                        draft_invoice.write({
                            'partner_id': self.tenant_id.id,
                            'invoice_line_ids': [
                                Command.create({
                                'name': rec.property_ref_id,
                                'quantity': 1,
                                'price_unit': record.amount,
                            })]
                        })
                        invoice = draft_invoice
                else:

                    invoice = self.env['account.move'].create({
                        'move_type': 'out_invoice',
                        'lease_id': self.id,
                        'partner_id': self[0].tenant_id.id,
                        'invoice_line_ids': invoice_line
                    })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Customer Invoice Wizard',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'target': 'current'
            }


    def action_open_invoices(self):
        """This function is for opening the related invoices of a rent/lease form
         when the invoice smart button is clicked.if there is any draft invoice
         while creating invoice again,then the draft invoice will be unlinked
         from the records."""

        return {
            "name": "Invoice",
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "account.move",
            "domain": [("lease_id", "=", self.rent_lease_id)]

        }


    @api.depends('invoice_id')
    def _compute_invoice_count(self):
        """This function is for computing the number of rent or lease records
        for each property"""
        for record in self:
            invoice_count = len(record.invoice_id)
            record.invoice_count = invoice_count


    @api.depends('invoice_id.payment_state')
    def _compute_is_paid(self):
        """This function is for computing whether the invoice is paid or not for
        creating a ribbon in related rent/lease record."""
        for record in self:
            record.is_paid = any(
                inv.state == "posted" and inv.payment_state == "paid" for inv in
                record.invoice_id)


    @api.depends('end_date', 'status')
    def _compute_due_date(self):
        """This function is for automatically calculating the due_date field by
        using the end_date field.If the due_date is after the current date,the
        record will automatically move to expired state."""
        for record in self:
            if record.end_date:
                record.due_date = record.end_date + timedelta(days=2)
                if record.due_date < Date.today():
                    self.status = 'Expired'
                else:
                    pass
            else:
                record.due_date = False
