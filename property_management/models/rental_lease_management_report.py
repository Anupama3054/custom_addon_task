# -*- coding: utf-8 -*-
from odoo import fields, models

class RentorLeaseManagementReport(models.TransientModel):
    """This is model designed for providing the report wizard for rent/lease record.
    Initially the name and description of the model is provided followed by the
     fields"""
    _name = 'rental.lease.management.report'
    _description = 'Rental or Lease Management Report'

    property_id=fields.Many2one('property.management',string="Property")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    state = fields.Selection(
        [("Draft", "Draft"), ("To Approve", "To Approve"),
         ("Confirmed", "Confirmed"), ("Closed", "Closed"),
         ("Returned", "Returned"), ("Expired", "Expired")], default="Draft",
        tracking=True,string="State")
    tenant_id = fields.Many2one('res.partner',string="Tenant")
    owner_id = fields.Many2one('res.partner',string="Owner")
    amount=fields.Float(string="Rent/Lease Amount")
    type = fields.Selection([("Rent", "Rent"), ("Lease", "Lease")],
                            default="Rent",string="Type")

    def action_create_pdf_report(self):
        query="""select rr.property_id as Property """