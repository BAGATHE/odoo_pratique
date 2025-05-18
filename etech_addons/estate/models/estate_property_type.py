from odoo import models,fields,api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _order = 'name'

    name = fields.Char(string='Property Type', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    estate_property_ids = fields.One2many('estate.property','property_type_id',string='Estate Property')
    offer_ids = fields.One2many(comodel_name='estate.property.offer',inverse_name='property_id',compute='_compute_offer_ids',string='Offers',store=False)
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')
    def _compute_offer_ids(self):
        for record in self:
            offers = self.env['estate.property.offer'].search([
                ('property_type_id', '=', record.id)
            ])
            record.offer_ids = offers

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
