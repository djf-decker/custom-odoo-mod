from odoo import fields, models


class Spaceship(models.Model):
    _name = "spaceship.gen"
    _description = "Generic Spaceship"

    spaceship_mfg_model = fields.Char(default="Unknown manufacturer")
    spaceship_mfg_date = fields.Date()
    lightspeed_capable = fields.Boolean(required=True)
    planet_of_origin = fields.Char(default="Earth")
