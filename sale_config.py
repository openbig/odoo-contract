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

from openerp.osv import fields, osv

import logging

logger = logging.getLogger(__name__)


class sale_configuration(osv.TransientModel):
    _inherit = 'sale.config.settings'

    _columns = {
        'module_contractmanagement_licenses': fields.boolean('Modules and Objectpackages Views on Contracts'),
        'modules_product_categ': fields.many2one('product.category', 'Modules Category'),
        'applications_product_categ': fields.many2one('product.category', 'Objectpackages Category'),
    }

    def default_get(self, cr, uid, fields, context=None):
        contract_view_set_obj = self.pool.get('contract.view.setting')
        res = super(sale_configuration, self).default_get(cr, uid, fields, context)
        vset_ids = contract_view_set_obj.search(cr, uid, [])
        vset_rec = vset_ids and max(vset_ids)
        for record in contract_view_set_obj.browse(cr, uid, vset_rec):
            res['modules_product_categ'] = record.modules_categ.id
            res['applications_product_categ'] = record.applications_categ.id
        return res

    def _change_categs(self, cr, uid, ids, context=None):
        contract_view_set_obj = self.pool.get('contract.view.setting')
        for new in self.browse(cr, uid, ids[0]):
            mod_categ_id = new.modules_product_categ and new.modules_product_categ.id or False
            logger.warn(new.modules_product_categ)
            logger.warn(mod_categ_id)
            app_categ_id = new.applications_product_categ and new.applications_product_categ.id or False
            vals = {}
            mod_categ_id and vals.update({'modules_categ': mod_categ_id})
            app_categ_id and vals.update({'applications_categ': app_categ_id})
            logger.warn(vals)
            contract_view_set_obj.create(cr, uid, vals)
        return True

    def set_modules_product_categ(self, cr, uid, ids, context=None):
        res = self._change_categs(cr, uid, ids, context)
        return res

    def set_applications_product_categ(self, cr, uid, ids, context=None):
        res = self._change_categs(cr, uid, ids, context)
        return res
