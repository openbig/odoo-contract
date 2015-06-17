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
{
    "name": "Contracts for Software and Media Sales",
    "version": "0.05 (8.0)",
    "author": "openbig.org",
    "website": "http://www.openbig.org",
    "category": "CRM, Project, Sale",
    "description": """
 Sell products and manage the contract
=====================================

 This module adds some functionality to clean up the 
 usability of contract maintenance. The purpose is to 
 forward sales order lines of licensed or subscribed 
 products to projects to create, apply or extend a 
 contract directly from a task.

 Create tasks from order lines
 -----------------------------

 On confirmation of a sale order line Odoo creates automatically 
 a task in the defined project. This basic functionality from 
 odoo core was extended to forward all required informations 
 to create in a very short time a proper contract. 
 Furthermore it allows a smooth followup process to bill, 
 to distribute license and digital media or to apply SLA 
 terms and conditions.

 Contract Creation
 -----------------

 Contract managers may open generated tasks to create directly 
 from this view a new contract or to assign an existing contract. 
 The automatically assigned contract templates apply product or 
 sale order related data like customer or contract 
 contact / contract ownwer, start and end dates, recurrent 
 billing and reminder options.

 Contracts in sales menu
 ------------------------

 After successfull contract creation they are visible 
 to the salespeople under the sales application menu 
 "Contracts", which is also a Odoo core functionality. 
 From this menu it is also possible to create or to work 
 on existing contracts. This may be the case, if 
 prolongations have to be sold or if salespeople needs 
 informations from the contract, like f.e. license keys 
 files or SLA terms and conditions.

 Extensions
 ==========

By other modules it is possible to extend the modules 
functionality on demand, f.e. by the module product_digital_media. 
It is also possible to apply SLA terms and conditions by the 
module project_sla from Daniel Reis under maintenance of 
the Odoo Community Association.


 Version Vistory
 ===============   

    # version 0.02:
    * when creating a contract, the customer is added to followers of it -> usage with email tab on partner form\n
    # version 0.03:
    * New Contract button is now visible from task form (aside from sale order line form)
    * Only customer related contracts under Contracts menu in sale_service
    * Button allowing to go from project to its analytic account is now only visible to administrator (Settings right)
    # version 0.04:
    * Basic license management functionality
    # version 0.05:
    * Sale Contracts button on partner form

Contributors
============
* Thorsten Vocks (OpenBIG.org)
* Mikołaj Dziurzyński (OpenBIG.org)

    """,
    "depends": [
                "account_analytic_analysis",
                "project_sla",
                "sale_service",
                "product_digital_media",
    ],
    "demo_xml": [],
    "data": [
        'data/email_template.xml',
        'res_config_view.xml',
        'wizard/res_license_update_wizard.xml',
        'res_license.xml',
        'res_partner_view.xml',
        "account_invoice_view.xml",
        "sale_contractmanagement_view.xml",
        "product_view.xml",
        "sale_view.xml",
        'security/ir.model.access.csv',
    ],
    "active": False,
    "license": "AGPL-3",
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
