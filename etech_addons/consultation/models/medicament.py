from odoo import fields,models,api

class Medicament(models.Model):
    _name = "consultation.medicament"
    _description = "Consultation Medicament"

    name = fields.Char('nom medicament',required=True)
    dosage = fields.Char("Dosage",required=True)

