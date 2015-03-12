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

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import email_split
from openerp import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class wizard_user(osv.osv_memory):
    _inherit = 'portal.wizard.user'
    _columns = {
        'company': fields.char('Company'),
        'portal': fields.char('Portal'),
        'welcome_message': fields.char('Welcome Messsage'),
        'db': fields.char('Database'),
        'user_name': fields.char('User Name'),
        'login': fields.char('Login'),
        'signup_url': fields.char('Signup URL'),
        'portal_url': fields.char('Portal URL'),
        'user_from': fields.many2one('res.users', "Addressing User"),
        'user_to': fields.many2one('res.users','Receiveing User')
    }

    def _send_email(self, cr, uid, wizard_user, context=None):
        """ send notification email to a new portal user
                @param wizard_user: browse record of model portal.wizard.user
                @return: the id of the created mail.mail record
        """
        res_partner = self.pool['res.partner']
        templates_obj = self.pool.get('email.template')
        this_context = context
        this_user = self.pool.get('res.users').browse(
            cr, SUPERUSER_ID, uid, context)
        if not this_user.email:
            raise osv.except_osv(_('Email Required'),
                                 _('You must have an email address in your User Preferences to send emails.'))

        # determine subject and body in the portal user's language
        user = self._retrieve_user(cr, SUPERUSER_ID, wizard_user, context)
        context = dict(this_context or {}, lang=user.lang)
        ctx_portal_url = dict(context, signup_force_type_in_url='')
        portal_url = res_partner._get_signup_url_for_action(cr, uid,
                                                            [user.partner_id.id],
                                                            context=ctx_portal_url)[user.partner_id.id]
        res_partner.signup_prepare(cr, uid, [user.partner_id.id], context=context)

        vals = {
        	'user_from': this_user.id,
        	'user_to': user.id,
            'company': this_user.company_id.name,
            'portal': wizard_user.wizard_id.portal_id.name,
            'welcome_message': wizard_user.wizard_id.welcome_message or "",
            'db': cr.dbname,
            'user_name': user.name,
            'login': user.login,
            'signup_url': user.signup_url,
            'portal_url': portal_url,
        }

        self.write(cr, uid, wizard_user.id, vals, context=None)

        templateid = templates_obj.search(
            cr, uid, [('name', '=', 'Portal Invitation')])
        try:
            template = templates_obj.browse(cr, uid, templateid)[0]
        except IndexError:
            raise osv.except_osv(_('Template not found!'),
                                 _('''Cannot find template for portal user invitations! The templates' name has to be = Portal Invitation  '''))
        _logger.warn('write here ')
        _logger.warn(locals())    
        return templates_obj.send_mail(cr, SUPERUSER_ID, template.id, wizard_user.id, force_send=True)
