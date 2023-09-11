from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date


class Spaceship(models.Model):
    _name = "spaceship.gen"
    _description = "Generic Spaceship"

    # Since this app is for selling spaceships, possibly lightspeed-capable and offworld-manufactured,
    # I reckon spaceship ages as if it were 150 years in the future.
    _canon_present_day: date = fields.Date.today() + relativedelta(years=150)

    name = fields.Char(compute="_compute_name", string="Manufacturer and Model")
    years_of_age = fields.Char(
        compute="_compute_spaceship_age",
        string=f"Years of Age as of {_canon_present_day.strftime('%m/%d/%Y')}"
    )
    spaceship_mfg = fields.Many2one("spaceship.mfg", string="Spaceship Manufacturer")
    spaceship_mfg_model = fields.Char(default="Unknown model", string="Model")
    spaceship_mfg_date = fields.Date(string="Date of Manufacture")
    lightspeed_capable = fields.Boolean(required=True, string="Has Lightspeed Capability")
    planet_of_origin = fields.Char(default="Earth", string="Planet of Origin")

    @api.depends("spaceship_mfg", "spaceship_mfg_model")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.spaceship_mfg.name} {record.spaceship_mfg_model}"

    @api.depends("spaceship_mfg_date")
    def _compute_spaceship_age(self):
        for record in self:
            mfg_date = fields.Date.to_date(record.spaceship_mfg_date)
            record.years_of_age = str(relativedelta(self._canon_present_day, mfg_date).years)
