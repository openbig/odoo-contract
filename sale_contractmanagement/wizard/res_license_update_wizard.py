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
from openerp import SUPERUSER_ID
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.translate import _

import logging

logger = logging.getLogger(__name__)


class res_license_update_line(osv.osv_memory):
	_name = "res.license.update.line"
	_columns = {
		'wizard_id': fields.many2one('res.license.update.wizard','Wizard'),
		'license_id': fields.many2one('res.license','License'),
		'modification_date': fields.date('Last Modification Date', readonly=True),
		'olddb_name': fields.char('Previous Database Name', readonly=True),
		'newdb_name': fields.char('New Database Name'),
	}

class res_license_update_wizard(osv.osv_memory):
    _name = "res.license.update.wizard"
    _columns = {
    	'license_ids': fields.one2many('res.license.update.line', 'wizard_id', 'Licenses'),
    }

    def default_get(self, cr, uid, fields, context):
    	res = {'license_ids':[]}
    	acc_analytic_obj = self.pool.get('account.analytic.account')
    	for license in acc_analytic_obj.browse(cr, uid, context.get('active_ids'), context)[0].license_ids:
    		if license.editable == 'yes':
	    		res['license_ids'].append({
	    			'modification_date': license.modification_date,
	    			'olddb_name': license.database_name or '',
	    			'newdb_name': '',
	    			'license_id': license.id,
	    			})
    	return res

    def generate_new(self, cr, uid, ids, context):
    	license_obj = self.pool.get('res.license')
    	for wizard in self.browse(cr, uid, ids, context):
    		for update in wizard.license_ids:
    			#if not update.newdb_name:
    			#	raise osv.except_osv(_('Error!'), _('You have not defined new database names for every license!'))
    			vals = {
    				'database_name': update.newdb_name,
    				'modification_date': time.strftime(DEFAULT_SERVER_DATE_FORMAT),
    				'editable': 'no',
    			}
    			license_obj.write(cr, SUPERUSER_ID, update.license_id.id, vals,context)
    			license_obj._get_license(cr, SUPERUSER_ID, update.license_id.id, context)

    	return True