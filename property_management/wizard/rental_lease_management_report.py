# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError
import io
import json
from datetime import datetime, date
from dateutil.rrule import rrule, DAILY
from odoo.tools import date_utils, json_default

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class RentorLeaseManagementReport(models.TransientModel):
    """This is model designed for providing the report wizard for rent/lease record.
    Initially the name and description of the model is provided followed by the
     fields and methods"""
    _name = 'rental.lease.management.report'
    _description = 'Rental or Lease Management Report'

    property_id = fields.Many2one('property.management', string="Property")
    from_date = fields.Date(string="From Date", required="True")
    to_date = fields.Date(string="To Date", required="True")
    state = fields.Selection(
        [("Draft", "Draft"), ("To Approve", "To Approve"),
         ("Confirmed", "Confirmed"), ("Closed", "Closed"),
         ("Returned", "Returned"), ("Expired", "Expired")], default="Draft",
        tracking=True, string="State")
    tenant_id = fields.Many2one('res.partner', string="Tenant")
    owner_id = fields.Many2one('res.partner', string="Owner")
    type = fields.Selection([("Rent", "Rent"), ("Lease", "Lease")],
                            default="Rent", string="Type")

    def action_create_pdf_report(self):
        """This is the action to be performed while clicking the print PDF button
        in the wizard.The records matching the query fetched from the database
        and the reporting action is triggered"""
        if self.to_date and self.from_date:
            if self.from_date > self.to_date:
                raise ValidationError(
                    'You entered start date as a date after end date')

        query = """select pm.property_ref_id as property,rl.start_date as Start_Date,
                rl.end_date as End_Date,rl.status as State,rp1.name as tenant,
                rp2.name as owner,rl.amount as Amount,rl.type as Type from 
                rental_lease_management as rl inner join 
                property_management_rental_lease_management_rel as rel
                on rl.id = rel.rental_lease_management_id inner join
                property_management as pm on pm.id = rel.property_management_id 
                left join res_partner as rp1 on rp1.id = rl.tenant_id
                left join res_partner as rp2 on rp2.id = pm.owner_id"""

        if self.from_date and self.to_date:
            query += """ where rl.start_date ='%s' and rl.end_date='%s'""" % (
                self.from_date, self.to_date)

        if self.property_id:
            query += """ and pm.property_ref_id='%s'""" % self.property_id.display_name

        if self.state:
            query += """ and rl.status='%s'""" % self.state

        if self.tenant_id:
            query += """ and rp1.name='%s'""" % self.tenant_id.name

        if self.owner_id:
            query += """ and rp2.name='%s'""" % self.owner_id.name

        if self.type:
            query += """ and rl.type='%s'""" % self.type

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        if report == []:
            raise ValidationError("No matching datas found!")
        data = {'owner': self.owner_id.name, 'report': report}
        return self.env.ref(
            'property_management.action_report_rentlease').report_action(
            None, data=data)

    def action_create_xlsx_report(self):
        if self.to_date and self.from_date:
            if self.from_date > self.to_date:
                raise ValidationError(
                    'You entered start date as a date after end date')
        data = {
            'property': self.property_id.display_name,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'state': self.state,
            'tenant': self.tenant_id.name,
            'owner': self.owner_id.name,
            'type': self.type,
        }
        print(data)
        if self.from_date and self.to_date:
            return {
                'type': 'ir.actions.report',
                'data': {
                    'model': 'rental.lease.management.report',
                    'options': json.dumps(data, default=json_default),
                    'output_format': 'xlsx',
                    'report_name': 'Rent/Lease Report',
                },
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        query = """select pm.property_ref_id as property,rl.start_date as Start_Date,
                rl.end_date as End_Date,rl.status as State,rp1.name as tenant,
                rp2.name as owner,rl.amount as Amount,rl.type as Type from 
                rental_lease_management as rl inner join 
                property_management_rental_lease_management_rel as rel
                on rl.id = rel.rental_lease_management_id inner join
                property_management as pm on pm.id = rel.property_management_id 
                left join res_partner as rp1 on rp1.id = rl.tenant_id
                left join res_partner as rp2 on rp2.id = pm.owner_id"""

        if data['from_date'] and data['to_date']:
            query += """ where rl.start_date ='%s' and rl.end_date='%s'""" % (
                data['from_date'], data['to_date'])

        if data['property']:
            query += """ and pm.property_ref_id='%s'""" % data['property']

        if data['state']:
            query += """ and rl.status='%s'""" % data['state']

        if data['tenant']:
            query += """ and rp1.name='%s'""" % data['tenant']

        if data['owner']:
            query += """ and rp2.name='%s'""" % data['owner']

        if data['type']:
            query += """ and rl.type='%s'""" % data['type']

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        records={'report': report}
        rec=records['report']
        print(rec)
        if report == []:
            raise ValidationError("No matching datas found!")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('report')
        head = workbook.add_format(
            {'bold': False, 'font_size': 25, 'align': 'center'}
        )
        cells = workbook.add_format(
            {'font_size': '11px', 'align': 'left'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        sheet.merge_range('I3:L5', 'Rent/Lease Report', head)
        sheet.merge_range('B8:C8', 'From Date:', cells)
        sheet.merge_range('D8:E8', data['from_date'], txt)
        sheet.merge_range('B9:C9', 'To Date:', cells)
        sheet.merge_range('D9:E9', data['to_date'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
