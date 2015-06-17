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
from openerp import _
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)


class sale_order(osv.osv):
    _inherit = "sale.order"

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """Prepare the dict of values to create the new invoice for a
           sales order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: sale.order record to invoice
           :param list(int) line: list of invoice line IDs that must be
                                  attached to the invoice
           :return: dict of value to create() the invoice
        """
        if context is None:
            context = {}
        journal_ids = self.pool.get('account.journal').search(cr, uid,
                                                              [
                                                                  ('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
                                                              limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                                 _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        invoice_vals = {
            'name': order.client_order_ref or '',
            'origin': order.name,
            'expected_contract_start': order.expected_date,
            'type': 'out_invoice',
            'reference': order.client_order_ref or order.name,
            'account_id': order.partner_id.property_account_receivable.id,
            'partner_id': order.partner_invoice_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': [(6, 0, lines)],
            'currency_id': order.pricelist_id.currency_id.id,
            'comment': order.note,
            'payment_term': order.payment_term and order.payment_term.id or False,
            'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
            'date_invoice': context.get('date_invoice', False),
            'company_id': order.company_id.id,
            'user_id': order.user_id and order.user_id.id or False,
            'section_id': order.section_id.id
        }

        # Care for deprecated _inv_get() hook - FIXME: to be removed after 6.1
        invoice_vals.update(self._inv_get(cr, uid, order, context=context))
        return invoice_vals

    def _days_to_contract_end(self, cr, uid, ids, name=None, arg=None, context=None):
        res = {}
        for so in self.browse(cr, uid, ids, context=None):
            if not so.project_id or not so.project_id.recurring_invoices:
                res[so.id] = 0
                return res
            next_inv_date = datetime.strptime(
                so.project_id.recurring_next_date, '%Y-%m-%d') + relativedelta(weeks=6)
            remaining_days = next_inv_date - datetime.today()
            res[so.id] = remaining_days.days
            return res

    _columns = {
        'days_to_contract_end': fields.function(_days_to_contract_end, string="Remaining Contract Days"),
        'expected_date': fields.date('Expected Contract Start'),
    }

    def onchange_remaining_days(self, cr, uid, ids, project_id, context=None):
        res = {}
        contract_obj = self.pool.get('account.analytic.account')
        for proj in contract_obj.browse(cr, uid, project_id, context=None):
            next_inv_date = datetime.strptime(
                proj.recurring_next_date, '%Y-%m-%d') + relativedelta(weeks=6)
            remaining_days = next_inv_date - datetime.today()

            res = {'value': {'days_to_contract_end': remaining_days.days}}
        return res


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    _columns = {
        'related_contract': fields.related('order_id', 'project_id', type='many2one', relation='account.analytic.account', string='Related Contract'),
        'license_owner': fields.related('order_id', 'partner_shipping_id', type='many2one', relation='res.partner', string='License Owner'),
    }

    def new_contract(self, cr, uid, ids, context):
        acc_a_inv_line_obj = self.pool.get('account.analytic.invoice.line')
        '''open account.analtic.account window and pass values as default'''
        ctx = context.copy()
        for sale_order_line in self.browse(cr, uid, ids, context):
            part = self.pool.get('res.partner').browse(
                cr, uid, sale_order_line.order_id.partner_id.id, context=ctx)
            if part.lang:
                ctx.update({'lang': part.lang})
            invoice_line_products = (0, 0)
            for sol in sale_order_line.order_id.order_line:
                if sol.product_id.auto_create_task:
                    new_product = acc_a_inv_line_obj.product_id_change(cr,
                                                                       uid,
                                                                       ids,
                                                                       sol.product_id.id,
                                                                       False,
                                                                       partner_id=sale_order_line.order_id.partner_id.id,
                                                                       price_unit=sol.product_id.lst_price,
                                                                       pricelist_id=sol.order_id.pricelist_id.id,
                                                                       context=ctx)['value']
                    new_product.update({'product_id': sol.product_id.id})
                    invoice_line_products = invoice_line_products + \
                        (new_product,)
            sla_ids_vals = [(4, x.id) for x in sale_order_line.product_id.sla]
            ctx.update(
                {
                    'default_partner_id': sale_order_line.order_id.partner_shipping_id and sale_order_line.order_id.partner_shipping_id.id or sale_order_line.order_id.partner_id.id,
                    'default_type': 'contract',
                    'default_state': 'preparing',
                    'default_fix_price_invoices': True,
                    'default_code': sale_order_line.order_id.name,
                    #                    'default_recurring_invoices': True,
                    'default_recurring_invoice_line_ids': invoice_line_products,
                    'default_sla_ids': sla_ids_vals,
                    'default_recurring_rule_type': 'yearly',
                    'default_manager_id': sale_order_line.order_id.user_id.id,
                    'default_message_follower_ids': [(4, sale_order_line.order_id.partner_id.id)],
                    'default_sale_order_line': sale_order_line.id,
                    'default_pricelist_id': sale_order_line.order_id.pricelist_id.id,
                }
            )
            if sale_order_line.order_id.expected_date:
                ctx.update({
                    'default_date_start': sale_order_line.order_id.expected_date,
                })
        res = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'sale_contractmanagement', 'view_account_analytic_account_form_remodelled')
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res and res[1] or False],
            'res_model': 'account.analytic.account',
            'context': ctx,
            'type': 'ir.actions.act_window',
            'nodestroy': False,
            'target': 'new',
        }
