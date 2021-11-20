# -*- coding:utf-8 -*-

import logging

from odoo import fields, models, api

logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class Presupuesto(models.Model):
    _name = "presupuesto"
    _inherit = ["image.mixin"]
    name = fields.Char(
        string="Pelicula"
    )
    fch_estreno = fields.Date(string="Fecha estreno")
    clasificacion = fields.Selection(selection=[
        ("G", "G"),  # publico general
        ("PG", "PG"),  # Se recomienda la compañia de un adulto
        ("PG-13", "PG-13"),  # Mayores de 13
        ("R", "R"),  # En compañia de un adulto obligatorio
        ("NC-17", "NC-17"),  # Mayores de 18
    ],
        string="Clasificación"
    )
    des_clasificacion = fields.Char(string="Descripcion clasificacion")
    puntuacion = fields.Integer(string="Puntuación", related="puntuacion2")
    puntuacion2 = fields.Integer(string="Puntuación 2")
    active = fields.Boolean(string="Activo", default=True)
    director_id = fields.Many2one(
        comodel_name="res.partner",
        string="Director"
    )
    categoria_director_id = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoria Director",
        default=lambda self: self.env.ref('peliculas.category_director')
        # Primera version
        # default=lambda self: self.env['res.partner.category'].search([('name', '=', 'Director')])
    )
    genero_ids = fields.Many2many(
        comodel_name="genero",
        string="Generos"
    )
    vista_general = fields.Text(string="Descripción")
    link_trailer = fields.Char(string="Trailer")
    es_libro = fields.Boolean(string="Version Libro")
    libro = fields.Binary(string="Libro")
    libro_filename = fields.Char(string="Nombre del libro")
    state = fields.Selection(
        selection=[
            ('borrador', 'Borrador'),
            ('aprobado', 'Aprobado'),
            ('cancelado', 'Cancelado'),
        ],
        default='borrador',
        string="Estado",
        copy=False
    )
    fch_aprobado = fields.Datetime(string='Fecha aprobado',copy=False)
    num_presupuesto = fields.Char(string="Numero presupuesto",copy=False)

    def aprobar_presupuesto(self):
        logger.info('****************** Entro a la funcion Aprobar presupuesto')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.info('****************** Entro a la funcion Cancelar presupuesto')
        self.state = 'cancelado'

    def unlink(self):
        logger.info('****************** Se disparo la funcion unlink')
        for record in self:
            if record.state != 'cancelado':
                raise UserError('No se puede eliminar el registro porque no se encuenta en el estado cancelado.')
            super(Presupuesto,record).unlink()

    @api.model
    def create(self, variables):
        logger.debug('****************** variables: {0}'.format(variables))
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.presupuesto.pelicula')
        variables['num_presupuesto'] = correlativo
        return super(Presupuesto, self).create(variables)

    def write(self, variables):
        logger.debug('****************** variables: {0}'.format(variables))
        if 'clasificacion' in variables:
            raise UserError('La clasificacion no se puede editar!')
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (copia)'
        default['puntuacion2'] = 1
        return super(Presupuesto,self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.des_clasificacion = 'publico general'
            if self.clasificacion == 'PG':
                self.des_clasificacion = 'Se recomienda la compañia de un adulto'
            if self.clasificacion == 'PG-13':
                self.des_clasificacion = 'Mayores de 13'
            if self.clasificacion == 'R':
                self.des_clasificacion = 'En compañia de un adulto obligatorio'
            if self.clasificacion == 'NC-17':
                self.des_clasificacion = 'Mayores de 18'
        else:
            self.des_clasificacion = False
