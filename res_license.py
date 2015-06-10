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
import time
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

import urllib2
import base64
import json
import random

from idoit_license_gen import create
import logging

_logger = logging.getLogger(__name__)


class res_license(osv.Model):
    _name = "res.license"
    _columns = {
        'contract_id': fields.many2one('account.analytic.account', 'license_ids', 'Related Contract'),
        'partner_id': fields.many2one('res.partner', 'Customer'),
        'modification_date': fields.date('Last Modification Date', readonly=True),
        'license_file': fields.binary('License', readonly=True),
        'license_filename': fields.char("License Filename"),
        'database_name': fields.char("License Database", readonly=True),
        'editable': fields.selection([('yes', 'Set Database Name'), ('no', 'Ready')], 'Status', required=True),
    }

    _defaults = {
        'editable': 'yes',
        'license_filename': 'License',
        'modification_date': time.strftime(DEFAULT_SERVER_DATE_FORMAT),
    }

    def _backend_request(self, cr, uid, composed_json, context=None):
        backend_url = self.pool.get('ir.config_parameter').get_param(
            cr, uid, 'backend_address')
        login = self.pool.get('ir.config_parameter').get_param(
            cr, uid, 'license_gen_login')
        password = self.pool.get('ir.config_parameter').get_param(
            cr, uid, 'license_gen_pass')
        if not backend_url or not login or not password:
            raise osv.except_osv(_('Error!'), _(
                'Please contact Customer Support. Cannot connect to license generator, check credentials.'))
        request = urllib2.Request(backend_url)
        base64string = base64.encodestring(
            '%s:%s' % (login, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Content-Type", "application/json; charset=UTF-8")
        request.add_data(json.dumps(composed_json))
        result = urllib2.urlopen(request)
        return result

    def _get_license(self, cr, uid, ids, context=None):
        '''get all necessary contract info, put it into JSON file, send to synetics backend, receive license and save into database'''
        for license in self.browse(cr, uid, ids, context=context):
            json_to_send = {
                "req_id": license.id,
                "request_data": {
                    "contract_data": {
                        "customer_id": license.contract_id.partner_id.id,
                        "date_start": license.contract_id.date_start,
                        "customer_name": license.contract_id.partner_id.name,
                        "db_name": license.database_name,
                    },
                    "product_data": [],
                }
            }
            if license.contract_id.date:
                json_to_send['request_data']['contract_data'][
                    'end_date'] = license.contract_id.date

            for invoice_lines in license.contract_id.recurring_invoice_line_ids:
                for product in invoice_lines.product_id:
                    prod_data = {
                        'product_name': product.name,
                    }
                    if product.is_product_variant:
                        for attribute in product.attribute_value_ids:
                            prod_data[
                                attribute.attribute_id.name] = attribute.name

                    json_to_send['request_data'][
                        'product_data'].append(prod_data)
            res = self._backend_request(cr, uid, json_to_send, context=context)
            res = res.read().decode('utf-8')
            res_dict = json.loads(res)
            if res_dict.get('error', False):
                raise osv.except_osv(_('Error!'), _(
                    'Please contact Customer Support.\n Error: {0}'.format(res_dict['error'])))
            self.write(cr, uid, ids, {'license_file': res_dict[
                       'licence_data'], 'license_filename': res_dict['filename']}, context)
            res2 = create(json_to_send)
            

        return True
