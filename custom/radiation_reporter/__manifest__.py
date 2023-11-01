# Copyright 2023 Voadimasina
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Radiation Reporter',
    'description': """
        Radiation reporter""",
    'version': '16.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Voadimasina',
    'website': 'www.odoo.com',
    'depends': [
        'base', 'web',
    ],
    'data': [
        'security/radiation_analyse.xml',
        'security/radiation_matiere.xml',
        'security/bruit_fond.xml',
        'security/radiation_etalon.xml',
        'security/radiation_element.xml',
        'security/radiation_prelevement.xml',
        'security/radiation_produit.xml',
        'security/analyse_prestation.xml',
        'views/ir_ui_menu.xml',
        'views/analyse_prestation.xml',
        'views/res_partner.xml',
        'views/radiation_element.xml',
        'views/radiation_produit.xml',
        'views/radiation_etalon.xml',
        'views/radiation_analyse.xml',
    ],
    'demo': [
    ],
}
