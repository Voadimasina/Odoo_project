# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationPrelevement(models.Model):

    _name = "radiation.prelevement"
    _description = "Radiation Prelevement"

    prestation_id = fields.Many2one(
        comodel_name='analyse.prestation',
    )
    product_id = fields.Many2one(
        comodel_name='radiation.produit',
        related='prestation_id.product_id',
        string="Produit"
    )
    masse = fields.Float()
    uom = fields.Selection(
        selection=[
            ('mg', 'Milligramme'),
            ('g', 'Gramme'),
            ('kg', 'Kilogramme'),
        ],
        required=True,
        default='g',
        string="Unité",
    )

