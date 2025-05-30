from odoo import fields, models,api
from datetime import date

class Client(models.Model):
    _name = 'consultation.client'
    _description = 'Consultation Client'

    name = fields.Char('Nom du client', required=True)
    date_naissance = fields.Date('Date de naissance', required=True)
    sexe = fields.Selection(string="Sexe",selection=[('male','Male'),('female','Female')],required=True)
    partner_id = fields.Many2one('res.partner',string="Client")
    partner_phone = fields.Char(related="partner_id.phone",string="Phone")
    age = fields.Integer(compute='_compute_age', string="Age",readonly=True)

    _sql_constraints = [
        ('check_client','UNIQUE(partner_id)','chaque client ne peut etre rattaché a une seule compte particulier ou entreprise')
    ]


    @api.depends('date_naissance')
    def _compute_age(self):
        for client in self:
            if client.date_naissance:
                client.age = date.today().year - client.date_naissance.year
            else :
                client.age = 0
