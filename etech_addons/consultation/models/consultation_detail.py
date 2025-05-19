from odoo import fields, models,api

class ConsultationDetail(models.Model):
    _name = 'consultation.consultation.detail'
    _description = 'Consultation Detail'

    consultation_id = fields.Many2one('consultation.consultation', string="Consultation", required=True)
    medicament_id = fields.Many2one('consultation.medicament',string="Medicament",required=True)
    quantite = fields.Integer(string="Quantite",required=True,default=1)
    price = fields.Float(string="Prix du medicament",required=True,default=0)
    _sql_constraints = [
        ('check_quantite_medicament','CHECK(quantite > 0)','le quantite ne peut pas etre inferieur a 1'),
        ('check_price','CHECK(price >= 0)','le prix ne peut pas etre inferieur a 0')
    ]