# -*- encoding: utf-8 -*-
##############################################################################
#
#    partner_billing
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
    "name": "Management of Commissions and Pricelists for Partners",
    "version": "0.01 (8.0)",
    "author": "openbig.org",
    "website": "http://www.openbig.org",
    "category": "CRM, account",
    "description": """
Invoice partner sales and calculate commissions
===============================================
The partner billing module allows to invoice reduced prices based 
on a partner pricelist or to create a commission supplier invoice. 
After payment receipt of the origin invoice paid by the customer 
commission invoices will be created in draft mode at the same time. 

Define new commission Pricelists
--------------------------------

At first you have to define a pricelist used to calculate the 
commissions on payment. This is done by a new pricelist type 
named "partner commission".

Assign pricelists to partner grades
-----------------------------------

You can assign a classic "sale" pricelist and now also a pricelist 
of type "partner commission". For the case an associated partner 
exists finally on an invoice the system generates automatically 
a commission invoice too.

Assign grades to Partners
-------------------------

You can assign grades to partners. By this Odoo core feature 
the system exactlly knows which price to calculate for the 
case of direct billing and it also knows the commission 
percentages.

Associate partner to sale
--------------------------

It is possible to associate the partner on the lead, opportunity, 
sale order or lately on the invoice. This association finally 
controls the commission billing.

Register payment
-----------------

The registration of a payment controls the time when a commission 
invoice will be created by Odoo.

Invoice confirmation or merge
-----------------------------

Finally an accountant have to confirm the invoice in draft mode. 
For sure there can be more than one commission invoice created. 
This depends also from the time frequence you usually want to pay 
the reseller commissions. In that case the wizard to merge 
invoices is very conveniant to use.

Contributors
============
* Mikołaj Dziurzyński (OpenBIG.org)
* Thorsten Vocks (OpenBIG.org)


    """,
    "depends": [
        'account',
        'crm_partner_assign',
        'sale_crm',
        'account_invoice_merge',
    ],
    "demo_xml": [],
    "data": [
        "data/account_data.xml",
        "data/pricelist_type_data.xml",
        "account_view.xml",
        "res_partner_view.xml",
        "crm_lead_view.xml",
        "sale_order_view.xml",
    ],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
