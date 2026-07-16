# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class RentorLeaseManagementReport(models.TransientModel):
    """This is model designed for providing the report wizard for rent/lease record.
    Initially the name and description of the model is provided followed by the
     fields"""
    _name = 'rental.lease.management.report'
    _description = 'Rental or Lease Management Report'

    property_id = fields.Many2one('property.management', string="Property")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    state = fields.Selection(
        [("Draft", "Draft"), ("To Approve", "To Approve"),
         ("Confirmed", "Confirmed"), ("Closed", "Closed"),
         ("Returned", "Returned"), ("Expired", "Expired")], default="Draft",
        tracking=True, string="State")
    tenant_id = fields.Many2one('res.partner', string="Tenant")
    owner_id = fields.Many2one('res.partner', string="Owner")
    amount = fields.Float(string="Rent/Lease Amount")
    type = fields.Selection([("Rent", "Rent"), ("Lease", "Lease")],
                            default="Rent", string="Type")

    def action_create_pdf_report(self):
        if self.to_date and self.from_date:
            if self.from_date > self.to_date:
                raise UserError(
                    'You entered start date as a date after end date')

        query = """select pm.property_ref_id as Property,rl.start_date as From,
        rl.end_date as To,rl.status as State,rl.tenant_id as Tenant,
        pm.owner_id as Owner,rl.amount as Amount,rl.type as Type from
         property_management as pm inner join rental_lease_management as rl
         on rl.id=pm.id"""
        if self.from_date and self.to_date:
            query += """where rl.start_date >='%s' and rl.end_date<='%s'%self.from_date,self.to_date"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        data = {'date': self.read()[0], 'report': report}
        return self.env.ref(
            'property_management.action_report_rentlease').report_action(
            None, data=data)


class RentalLeaseReport(models.AbstractModel):
    _name = 'report.property_management.form_rent_lease_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['rental.lease.management'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'rental.lease.management',
            'docs': docs,
            'data': data,
        }
