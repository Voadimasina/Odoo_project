# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from math import sqrt
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class RadiationAnalyse(models.Model):
    _name = "radiation.analyse"
    _description = "Radiation Analyse"

    name = fields.Char(
        string="Référence",
        required=True, copy=False, readonly=True,
        index='trigram',
        default=lambda self: _('Nouveau'),
    )
    date = fields.Date(
        default=fields.Date.context_today,
    )
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
        domain="[('prestation_id', '=', prestation_id), ('resultat_id','=', False)]",
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
    resultat_ids = fields.One2many(
        comodel_name="radiation.resultat",
        inverse_name="analyse_id",
    )
    resultat_count = fields.Integer(
        compute="_compute_resultat_count"
    )

    def action_view_resultats(self):
        action = self.sudo().env.ref('radiation_reporter.radiation_resultat_act_window').read()[0]
        action.update({
            'domain': [('id', 'in', self.resultat_ids.ids)],
        })
        return action

    @api.depends('resultat_ids')
    def _compute_resultat_count(self):
        for rec in self:
            rec.resultat_count = len(rec.resultat_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("Nouveau")) == _("Nouveau"):
                vals['name'] = self.env['ir.sequence'].next_by_code('radiation.analyse') or _("Nouveau")
        res = super().create(vals_list)
        res.prestation_id.write({'state': 'in_progress'})
        return res

    def action_generate_resultat(self):
        self.ensure_one()
        matieres = self.matiere_ids
        etalons = self.etalon_ids
        bruits = self.bruit_ids
        prelevement_masse = self.prelevement_id.masse
        if not matieres.element_id:
            raise ValidationError("Matières manquants")
        if matieres.element_id - etalons.element_id:
            raise ValidationError("Etalons manquants")
        if matieres.element_id - bruits.element_id:
            raise ValidationError("Bruits de fond manquants")
        line_data = []
        try:
            for matiere in matieres:
                etalon = etalons.filtered(lambda l: l.element_id == matiere.element_id)[0]
                bruit = bruits.filtered(lambda l: l.element_id == matiere.element_id)[0]
                taux_compt_etalon = etalon.taux_compt - bruit.taux_compt
                taux_compt_matiere = matiere.taux_compt - bruit.taux_compt
                inc_taux_compt_etalon = sqrt(etalon.inc_taux_compt ** 2 + bruit.inc_taux_compt ** 2)
                inc_taux_compt_matiere = sqrt(matiere.inc_taux_compt ** 2 + bruit.inc_taux_compt ** 2)
                activite = (etalon.activity * taux_compt_matiere * etalon.masse) / (
                            taux_compt_etalon * prelevement_masse)
                inc_activite = activite * sqrt(
                    (inc_taux_compt_etalon / taux_compt_etalon) ** 2
                    + (inc_taux_compt_matiere / taux_compt_matiere) ** 2
                    + (etalon.inc_activity / etalon.activity) ** 2
                )
                teneur = activite / etalon.facteur_conversion
                line_data.append((0, 0, {
                    'element_id': matiere.element_id.id,
                    'activite': activite,
                    'inc_activite': inc_activite,
                    'teneur': teneur,
                }))
        except ZeroDivisionError:
            raise UserError('Division par zéro impossible, veuillez vérifier les données saisies')
        resultat_data = {
            "analyse_id": self.id,
            "user_id": self.user_id.id,
            "line_ids": line_data
        }
        resultat = self.env["radiation.resultat"].create(resultat_data)
        self.prelevement_id.write({"resultat_id": resultat.id})
