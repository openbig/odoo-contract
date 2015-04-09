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
from openerp import fields 

class res_partner_grade(osv.Model):
	_inherit = 'res.partner.grade'
	reseller_pricelist = fields.Many2one('product.pricelist','Reseller Pricelist')
	commission_pricelist = fields.Many2one('product.pricelist','Commission Pricelist', domain="[('type', '=', 'partner_commission')]")

class res_partner(osv.Model):
	_inherit = 'res.partner'
	commission_journal = fields.Many2one('account.journal', 'Journal for Commissions')