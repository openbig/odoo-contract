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

import logging

_logger = logging.getLogger(__name__)


class res_partner_grade(osv.Model):
    _inherit = 'res.partner.grade'
    reseller_pricelist = fields.Many2one(
        'product.pricelist', 'Reseller Pricelist')
    commission_pricelist = fields.Many2one(
        'product.pricelist', 'Commission Pricelist', domain="[('type', '=', 'partner_commission')]")


class res_partner(osv.Model):
    _inherit = 'res.partner'

    def _commission_invoices(self):
        for partner in self:
            partner.commission_invoices_count = len(
                self.env['account.invoice'].search([['partner_id', '=', partner.id],['commission_type','=','commission_invoice']]))

    commission_journal = fields.Many2one(
        'account.journal', 'Journal for Commissions')
    commission_invoices_count = fields.Integer(
        compute="_commission_invoices", string="Commission Invoices")
