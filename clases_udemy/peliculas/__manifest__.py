# -*- coding:utf-8 -*-

{
    'name': 'Modulo de peliculas',
    'version': '1.0',
    'depends': [
        'contacts',
    ],
    'author': 'Andres Gonzalez',
    'category': 'Peliculas',
    'website': 'https://www.google.com',
    'summary': 'Modulo de presupuestos para peliculas',
    'description': '''
    Modulo para hacer presupuestos de peliculas
    ''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/categoria.xml',
        'data/secuencia.xml',
        'wizard/update_wizard_view.xml',
        'views/menu.xml',
        'views/presupuesto.xml',
    ],
}