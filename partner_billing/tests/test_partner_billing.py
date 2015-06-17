# -*- coding: utf-8 -*-

from openerp.addons.partner_billing.tests.common import TestCommissionCommon
from openerp import api


class TestCommissionFlow(TestCommissionCommon):

    def test_01_associated_partner_passing(self):
        """ Basic test checking if associated partner assigned on crm.lead \
        object is passed to \invoice object."""

        lead = self.leadObj.create(
            {'name': 'test lead 1',
             'associated_partner': self.companyA,
             'partner_id': self.companyB,
             })

        self.leadObj.convert_opportunity(self.companyB)
        opp2quotWizard = self.makeSaleObj.create({
            'partner_id': self.companyB,
            'close': True,
        })
        self.makeSaleObj.makeOrder()
