# -*- encoding: utf-8 -*-
##############################################################################
#
#    contractmanagement_licenses
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
{
    "name": "Modules And Application Views",
    "version": "0.01 (8.0)",
    "author": "openbig.org",
    "website": "http://www.openbig.org",
    "category": "CRM, Project, Sale",
    "description": """This module adds list views.""",
    "depends": [
                "account_analytic_analysis",
                "sale",
                "contractmanagement_licencetypes",
    ],
    "demo_xml": [],
    "data": [
        'sale_config_view.xml',
        'contract_view.xml',
        "security/ir.model.access.csv",
    ],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
