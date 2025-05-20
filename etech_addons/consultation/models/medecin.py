from odoo import fields, models,api
from datetime import date


class Medecin(models.Model):
    _name = 'consultation.medecin'
    _description = 'Medecin'

    name = fields.Char('Nom du Medecin',required=True)
    debut_service = fields.Date("debut service",required=True)
    user_id = fields.Many2one('res.users',string="User")
    user_login = fields.Char(related='user_id.login', string="User Login", store=False)
    active = fields.Boolean('Active', default=True)
    consultation_ids = fields.One2many('consultation.consultation','medecin_id','consultations')
    experience = fields.Char(compute='_compute_experience',string='Experience',store=False)

    _sql_constraints = [
        ('check_unique_user','UNIQUE(user_id)','Chaque utilisateur ne peut être associé qu’à un seul médecin.')
    ]

    @api.depends('debut_service')
    def _compute_experience(self):
        for medecin in self:
            if medecin.debut_service:
                medecin.experience = date.today() - medecin.debut_service