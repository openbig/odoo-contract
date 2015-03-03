# -*- encoding: utf-8 -*-
##############################################################################
#
#    contractmanagement_licenses
#    (C) 2014 big-consulting GmbH
#    (C) 2014 OpenGlobe
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _

import logging

logger = logging.getLogger(__name__)


class sale_order_line(models.Model):

    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom,
                                                             qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag, context)

        logger.warn(product)
        res['value']['is_module'] = self._is_mod(
            cr, uid, product, context=None)
        res['value']['is_application'] = self._is_app(
            cr, uid, product, context=None)
        return res

    def _is_mod(self, cr, uid, product, context=None):
        settings_obj = self.pool.get("contract.view.setting")
        product_obj = self.pool.get("product.product")
        settings_id = settings_obj.search(
            cr, uid, [], limit=1, order='id desc')
        for sett in settings_obj.browse(cr, uid, settings_id, context):
            product_br = product_obj.browse(cr, uid, product)
            sett.modules_categ
            if sett.modules_categ == product_br.categ_id:
                return True
            else:
                return False

    def _is_app(self, cr, uid, product, context=None):
        settings_obj = self.pool.get("contract.view.setting")
        product_obj = self.pool.get("product.product")
        settings_id = settings_obj.search(
            cr, uid, [], limit=1, order='id desc')
        for sett in settings_obj.browse(cr, uid, settings_id, context):
            product_br = product_obj.browse(cr, uid, product)
            sett.modules_categ
            if sett.applications_categ == product_br.categ_id:
                return True
            else:
                return False

    is_module = fields.Boolean(string="Module?")
    is_application = fields.Boolean(string="Objectpackage?")
