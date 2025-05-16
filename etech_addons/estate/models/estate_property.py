from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'

    name = fields.Char('Property Name', required=True,default="Unknown")
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability',copy=False,default=lambda self: date.today()+relativedelta(months=3))
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float('Selling Price',readonly=True,copy=False)
    bedrooms = fields.Integer('Bedrooms',default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(string='State',required=True,default='new',selection=[('new', 'New'), ('offer received', 'Offer Received'),('offer accepted','Offer Accepted'),('sold', 'Sold'),('cancelled','Cancelled')])
    property_type_id = fields.Many2one('estate.property.type',string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True,
                              default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer",copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer',  'property_id',string='Offers')
