# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationAnalyse(models.Model):
    _name = "radiation.analyse"
    _description = "Radiation Analyse"

    date = fields.Date()
    user_id = fields.Many2one(
        comodel_name='res.users',
        default=lambda self: self.env.user,
    )
    client_id = fields.Many2one(
        comodel_name='res.partner',
        related="prestation_id.client_id",
        store=True,
    )
    prestation_id = fields.Many2one(
        comodel_name='analyse.prestation',
        required=True,
    )
    prelevement_id = fields.Many2one(
        comodel_name='radiation.prelevement',
        domain="[('prestation_id', '=', prestation_id)]",
        required=True,
    )
    etalon_ids = fields.Many2many(
        comodel_name='radiation.etalon',
    )
    bruit_ids = fields.One2many(
        comodel_name="bruit.fond",
        inverse_name="analyse_id",
    )
    matiere_ids = fields.One2many(
        comodel_name="radiation.matiere",
        inverse_name="analyse_id",
    )
