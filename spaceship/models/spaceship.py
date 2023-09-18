from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date


class Spaceship(models.Model):
    _name = "spaceship.gen"
    _description = "Generic Spaceship"
    _order = "spaceship_mfg desc, spaceship_mfg_model desc"

    # Since this app is for selling spaceships, possibly lightspeed-capable and offworld-manufactured,
    # I reckon spaceship ages as if it were 150 years in the future.
    _canon_present_day: date = fields.Date.today() + relativedelta(years=150)

    name = fields.Char(compute="_compute_name", string="Manufacturer and Model")
    years_of_age = fields.Char(
        compute="_compute_spaceship_age",
        inverse="_inverse_spaceship_age",
        store=True,
        string=f"Years of Age as of {_canon_present_day.strftime('%m/%d/%Y')}"
    )
    spaceship_mfg = fields.Many2one("spaceship.mfg", required=True, string="Spaceship Manufacturer")
    spaceship_mfg_model = fields.Char(default="Unknown model", string="Model")
    spaceship_mfg_date = fields.Date(required=True, string="Date of Manufacture")
    lightspeed_capable = fields.Boolean(required=True, string="Has Lightspeed Capability")
    planet_of_origin = fields.Char(default="Earth", string="Planet of Origin")

    # Boilerplate to allow me to use a currency for a monetary field
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    # Attributes for bidding on ships
    highest_bidder = fields.Char(string="Highest Bidder", default="No bids yet")
    highest_bid = fields.Monetary(string="Highest Bid", currency_field="currency_id", default=0.00)
    date_of_last_bid = fields.Date(string="Date of highest bid",  required=False)
    sale_record = fields.Many2one("spaceship.sale", required=False, string="Sale record")

    @api.depends("spaceship_mfg", "spaceship_mfg_model")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.spaceship_mfg.name} {record.spaceship_mfg_model}"

    @api.depends("spaceship_mfg_date")
    def _compute_spaceship_age(self):
        for record in self:
            mfg_date = fields.Date.to_date(record.spaceship_mfg_date)
            record.years_of_age = str(relativedelta(self._canon_present_day, mfg_date).years)

    def _inverse_spaceship_age(self):
        for record in self:
            current_year = self._canon_present_day.year
            new_mfg_year = current_year - int(record.years_of_age)
            record.spaceship_mfg_date = record.spaceship_mfg_date.replace(year=new_mfg_year)

    @api.constrains("spaceship_mfg_date")
    def _check_mfg_date(self):
        for record in self:
            if record.spaceship_mfg_date > self._canon_present_day:
                raise ValidationError(
                    "A spaceship's manufacturing date cannot be in the future "
                    + f"relative to {self._canon_present_day}."
                )

    def launch_bid_wizard(self):
        wizard = self.env["spaceship.bid.wizard"].create({
            "spaceship_id": self.id
        })
        return {
            'name': "Spaceship Bid",
            'type': 'ir.actions.act_window',
            'res_model': 'spaceship.bid.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new'
        }

    def place_bid(self, bid: float, bidder_name: str):
        for record in self:
            if bid > record.highest_bid:
                record.highest_bid = bid
                record.highest_bidder = bidder_name
                print(f"-=[ {bidder_name} placed a bid of {bid} on {self.name}. ]=-")
            elif bid < 0:
                raise ValidationError("You cannot bid a negative amount of money.")
            else:
                raise ValidationError("You cannot place a bid unless it is higher than the last highest bid.")
