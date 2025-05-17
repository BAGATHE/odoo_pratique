from odoo import fields, models,api,_
from odoo.exceptions import ValidationError
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
    total_area = fields.Integer(string='Total Area',compute="_compute_total_area",store=False)
    best_price = fields.Float('Best Price',compute='_compute_best_price',store=False,readonly=True)

    @api.constrains('living_area','garden_area')
    def _check_is_positive_area(self):
        for rec in self:
            if rec.living_area < 0 or rec.garden_area < 0:
                raise ValidationError('Area must be positive')
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            offers_price = record.offer_ids.mapped('price')
            record.best_price = max(offers_price) if offers_price else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

