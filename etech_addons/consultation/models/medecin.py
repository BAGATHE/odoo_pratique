from odoo import fields, models,api
from datetime import date


class Medecin(models.Model):
    _name = 'consultation.medecin'
    _description = 'Medecin'

    name = fields.Char('Nom du Medecin',required=True)
    debut_service = fields.Date("debut service",required=True)
    user_id = fields.Many2one('res.users',string="User")
    user_login = fields.Char(related='user_id.login', string="User Login", store=False)
    active = fields.Boolean('Active', default=False)
    consultation_ids = fields.One2many('consultation.consultation','medecin_id','consultations')
    experience = fields.Char(compute='_compute_experience',string='Experience',store=False,default='non defini')
    nb_consultation_du_jour = fields.Integer(compute="_compute_consultation_du_jour", string="Nombre consultation du jour",store=False, readonly=True)
    _sql_constraints = [
        ('check_unique_user','UNIQUE(user_id)','Chaque utilisateur ne peut être associé qu’à un seul médecin.')
    ]

    @api.depends('debut_service')
    def _compute_experience(self):
        for medecin in self:
            if medecin.debut_service:
                medecin.experience = date.today() - medecin.debut_service

    api.depends('consultation_ids')
    def _compute_consultation_du_jour(self):
        nb_consultation = 0;
        for medecin in self:
            if medecin:
                consultations = medecin.consultation_ids
                for consultation in consultations:
                    if consultation:
                        if consultation.date_debut_consultation.date() == date.today():
                            nb_consultation += 1
                self.nb_consultation_du_jour = nb_consultation

    def consultation_du_jour(self):
        print("tzqtttqztyqtzeyutqzeytqztdqiysfquyfpoqfiuyfp make money again again and again Do it")
