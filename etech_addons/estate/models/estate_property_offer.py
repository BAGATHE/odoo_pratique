from odoo import fields, models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float('Price', digits=(16, 2),default=0)
    state = fields.Selection(string="State",copy=False,selection=[('accepted','Accepted'),('rejected','Rejected')])
    partner_id = fields.Many2one('res.partner', string="Partner",required=True)
    property_id = fields.Many2one('estate.property', string="Property",required=True)
    validity = fields.Integer('Validity (Days)',default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    _sql_constraints = [
        ('check_price','CHECK(price > 0)','le prix doit etre superieur a 0')
    ]

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity is not None:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline=False

    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_confirm_offer(self):
        self.ensure_one()
        if self.state == 'rejected':
            raise UserError("offre rejeté ne peut plus etre accepté")
        else:
            self.state = 'accepted'
            other_offers = self.search([
                ('property_id', '=', self.property_id.id),
                ('id', '!=', self.id),
                ('state', '!=', 'rejected')
            ])
            other_offers.write({'state': 'rejected'})
            self.property_id.selling_price = self.price
            self.property_id.partner_id = self.partner_id.id

    def action_decline_offer(self):
        self.ensure_one()
        self.state = 'rejected'




