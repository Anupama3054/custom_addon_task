# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PropertyManagement(models.Model):
    """This  class is used to manage the fields for providing the property
    details.Initially the name and description of the model is provided,followed
    by the fields and their types."""
    _name = 'property.management'
    _description = 'property details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'property_ref_id'

    property_ref_id = fields.Char(string='Property', required=True, copy=False,
                                  readonly=True, default=lambda self: 'New')
    status = fields.Selection(
        [("Draft", "Draft"), ("Rented", "Rented"), ("Leased", "Leased"),
         ("Sold", "Sold")], default="Draft", tracking=True)
    address = fields.Text(string="address")
    house_name = fields.Char(string="house_name")
    street = fields.Char(string="street")
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    image = fields.Image(string="Image", max_width=128, max_height=128)
    built_date = fields.Date(string="Built Date")
    can_be_sold = fields.Boolean(string="Can be sold")
    legal_amount = fields.Float(string="Legal Amount")
    rent = fields.Float(string="Rent")
    description = fields.Text(string="Description")
    owner_id = fields.Many2one('res.partner', string='Owner')
    record_count = fields.Integer(string="Record Count",
                                  compute='_compute_record_count')
    facility_name = fields.Many2many("property.facilities",
                                     string="Facilities")
    company_id = fields.Many2one('res.company', string="Company",
                              default=lambda self: self.env.user.company_id.id)
    active=fields.Boolean(string="Active", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """ This function is used to create a sequence for each form.Before saving
        the form,the sequence will be set to 'New' and on saving,the sequence
        will be automatically updated based on the prefix,padding and increment
        we already specified."""
        for vals in vals_list:
            if vals.get('property_ref_id', 'New') == 'New':
                vals['property_ref_id'] = self.env['ir.sequence'].next_by_code(
                    'property_seq') or 'New'
        return super(PropertyManagement, self).create(vals_list)

    def _compute_record_count(self):
        """This function is for computing the number of rent or lease records
        for each property"""
        for record in self:
            record_count = self.env['rental.lease.management'].search_count([
                ('property', '=', record.property_ref_id)])
            record.record_count = record_count

    def action_open_rent_lease_records(self):
        """This function is for defining what action to be performed while
        clicking the smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Records',
            'res_model': 'rental.lease.management',
            'view_mode': 'list,form',
            'domain': [('property', '=', self.property_ref_id)],
            'target': 'current'
        }
