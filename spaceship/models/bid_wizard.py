from odoo import fields, models


class BidWizard(models.TransientModel):
    _name = "spaceship.bid.wizard"
    _description = "Wizard for placing bids on ships"

    bidder_name = fields.Char(string="Bidder's Name", required=True)

    # Boilerplate to allow me to use a currency for a monetary field
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    bid_amount = fields.Monetary(string="Bid Amount", currency_field="currency_id", required=True)
    spaceship_id = fields.Many2one("spaceship.gen", string="Spaceship", readonly=True)
