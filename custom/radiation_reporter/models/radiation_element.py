# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationElement(models.Model):

    _name = "radiation.element"
    _description = "Radiation Element"

    name = fields.Char(
        required=True,
        string="Nom"
    )
    code = fields.Char(
        required=True,
    )
    low_level = fields.Integer(
        string="Niveau faible"
    )
    level_exemption = fields.Integer(
        string="Niveau d'exemption",
    )
