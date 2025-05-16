from odoo import fields, models
from odoo.fields import Selection


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float('Price', digits=(16, 2),default=0)
    state = fields.Selection(string="State",copy=False,selection=[('accepted','Accepted'),('rejected','Rejected')])
    partner_id = fields.Many2one('res.partner', string="Partner",required=True)
    property_id = fields.Many2one('estate.property', string="Property",required=True)

