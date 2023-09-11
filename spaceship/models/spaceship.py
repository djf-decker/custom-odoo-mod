from odoo import api, fields, models


class Spaceship(models.Model):
    _name = "spaceship.gen"
    _description = "Generic Spaceship"

    name = fields.Char(compute="_compute_name", string="Manufacturer and Model")

    spaceship_mfg = fields.Many2one("spaceship.mfg", string="Spaceship Manufacturer")
    spaceship_mfg_model = fields.Char(default="Unknown model", string="Model")
    spaceship_mfg_date = fields.Date(string="Date of Manufacture")
    lightspeed_capable = fields.Boolean(required=True, string="Has Lightspeed Capability")
    planet_of_origin = fields.Char(default="Earth", string="Planet of Origin")

    @api.depends("spaceship_mfg", "spaceship_mfg_model")
    def _compute_name(self):
        for record in self:
            record.name = f"{self.spaceship_mfg.name} {self.spaceship_mfg_model}"
