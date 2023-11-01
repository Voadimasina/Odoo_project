# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AnalysePrestation(models.Model):

    _name = "analyse.prestation"
    _description = "Analyse Prestation"

    client_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        string="Client"

    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        default=lambda self: self.env.user,
        string="Responsable"
    )
    product_id = fields.Many2one(
        comodel_name='radiation.produit',
        required=True,
        string="Produit"
    )
    date = fields.Date(
        default=fields.Date.context_today,
    )
    quantity = fields.Float(
        string="Qauntité",
    )
    uom = fields.Selection(
        selection=[
            ('g', 'Gramme'),
            ('kg', 'Kilogramme'),
            ('t', 'Tonne'),
        ],
        required=True,
        default='t',
        string="Unité",
    )
    prelevement_ids = fields.One2many(
        comodel_name='radiation.prelevement',
        inverse_name='prestation_id',
    )
    # TODO: add fields state
