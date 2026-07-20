# -*- coding: utf-8 -*-
from odoo import models, api

class RentalLeaseReport(models.AbstractModel):
    """This abstract model is for passing the records to the template efficiently."""
    _name = 'report.property_management.form_rent_lease_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """The records are returned efficiently"""
        print(data)
        return {
            'doc_model': 'rental.lease.management',
            'data': data,
            'report': data['report'],
            'owner':data['owner']
        }
