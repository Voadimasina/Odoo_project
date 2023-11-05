# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationPrelevement(models.Model):

    _name = "radiation.prelevement"
    _description = "Radiation Prelevement"

    name = fields.Char(
        string="Référence",
        required=True, copy=False, readonly=True,
        index='trigram',
        default=lambda self: _('Nouveau'),
    )

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("Nouveau")) == _("Nouveau"):
                vals['name'] = self.env['ir.sequence'].next_by_code('radiation.prelevement') or _("Nouveau")
        return super().create(vals_list)

