from odoo import fields, models,api

class Consultation(models.Model):
    _name = 'consultation.consultation'
    _description = 'Consultation'

    date_debut_consultation = fields.Datetime(string="Debut consultation",required=True)
    date_fin_consultation = fields.Datetime(string="fin consultation",required=True)
    client_id = fields.Many2one('consultation.client',string="Patient",required=True)
    medecin_id = fields.Many2one('consultation.medecin',string="Médecin",required=True,index=True,default=lambda self: self.env['consultation.medecin'].search([('user_id', '=', self.env.uid)], limit=1))
    consultation_details_ids = fields.One2many( 'consultation.consultation.detail','consultation_id',string="Détails de la consultation")
    prix_consultation = fields.Float(string="Prix consultation",required=True)
    prix_total_medicament = fields.Float(string="Prix Total Medicament", required=True)
    status = fields.Selection(string="Status",required=True,default='non faites',selection=[
        ('non faites','Non faites'),('',''),('','')
    ])