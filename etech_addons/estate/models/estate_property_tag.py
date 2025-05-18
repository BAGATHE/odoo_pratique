from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name'

    name = fields.Char(string='Property Tag', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('check_tag_name','UNIQUE(name)','le tag est deja attribué choississez un autre')
    ]