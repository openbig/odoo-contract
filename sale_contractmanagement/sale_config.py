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

logger = logging.getLogger(__name__)


class sale_configuration(osv.TransientModel):
    _inherit = 'sale.config.settings'

    _columns = {
        'backend_address': fields.char('Backend Address'),
        'license_gen_login': fields.char('Login'),
        'license_gen_pass': fields.char('Password'),
    }

    def default_get(self, cr, uid, fields, context=None):
        res = super(sale_configuration, self).default_get(cr, uid, fields, context)
        logger.warn(res)
        res['license_gen_login'] = self.pool.get('ir.config_parameter').get_param(cr, uid, 'license_gen_login')
        res['license_gen_pass'] = self.pool.get('ir.config_parameter').get_param(cr, uid, 'license_gen_pass')
        res['backend_address'] = self.pool.get('ir.config_parameter').get_param(cr, uid, 'backend_address')
        return res


#    def get_license_get_login(self, cr, uid, ids, context=None):
#
#       return {
#            'license_gen_login': self.pool.get('ir.config_parameter').get_param(cr, uid, 'license_gen_login')
#        }
#
#    def get_license_get_pass(self, cr, uid, ids, context=None):
#
#        return {
#            'license_gen_pass': self.pool.get('ir.config_parameter').get_param(cr, uid, 'license_gen_pass')
#        }


    def set_license_login_login(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids)
        config = config and config[0]
        val = '%s' % config.license_gen_login or False
        self.pool.get('ir.config_parameter').set_param(
            cr, uid, 'license_gen_login', val)
        return 'license_gen_login'

    def set_license_login_pass(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids)
        config = config and config[0]
        val = '%s' % config.license_gen_pass or False
        self.pool.get('ir.config_parameter').set_param(
            cr, uid, 'license_gen_pass', val)
        return 'license_gen_pass'

    def set_backend_address(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids)
        config = config and config[0]
        val = '%s' % config.backend_address or False
        self.pool.get('ir.config_parameter').set_param(
            cr, uid, 'backend_address', val)
        return 'backend_address'
