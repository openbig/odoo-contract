# -*- encoding: utf-8 -*-
##############################################################################
#
#    sale_contractmanagement
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

_logger = logging.getLogger(__name__)


class task(osv.Model):
    _inherit = "project.task"
    _columns = {
        'related_contract': fields.related('sale_line_id', 'related_contract', type='many2one', relation='account.analytic.account', string='Related Contract'),
        'license_owner': fields.related('sale_line_id', 'license_owner', type='many2one', relation='res.partner', string='License Owner'),
    }

    def new_contract_from_task(self, cr, uid, ids, context):
        so_line_obj = self.pool.get('sale.order.line')
        for record in self.browse(cr, uid, ids, context):
            ctx = context.copy()
            ctx.update({'active_ids': [record.sale_line_id.id]})
            res = so_line_obj.new_contract(
                cr, uid, [record.sale_line_id.id], context)
            return res


class procurement_order(osv.Model):
    _inherit = 'procurement.order'

    def run(self, cr, uid, ids, autocommit=False, context=None):
        ctx = context.copy()
        if not context.get('lang', False):
            ctx['lang'] = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).lang

        return super(procurement_order, self).run(
            cr, uid, ids, autocommit=autocommit, context=ctx)
