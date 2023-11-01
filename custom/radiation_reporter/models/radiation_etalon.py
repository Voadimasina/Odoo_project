# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationEtalon(models.Model):
    _name = "radiation.etalon"
    _inherit = ['radiation.mesure']
    _description = "Radiation Etalon"

    geometrie = fields.Char()
    masse = fields.Float()
    activity = fields.Float(
        string="Activité",
    )
    inc_activity = fields.Float(
        string="Incertitude de l'activité"
    )
    facteur_conversion = fields.Float(
        string="facteur de Conversion"
    )
