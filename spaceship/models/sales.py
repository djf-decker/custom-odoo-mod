from odoo import fields, api, models


class Sale(models.Model):
    _name = "spaceship.sale"
    _description = "Record of a spaceship's sale"
    date_of_sale = fields.Date(required=True, string="Date of Sale")
    buyer_name = fields.Char(required=True, string="Buyer's Name")

    # Boilerplate to allow me to use a currency for a monetary field
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    sale_price = fields.Monetary(string="Price for which it was sold", currency_field="currency_id")


    # defined for debugging/logging purposes
    def __str__(self):
        return f"Sold to {self.buyer_name} for € {self.sale_price:.2f} on {self.date_of_sale}"
