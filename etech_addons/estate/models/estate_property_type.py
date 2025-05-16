from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string='Property Type', required=True)
    estate_property_ids = fields.One2many('estate.property','property_type_id',string='Estate Property')