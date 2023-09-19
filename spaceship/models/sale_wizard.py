from odoo import fields, models


class SaleWizard(models.TransientModel):
    _name = "spaceship.sale.wizard"
    _description = "Wizard for selling ships once a highest bidder is confirmed"

    buyer_name = fields.Char(string="Buyer's Name")

    # Boilerplate to allow me to use a currency for a monetary field
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    sale_amount = fields.Monetary(string="Sale Amount", currency_field="currency_id")
    spaceship_id = fields.Many2one("spaceship.gen", string="Spaceship")

    def sell_ship_from_wizard(self):
        self.spaceship_id.sell_ship(float(self.sale_amount), str(self.buyer_name))
