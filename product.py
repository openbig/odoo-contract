# -*- encoding: utf-8 -*-
##############################################################################
#
#    product_digital_media
#    (C) 2015 big-consulting GmbH
#    (C) 2015 OpenGlobe
#    Author: Thorsten Vocks (openBIG.org)
#    Author: Mikołaj Dziurzyński, Grzegorz Grzelak (OpenGlobe)
#
#    All Rights reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. , default='fields.Date.context_today'
#
##############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _


import logging

_logger = logging.getLogger(__name__)


class digital_media(models.Model):
    _name = 'digital.media'

    date = fields.Date("Creation Date", default=fields.Date.context_today)
    uploaded_by = fields.Many2one(
        'res.users', 'Uploaded by', default=lambda self: self.env.uid)
    data = fields.Binary('File Data')
    filename = fields.Char('Filename')
    title_name = fields.Char('Title Name')
    extension = fields.Char('File Extension')
    product_ids = fields.Many2many(comodel_name='product.product', relation='digital_media_product_product_rel',
                                   column1='digital_media_id', column2='product_product_id', string='Products')
    description = fields.Text('Description')

    @api.onchange('filename')
    def get_all(self):
        if self.filename:
            splitted = self.filename.split('.', 1)
            if len(splitted) > 1:
                self.title_name, self.extension = splitted
            else:
                for string in splitted:
                    self.title_name = splitted

    @api.multi
    def write(self, vals):
        if 'product_ids' in vals:
            analytic_invoice_line_obj = self.env[
                'account.analytic.invoice.line']
            for product_id in vals['product_ids'][0][2]:
                invoice_lines = analytic_invoice_line_obj.search(
                    [['product_id', '=', product_id]])
                for line in invoice_lines:
                    line.analytic_account_id._get_downloads()
        return super(digital_media, self).write(vals)

    @api.multi
    def get_form(self):
        _logger.warn(locals())
        _logger.warn(self.id)
        return {
            'name': _('Digital Media'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': 'digital.media',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

class product_product(models.Model):
    _inherit = 'product.product'

    file_ids = fields.Many2many(comodel_name='digital.media', relation='digital_media_product_product_rel',
                                column1='product_product_id', column2='digital_media_id', string='File')


class digital_media_product_product_rel(models.Model):
    _name = 'digital.media.product.product.rel'
    digital_media_id = fields.Many2one('digital.media', 'Related Downloads')
    product_product_id = fields.Many2one('product.product', 'Related Products')

product_product()
