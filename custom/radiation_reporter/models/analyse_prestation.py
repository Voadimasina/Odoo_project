# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalysePrestation(models.Model):

    _name = "analyse.prestation"
    _description = "Analyse Prestation"

    name = fields.Char(
        string="Référence de la prestation",
        required=True, copy=False, readonly=True,
        index='trigram',
        default=lambda self: _('Nouveau'))

    state = fields.Selection(
        selection=[
            ('draft', 'Nouveau'),
            ('in_progress', 'En cours'),
            ('done', 'Terminé'),
        ],
        default='draft',
    )

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

    def action_set_done(self):
        self.write({'state': 'done'})

    def action_set_cancel(self):
        self.write({'state': 'draft'})

    def action_perform_analysis(self):
        self.ensure_one()
        if not self.prelevement_ids:
            raise ValidationError("On ne peut pas effectuer une analyse sans prélèvement")
        action = self.env['ir.actions.actions']._for_xml_id('radiation_reporter.radiation_analyse_act_window')
        action['context'] = {
            'default_prestation_id': self.id,
            'default_prelevement_id': self.prelevement_ids[0].id,
        }
        action['view_mode'] = 'form'
        return action

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("Nouveau")) == _("Nouveau"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['date'])
                ) if 'date' in vals else None
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'analyse.prestation', sequence_date=seq_date) or _("Nouveau")
        return super().create(vals_list)
    # TODO: add fields state
