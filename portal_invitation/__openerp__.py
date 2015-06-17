# -*- encoding: utf-8 -*-
##############################################################################
#
#    portal_invitation
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
    "name": "Portal Invitation from Template",
    "version": "0.01 (8.0)",
    "author": "openbig.org",
    "website": "http://www.openbig.org",
    "category": "CRM",
    "description": """
Portal Invitation from temmplate
================================

The module portal_invitation improves the onboarding 
of new portal users. The usability of odoo core module 
was a bit ugly, leading to unclear advises for a new 
portal user. Main improvement was done by fixing the 
email template and the translation related to it. 

Contributors
============
* Thorsten Vocks (OpenBIG.org)
* Mikołaj Dziurzyński (OpenGlobe)
    """,
    "depends": [
        'email_template',
        'portal',
    ],
    "demo_xml": [],
    "data": [
        'data/email_template_data.xml',
        ],
    "active": False,
    "license": "AGPL-3",
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
