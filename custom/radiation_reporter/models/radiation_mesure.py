# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationMesure(models.AbstractModel):
    _name = "radiation.mesure"
    _description = "Radiation Mesure"

    element_id = fields.Many2one(
        comodel_name='radiation.element',
        required=True,
    )
    temps_compt = fields.Float(
        default=1,
    )
    aire_nette = fields.Float()
    inc_aire_nette = fields.Float()
    taux_compt = fields.Float(
        compute='_compute_taux_compt',
        store=True,
    )
    inc_taux_compt = fields.Float(
        compute='_compute_taux_compt',
        store=True,
    )

    @api.depends('temps_compt', 'aire_nette', 'inc_aire_nette')
    def _compute_taux_compt(self):
        for rec in self:
            if rec.temps_compt != 0:
                rec.taux_compt = rec.aire_nette / rec.temps_compt
                rec.inc_taux_compt = rec.inc_aire_nette / rec.temps_compt
            else:
                rec.taux_compt = 0
                rec.inc_taux_compt = 0
