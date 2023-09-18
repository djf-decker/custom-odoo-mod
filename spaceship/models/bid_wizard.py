from odoo import fields, models


class BidWizard(models.TransientModel):
    _name = "spaceship.bid.wizard"
    _description = "Wizard for placing bids on ships"

    bidder_name = fields.Char(string="Bidder's Name")

    # Boilerplate to allow me to use a currency for a monetary field
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    bid_amount = fields.Monetary(string="Bid Amount", currency_field="currency_id")
    spaceship_id = fields.Many2one("spaceship.gen", string="Spaceship")

    def place_bid_from_wizard(self):
        self.spaceship_id.place_bid(float(self.bid_amount), str(self.bidder_name))
