# -*- encoding: utf-8 -*-
##############################################################################
#
#    crm_contractamangement
#    (C) 2015 big-consulting GmbH
#    (C) 2015 OpenGlobe
#    Author: Thorsten Vocks (openBIG.org)
#    Author: Mikołaj Dziurzyński (OpenGlobe)
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

from openerp import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class res_parnter(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _customer_contracts(self):
        for partner in self:
            family = self.search([('parent_id', 'child_of', partner.id)])
            _logger.warn(partner.name)
            _logger.warn(family)
            res = len(self.env['account.analytic.account'].search(
                [['partner_id', 'in', [x.id for x in family]], ['type', '=', 'contract'],
                 ['template_id', '!=', False]]))
            _logger.warn(res)
            partner.contracts = res

    contracts = fields.Integer(
        compute="_customer_contracts", string='Contracts')
