# -*- encoding: utf-8 -*-
##############################################################################
#
#    portal_customer
#    (C) 2015 big-consulting GmbH
#    (C) 2015 OpenGlobe
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
{
    "name": "Portal Customization for Customers",
    "version": "0.01 (8.0)",
    "author": "openbig.org",
    "website": "http://www.openbig.org",
    "category": "CRM",
    "description": """ This module introduces portal customization for customers. Throught the portal, customers can:\n *view their quotations, sale orders and invoices""",
    "depends": [
        'project_sla',
        'sale_contractmanagement',
        'portal_sale',
        'web_kanban',
        'crm_partner_assign',
        'product_digital_media',
    ],
    "demo_xml": [],
    "data": [
        'account_analytic_account_view.xml',
        'security/ir.model.access.csv',
        'security/portal_security.xml',
        'views/contract_view.xml',
    ],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
