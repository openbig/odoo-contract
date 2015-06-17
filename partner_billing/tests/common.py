# -*- coding: utf-8 -*-

from openerp.tests import common


class TestCommissionCommon(common.TransactionCase):

    def setUp(self):
        super(TestCommissionCommon, self).setUp()

        self.leadObj = self.env['crm.lead']
		self.soObj = self.env['sale.order']
		self.invoiceObj = self.env['account.invoice']
		self.partnerObj = self.env['res.partner']
		self.partnerGradeObj = self.env['res.partner.grade']
		self.makeSaleObj = self.env['crm.make.sale']

		#Creted partner grade "Standard A"
		self.partnerGrade = self.partnerGradeObj.create({
			'name': 'Standard A',
			})

		#Created company 'Company A' -> graded partner
		self.companyA = self.partnerObj.create({
			'name': 'Company A',
			'is_company': True,
			'grade_id': self.partnerGrade,
			'customer': True,
			'supplier': True,
			})

		#Created company 'Company B', ordinary customer

		self.companyB = self.partnerObj.create({
			'name': 'Company B',
			'is_company': True,
			'customer': True,
			})

