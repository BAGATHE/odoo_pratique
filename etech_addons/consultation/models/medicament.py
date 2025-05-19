from odoo import fields,models,api

class Medicament(models.Model):
    _name = "consultation.medicament"
    _description = "Consultation Medicament"

    name = fields.Char('nom medicament',required=True)
    dosage = fields.Char("Dosage",required=True)
    price = fields.Float("Prix de la medicament",required=True,default=0)
    active = fields.Boolean("Active", default=True)


    _sql_constraints = [
        ('check_price','CHECK(price >= 0 )','le prix ne peut pas etre inferieur a 0'),
    ]

