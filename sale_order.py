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
from openerp import fields, models, api
from openerp.tools.translate import _

import logging

_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = "sale.order"
    associated_partner = fields.Many2one('res.partner', "Associated Partner", domain=[(
        'grade_id', '!=', False)], help="Partner/Reseller who reported this lead. Important for commission invoices.")

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(
            cr, uid, order, lines, context=context)
        res['associated_partner'] = order.associated_partner and order.associated_partner.id or False
        return res

    @api.onchange('partner_invoice_id')
    def onchange_partner_invoice_id(self):
        if self.partner_invoice_id.grade_id:
            if not self.partner_invoice_id.grade_id.reseller_pricelist:
                raise osv.except_osv(_('Missing Values Error!'), _(
                    "Partner {0} has no reseller pricelist defined! Please go into partner grade {1} and define a reseller pricelist!".format(self.partner_invoice_id.name, self.partner_invoice_id.grade_id.name)))
            self.pricelist_id = self.partner_invoice_id.grade_id.reseller_pricelist.id


class crm_make_sale(osv.osv_memory):
    _inherit = 'crm.make.sale'

    def makeOrder(self, cr, uid, ids, context=None):
        res = super(crm_make_sale, self).makeOrder(
            cr, uid, ids, context=context)
        # deal only with singles
        if not isinstance(res['res_id'], int):
            return res
        data = context and context.get('active_ids', []) or []
        crm_lead_obj = self.pool.get('crm.lead')
        sale_order_obj = self.pool.get('sale.order')
        for quotation in sale_order_obj.browse(cr, uid, res['res_id']):
            lead = crm_lead_obj.browse(cr, uid, data)[0]
            vals = {
                'associated_partner': lead and lead.associated_partner.id or False,
                'campaign_id': lead and lead.campaign_id.id or False,
                'medium_id': lead and lead.medium_id.id or False,
                'source_id': lead and lead.source_id.id or False,
            }
            sale_order_obj.write(cr, uid, [quotation.id], vals)

        return res
