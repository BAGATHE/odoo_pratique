from odoo import fields, models

class Medecin(models.Model):
    _name = 'consultation.medecin'
    _description = 'Medecin'

    name = fields.Char('Nom du Medecin',required=True)
    debut_service = fields.Date("debut service",required=True)
    user_id = fields.Many2one('res.users',string="User")
    user_login = fields.Char(related='user_id.login', string="User Login", store=False)
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('check_unique_user','UNIQUE(user_id)','Chaque utilisateur ne peut être associé qu’à un seul médecin.')
    ]