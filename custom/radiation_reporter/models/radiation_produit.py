# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationProduit(models.Model):

    _name = "radiation.produit"
    _description = "Radiation Produit"

    name = fields.Char(
        string="Type",
        required=True,
    )
    description = fields.Text()
