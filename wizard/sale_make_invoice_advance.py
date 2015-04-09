# -*- encoding: utf-8 -*-
##############################################################################
#
#    partner_billing
#    (C) 2015 Mikołaj Dziurzyński, Grzegorz Grzelak, Thorsten Vocks (big-consulting GmbH)
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

from openerp.osv import osv
from openerp import fields, models 
import logging

_logger = logging.getLogger(__name__)

class sale_advance_payment_inv(osv.osv_memory):
	_inherit = "sale.advance.payment.inv"

	def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
		res = super(sale_advance_payment_inv,self)._prepare_advance_invoice_vals(cr, uid, ids, context=context)
		sale_order_obj = self.pool.get('sale.order')
		for pair in res:
			for sale in sale_order_obj.browse(cr, uid, [pair[0]]):
				pair[1]['associated_partner'] = sale.associated_partner and sale.associated_partner.id or False

		return res

