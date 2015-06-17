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

from openerp import api
from openerp import fields as new_fields
from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID
from urlparse import urljoin

import logging

_logger = logging.getLogger(__name__)


class account_analytic_invoice_line(osv.Model):
    _inherit = "account.analytic.invoice.line"

    def default_get(self, cr, uid, fields, context=None):
        res = super(account_analytic_invoice_line, self).default_get(
            cr, uid, fields, context=context)
        return res

    # Overriding for the needs of corect variant price definition
    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', partner_id=False, price_unit=False, pricelist_id=False, company_id=None, context=None):
        local_context = dict(
            context, company_id=company_id, force_company=company_id, pricelist=pricelist_id)
        product_br = self.pool.get('product.product').browse(
            cr, uid, product, local_context)
        res = super(account_analytic_invoice_line, self).product_id_change(cr, uid, ids, product, uom_id, qty=qty, name=name,
                                                                           partner_id=partner_id, price_unit=product_br.lst_price, pricelist_id=pricelist_id, company_id=company_id, context=context)
        return res


class account_a_account(osv.Model):
    _inherit = "account.analytic.account"

    def _get_email(self, cr, uid, ids, name, arg, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, SUPERUSER_ID, ids, context=context):
            result[obj.id] = obj.manager_id.email
        return result

    def _get_phone(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for acc in self.browse(cr, SUPERUSER_ID, ids, context=context):
            res[acc.id] = acc.manager_id.phone or acc.manager_id.mobile or ''
        return res

    def _get_image(self, cr, uid, ids, name, arg, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, SUPERUSER_ID, ids, context=context):
            cr.execute('''select encode(image,'base64') from res_partner where id={0};'''.format(
                obj.manager_id.partner_id.id))
            image = cr.fetchone()
            if image and image[0]:
                result[obj.id] = tools.image_resize_image_medium(
                    image[0].decode('base64'))
        return result

    def _get_portal_login_page(self, cr, uid, context=None):
        base_url = self.pool.get('ir.config_parameter').get_param(
            cr, SUPERUSER_ID, 'web.base.url')
        url = urljoin(base_url, '/web/login')
        return url

    _columns = {
        'color': fields.integer('Color Index'),
        'days_before_end': fields.integer('Days before Contract Ends', help='Invoice will be created some time before contract ends.'),
        'state': fields.selection([('template', 'Template'),
                                   ('preparing', 'Preparing'),
                                   ('draft', 'New'),
                                   ('open', 'In Progress'),
                                   ('pending', 'To Renew'),
                                   ('close', 'Closed'),
                                   ('cancelled', 'Cancelled')],
                                  'Status', required=True,
                                  track_visibility='onchange', copy=False),
        'unlimited': fields.boolean('Unlimited Contract', help="If this field is checked there will be on notifications about contract expiration"),
        'recurring_rule_type': fields.selection([
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)'),
        ], 'Recurrency', help="Invoice automatically repeat at specified interval"),
        'num_of_invoices': fields.integer('Number of Created Invoices'),
        'sale_order_line': fields.many2one('sale.order.line', 'Origin Sale Order Line'),
        'license_filename': fields.char("License Name", size=64, readonly=True),
        'license_file': fields.binary('License', readonly=True),
        'license_ids': fields.one2many('res.license', 'contract_id', 'Available Licenses'),
        'manager_tel': fields.function(_get_phone, type="char", string="Managers' Phone No."),
        'manager_image': fields.function(_get_image, type="binary", string="Managers' Image"),
        'manager_email': fields.function(_get_email, type="char", string="Managers' Email"),
        'portal_login_page': fields.char('Portal Login Page', help='Field for portal information management.'),
    }

    file_ids = new_fields.Many2many(
        comodel_name='digital.media', string='File')

    _defaults = {
        'num_of_invoices': 0,
        'days_before_end': 42,
        'recurring_rule_type': 'yearly',
        'portal_login_page': _get_portal_login_page,
    }

    # Overriding pricelist_id field functionality from hr_timesheet_invoice
    def on_change_partner_id(self, cr, uid, ids, partner_id, name, context=None):
        res = super(account_a_account, self).on_change_partner_id(
            cr, uid, ids, partner_id, name, context=context)
        if res['value'].has_key('pricelist_id'):
            del res['value']['pricelist_id']
        return res

    def default_get(self, cr, uid, fields, context=None):
        res = super(account_a_account, self).default_get(
            cr, uid, fields, context=context)
        return res

    def _interval_type(self, interval_type, recurring_interval):
        if not interval_type:
            interval_type = 'yearly'
        if interval_type == 'daily':
            return relativedelta(days=recurring_interval)
        elif interval_type == 'weekly':
            return relativedelta(weeks=recurring_interval)
        elif interval_type == 'monthly':
            return relativedelta(months=recurring_interval)
        elif interval_type == 'yearly':
            return relativedelta(years=recurring_interval)
        else:
            raise osv.except_osv(
                _('Wrong interval type'), _("Wrong interal type"))

    def onchange_recurring_invoices(self, cr, uid, ids, recurring_invoices, date_start=False, recurring_interval=1, interval_type=False, days_before=42, context=None):
        value = {}
        if date_start and recurring_invoices:
            try:
                start_date = datetime.datetime.strptime(date_start, "%Y-%m-%d")
                next_date = start_date + \
                    self._interval_type(interval_type, recurring_interval)
                corrected_next_date = next_date - \
                    relativedelta(days=days_before)
            except:
                raise osv.except_osv(
                    _('Please fill Date Start!'), _("No Date Start!"))
            value = {
                'value': {'recurring_next_date': corrected_next_date.strftime('%Y-%m-%d')}}
        return value

    @api.multi
    @api.onchange('recurring_invoice_line_ids')
    def _get_downloads(self):
        product_obj = self.env['product.product']
        self.file_ids = []
        new_downloads = []
        product_ids = {
            line.product_id.id for line in self.recurring_invoice_line_ids}
        for product_id in product_ids:
            for file in product_obj.browse(product_id).file_ids:
                new_downloads.append((4, file.id))
        self.file_ids = new_downloads

    def _recurring_create_invoice(self, cr, uid, ids, automatic=False, context=None):
        context = context or {}
        invoice_ids = []
        current_date = time.strftime('%Y-%m-%d')
        if ids:
            contract_ids = ids
        else:
            contract_ids = self.search(cr, uid, [('recurring_next_date', '<=', current_date), (
                'state', '=', 'open'), ('recurring_invoices', '=', True), ('type', '=', 'contract')])
        if contract_ids:
            cr.execute(
                'SELECT company_id, array_agg(id) as ids FROM account_analytic_account WHERE id IN %s GROUP BY company_id', (tuple(contract_ids),))
            for company_id, ids in cr.fetchall():
                for contract in self.browse(cr, uid, ids, context=dict(context, company_id=company_id, force_company=company_id)):
                    try:
                        invoice_values = self._prepare_invoice(
                            cr, uid, contract, context=context)
                        invoice_ids.append(
                            self.pool['account.invoice'].create(cr, uid, invoice_values, context=context))
                        next_date = datetime.datetime.strptime(
                            contract.recurring_next_date or current_date, "%Y-%m-%d")
                        interval = contract.recurring_interval
                        if contract.recurring_rule_type == 'daily':
                            new_date = next_date + \
                                relativedelta(days=+interval)
                        elif contract.recurring_rule_type == 'weekly':
                            new_date = next_date + \
                                relativedelta(weeks=+interval)
                        elif contract.recurring_rule_type == 'monthly':
                            new_date = next_date + \
                                relativedelta(months=+interval)
                        else:
                            new_date = next_date + \
                                relativedelta(years=+interval)
                        num_of_invoices = contract.num_of_invoices + 1
                        self.write(cr, uid, [contract.id], {'recurring_next_date': new_date.strftime(
                            '%Y-%m-%d'), 'num_of_invoices': num_of_invoices}, context=context)
                        if automatic:
                            cr.commit()
                    except Exception:
                        if automatic:
                            cr.rollback()
                            _logger.exception(
                                'Fail to create recurring invoice for contract %s', contract.code)
                        else:
                            raise
        return invoice_ids

    def action_contract_send(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        assert len(
            ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(
                cr, uid, 'sale_contractmanagement', 'template_new_contract_info')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'account.analytic.account',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def write_new(self, cr, uid, ids, vals, context=None):
        sale_order_line_obj = self.pool.get('sale.order.line')
        sale_order_obj = self.pool.get('sale.order')
        for sol in sale_order_line_obj.browse(cr, uid, vals['default_sale_order_line']):
            sale_order_line_obj.write(
                cr, uid, sol.id, {'related_contract': (ids[0],)})
            sale_order_obj.write(
                cr, uid, sol.order_id.id, {'project_id': (ids[0],)})
        self.set_open(cr, uid, ids)
        for contract in self.browse(cr, uid, ids):
            if not contract.license_ids:
                self.write(cr, uid, ids, {'license_ids': [(0, 0, {'modification_date': datetime.datetime.strftime(datetime.datetime.now(
                ), tools.DEFAULT_SERVER_DATETIME_FORMAT), 'contract_id': contract.id, 'editable': 'yes', 'partner_id': contract.partner_id.id})]})
            if contract.template_id.name in ['Sold Licence Template', 'Evaluation Licence Template']:
                self.pool.get('res.license')._get_license(
                    cr, uid, [contract.license_ids[0].id], context=context)
                self.write(cr, uid, ids, {
                           'license_ids': [(1, contract.license_ids[0].id, {'editable': 'no'})]})
        return True

    def create(self, cr, uid, vals, context=None):
        vals['state'] = 'open'
        res = super(account_a_account, self).create(
            cr, uid, vals, context=context)
        if vals.get('manager_id', False):
            manager_partner_id = self.pool.get('res.users').browse(
                cr, uid, vals.get('manager_id')).partner_id.id or False
            if manager_partner_id:
                self.write(
                    cr, uid, res, {'message_follower_ids': (manager_partner_id,)})
        return res
