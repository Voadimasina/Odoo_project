# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationResultat(models.Model):

    _name = "radiation.resultat"
    _description = "Résultat"

    name = fields.Char(
        string="Référence du résultat",
        required=True, copy=False, readonly=True,
        index='trigram',
        default=lambda self: _('Nouveau'),
    )
    date = fields.Date(
        default=fields.Date.context_today,
    )
    analyse_id = fields.Many2one(
        comodel_name='radiation.analyse',
    )
    client_id = fields.Many2one(
        comodel_name='res.partner',
        related="analyse_id.client_id",
        store=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.partner',
        defaulf=lambda self: self.env.user,
    )
    line_ids = fields.One2many(
        comodel_name='radiation.resultat.line',
        inverse_name='resultat_id',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("Nouveau")) == _("Nouveau"):
                vals['name'] = self.env['ir.sequence'].next_by_code('radiation.resultat') or _("Nouveau")
        return super().create(vals_list)
