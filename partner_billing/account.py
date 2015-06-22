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
from openerp.tools.translate import _
from openerp import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class account_invoice(models.Model):
    _inherit = "account.invoice"
    associated_partner = fields.Many2one('res.partner', "Associated Partner", domain=[(
        'grade_id', '!=', False)], help="Partner/Reseller who reported this lead. Important for commission invoices.")
    commission_type = fields.Selection([('commission_invoice', 'Commission Invoice'), (
        'commission_refund', 'Commission Refund'), ('not_commission', 'Not Commission')], default='not_commission')
    origin_invoice = fields.Many2one(comodel_name='account.invoice',string='Invoice of Origin', help="Invoice, which reconcilliation triggered creation of this invoice.")
#    commission_invoice = fields.Many2many(comodel_name='account.invoice',relation="account_invoice_commission_rel",column1="commission_invoice_id",column2="origin_invoice_id",string='Commission Invoice', help="Commission invoice created when this invoice got paid.")

    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        res = super(account_invoice, self)._prepare_refund(invoice, date=date, period_id=period_id, description=description, journal_id=journal_id)
        if 'journal_id' in res:
        	journal = self.env['account.journal'].browse(journal_id)
        	if journal.name == "Commission Refund Journal":
        		_logger.warn("refund prepare")
        		res.update({'commission_type':'commission_refund'})
        return res

    @api.multi
    def do_merge(self, keep_references=True):
        res = super(account_invoice, self).do_merge(keep_references=keep_references)
        if res:
            merged_ids = res.keys()
            for merged in merged_ids:
                merged_invoice = self.browse(merged)
                for invoice in self.browse(res[merged]):
                    if invoice.commission_type == 'commission_invoice':
                        merged_invoice.write({'commission_type': 'commission_invoice'})
                    elif invoice.commission_type == 'commission_refund':
                        merged_invoice.write({'commission_type': 'commission_refund'})
                    else:
                        continue
        return res


    @api.multi
    def onchange_journal_id(self, journal_id=False):
        res = super(account_invoice, self).onchange_journal_id(journal_id)
        if journal_id:
            journal = self.env['account.journal'].browse(journal_id)
            if journal.name == 'Commission Journal':
                res['value']['commission_type'] = 'commission_invoice'
            elif journal.name == 'Commission Refund Journal':
                res['value']['commission_type'] = 'commission_refund'
            else:
                res['value']['commission_type'] = 'not_commission'
        return res

    @api.multi
    def create_commission_invoice(self):
        if not self.associated_partner:
            return True
        if not self.associated_partner.grade_id.commission_pricelist:
            raise osv.except_osv(_('Missing Values Error!'),_("Assigned partner has no commission pricelist defined! Please go to assigned partners' grade and assign a commission pricelist!"))
        for invoice in self:
            commission_journal = self.env['account.journal'].search([['name','=','Commission Journal']])
            invoice_vals = {
                'partner_id': self.associated_partner.id,
                'journal_id': commission_journal.id,
                'origin_invoice': self.id,
                'origin': self.origin,
                'type': 'in_invoice',
                'commission_type': 'commission_invoice',
                'invoice_line': [],
            }
            invoice_vals.update(self.onchange_partner_id('in_invoice',self.associated_partner.id)['value'])
            for line in self.invoice_line:
                line_vals = {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                }
                line_vals.update(self.env['account.invoice.line'].product_id_change(line.product_id.id,line.product_id.uom_id.id, qty=line.quantity,type='in_invoice',partner_id=self.associated_partner.id)['value'])
                temp_self = self
                pricelist_id = self.associated_partner.grade_id.commission_pricelist.id
                self = self.associated_partner.grade_id.commission_pricelist
                line_vals['price_unit'] = self.env['product.pricelist'].price_get(line_vals['product_id'], line.quantity, invoice_vals['partner_id'])[pricelist_id]
                self = temp_self
                line_vals['name'] = _("Commission")
                _logger.warn(line_vals)
                invoice_vals['invoice_line'].append((0,0,line_vals))
            commission_invoice = self.create(invoice_vals)
#            self.write({'commission_invoice':[(4,commission_invoice)]})
        return True