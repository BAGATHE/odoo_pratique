from odoo import fields, models,api,_
from odoo.exceptions import ValidationError,UserError
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare,float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = 'id desc'

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

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)','le prix doit etre stictement superieur a 0'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'le prix de vente doit etre stictement superieur a 0'),
        ('check_name','UNIQUE(name)','le nom est deja attribué a un autre propriete choisissez un autre')
    ]

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

    def sold_estate_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("offre est deja annulé")
            record.state = 'sold'

    def cancel_estate_property(self):
        for record in self:
            record.state = 'cancelled'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            minimum_price = record.expected_price * 0.9
            if float_compare(record.selling_price, minimum_price, precision_digits=2) < 0:
                raise ValidationError("Le prix de vente ne peut pas être inférieur à 90% du prix attendu.")

