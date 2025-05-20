from datetime import datetime,time

from odoo import fields, models,api
from odoo.exceptions import UserError,ValidationError

class Consultation(models.Model):
    _name = 'consultation.consultation'
    _description = 'Consultation'

    NB_LIMITE_CONSULTATION_JOURNALIERE = 3

    date_debut_consultation = fields.Datetime(string="Debut consultation",required=True)
    date_fin_consultation = fields.Datetime(string="fin consultation",required=True)
    client_id = fields.Many2one('consultation.client',string="Patient",required=True)
    medecin_id = fields.Many2one('consultation.medecin',string="Médecin",required=True,index=True,default=lambda self: self.env['consultation.medecin'].search([('user_id', '=', self.env.uid)], limit=1))
    consultation_details_ids = fields.One2many( 'consultation.consultation.detail','consultation_id',string="Détails de la consultation")
    prix_consultation = fields.Float(string="Prix consultation",required=True,default=0)
    prix_total_medicament = fields.Float(compute="_compute_total_medicament", string="Prix total medicament", store=True,readonly=True)
    status = fields.Selection(string="Status",default='non traiter',selection=[
        ('non traiter','Non Traiter'),('en cours','En Cours'),('faite','Faite'),('annulé','Annulé')
    ])



    _sql_constraints = [
        ('check_prix_consultation','CHECK(prix_consultation >= 0)','consultation devrais etre positive'),
        ('check_date','CHECK(date_debut_consultation < date_fin_consultation)','la date fin devrais etre superieur a date debut ')
    ]

    @api.depends("consultation_details_ids")
    def _compute_total_medicament(self):
        for record in self:
            total = 0
            consultation_details = record.consultation_details_ids
            for detail in consultation_details:
                total = total + (detail.prix * detail.quantite)
            record.prix_total_medicament = total

    def in_progress_consultation(self):
        self.ensure_one()
        if self.status == 'annulé':
            raise UserError("cette consultation est deja annulé")
        else:
            self.status = 'en cours'

    def finish_consultation(self):
        self.ensure_one()
        if self.status == 'annulé':
            raise UserError("cette consultation est deja annulé")
        else:
            self.status = 'faite'

    def cancel_consultation(self):
        self.ensure_one()
        if self.status == 'faite':
            raise UserError("la consultation ne peut plus etre annulé")
        else:
            self.status = 'annulé'

    def view_detail(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Details Consultation',
            'res_model': 'consultation.consultation',
            'res_id': self.id,
            'views': [(self.env.ref('consultation.consultation').id, 'form')],
            'target': 'current',
        }

    @api.constrains('date_debut_consultation')
    def check_date_disponibilite(self):
        for consultation in self:
            date = consultation.date_debut_consultation.date()
            debut_date = datetime.combine(date, time.min)
            fin_date = datetime.combine(date, time.max)
            nb_consultation = self.search_count([
                ('date_debut_consultation', '>=', debut_date),
                ('date_debut_consultation', '<=', fin_date),
                ('id', '!=', consultation.id)
            ])
            if nb_consultation >= consultation.NB_LIMITE_CONSULTATION_JOURNALIERE:
                raise ValidationError(f"cette date {date} est deja plein")

    @api.constrains('date_debut_consultation','date_fin_consultation')
    def check_crenaux_horaire(self):
        for consultation in self:
            non_valide_crenaux = self.search([
                ('id', '!=', consultation.id),
                ('date_debut_consultation', '<', consultation.date_fin_consultation),
                ('date_fin_consultation', '>', consultation.date_debut_consultation),
            ])
            if non_valide_crenaux:
                raise ValidationError(f"ce crenaux horaire n'est pas disponible {consultation.date_debut_consultation}-{consultation.date_fin_consultation}")
