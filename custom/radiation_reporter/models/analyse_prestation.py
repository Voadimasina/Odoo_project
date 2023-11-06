# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date
import base64
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalysePrestation(models.Model):
    _name = "analyse.prestation"
    _description = "Analyse Prestation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    resultat_ids = fields.One2many(
        comodel_name='radiation.resultat',
        compute='_compute_resultat_ids'
    )
    resultat_count = fields.Integer(
        compute='_compute_resultat_ids'
    )
    analyse_ids = fields.One2many(
        comodel_name='radiation.analyse',
        inverse_name='prestation_id',
    )
    analyse_count = fields.Integer(
        compute='_compute_analyse_count',
    )

    @api.depends('analyse_ids')
    def _compute_analyse_count(self):
        for rec in self:
            rec.analyse_count = len(rec.analyse_ids)

    @api.depends('prelevement_ids.resultat_id')
    def _compute_resultat_ids(self):
        for rec in self:
            rec.resultat_ids = rec.prelevement_ids.resultat_id
            rec.resultat_count = len(rec.prelevement_ids.resultat_id)

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
        }
        action['view_mode'] = 'form'
        action['domain'] = [('prestation_id', '=', self.id)]
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

    def action_send_mail(self):
        attachment_id = self.action_generate_report()
        mail_template = self.env.ref('radiation_reporter.email_template_radiation_report')
        email = self.client_id.email
        email_values = {
            'email_to': email,
            'attachment_ids': [(6, 0, [attachment_id])],
        }
        mail_template.send_mail(self.id, force_send=True, email_values=email_values)

    def action_generate_report(self):
        self.ensure_one()
        data = self._prepare_data_report()
        today = date.today()
        Report = self.env['ir.actions.report']
        pdf, format = Report._render_qweb_pdf('radiation_reporter.radiation_report_details_report', data=data)
        attachment_name = _("Rapport_analyse_radiation_%s.pdf") % (today.strftime('%d_%B_%Y'))
        res = self._create_attachment(pdf, attachment_name)
        return res

    def _prepare_data_report(self):
        code = 1
        resultats_data = []
        for resultat in self.resultat_ids:
            line_data = []
            first_line = True
            for line in resultat.line_ids:
                resultats_data.append({
                    'code': code,
                    'rowspan': len(resultat.line_ids) if first_line else 0,
                    'famille': line.element_id.name,
                    'activity': round(line.activite, 2),
                    'inc_activity': round(line.inc_activite, 2),
                    'level_exemption': line.element_id.level_exemption,
                })
                first_line = False
            code += 1
        levels = resultat.line_ids.mapped('level')
        tri_key = ['low', 'normal', 'high']
        level = max(levels, key=lambda x: (tri_key.index(x), levels[::-1].index(x)))
        return {
            'resultats': resultats_data,
            'date': date.today().strftime('%d %B %Y'),
            'level': level,
            'client': self.client_id.display_name,
            'resp': self.user_id.display_name,
            'produit': self.product_id.display_name,
            'ref': '%s/%s/INSTN/DG/ATN/Rv' % (date.today().strftime("%y/%m/%d"), resultat.id),
        }

    def _create_attachment(self, pdf, name):
        attachment = self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            'datas': base64.b64encode(pdf),
            'mimetype': 'application/x-pdf',
            'res_id': self.id,
            'res_model': 'analyse.prestation',
        })
        return attachment.id

    def action_view_resultats(self):
        action = self.sudo().env.ref('radiation_reporter.radiation_resultat_act_window').read()[0]
        action.update({
            'domain': [('id', 'in', self.resultat_ids.ids)],
        })
        return action

    def action_view_analyse(self):
        action = self.sudo().env.ref('radiation_reporter.radiation_analyse_act_window').read()[0]
        action.update({
            'domain': [('prestation_id', '=', self.id)],
        })
        return action
    # TODO: add fields state
