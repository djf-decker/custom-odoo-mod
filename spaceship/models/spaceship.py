from odoo import fields, models

class Spaceship(models.Model):
    _name = "space.ship"
    _description = "Generic Spaceship"


    spaceship_mfg_model = fields.Char(required=True)
