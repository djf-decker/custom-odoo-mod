from odoo import fields, models


class SpaceshipManufacturer(models.Model):
    _name = "spaceship.mfg"
    _description = "Spaceship Manufacturer"

    name = fields.Char(default="Unknown Manufacturer", string="Manufacturer")
