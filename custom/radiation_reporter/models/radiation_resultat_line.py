# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class RadiationResultatLine(models.Model):
    _name = "radiation.resultat.line"
    _description = "Radiation Resultat Line"

    resultat_id = fields.Many2one(
        comodel_name='radiation.resultat',
    )
    element_id = fields.Many2one(
        comodel_name='radiation.element',
    )
    activite = fields.Float(
        string='Activité',
        digits=(12, 5),
    )
    inc_activite = fields.Float(
        string='Incertitude activité',
        digits=(12, 5),
    )
    teneur = fields.Float(
        digits=(12, 5),
    )
    level = fields.Selection(
        selection=[
            ('low', 'Faible'),
            ('normal', 'Normal'),
            ('high', 'Elevé'),
        ],
        compute='_compute_level',
        string="Niveau"
    )

    @api.depends('element_id.low_level', 'element_id.level_exemption', 'activite')
    def _compute_level(self):
        for rec in self:
            if rec.activite < rec.element_id.low_level:
                rec.level = 'low'
            elif rec.activite >= rec.element_id.level_exemption:
                rec.level = 'high'
            else:
                rec.level = 'normal'
