# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationMatiere(models.Model):

    _name = "radiation.matiere"
    _inherit = ['radiation.mesure']
    _description = "Matière"

    analyse_id = fields.Many2one(
        comodel_name="radiation.analyse",
        required=True,
    )
