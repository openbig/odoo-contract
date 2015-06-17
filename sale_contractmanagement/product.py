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


class product_template(osv.osv):
    _inherit = 'product.template'
    _columns = {
        'sla_related': fields.boolean('Service Level Agreement'),
        'sla': fields.many2one('project.sla', 'Related SLA'),
    }
