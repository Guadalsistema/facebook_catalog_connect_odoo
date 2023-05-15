# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from odoo.addons.website.tools import MockRequest
from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install')
class TestFacebookConnectFeed(HttpCase):
    def test_get_pricelist_available_multi_company(self):
        ''' Test that the `property_product_pricelist` of `res.partner` is not
            computed as SUPERUSER_ID.
            Indeed, `property_product_pricelist` is a _compute that ends up
            doing a search on `product.pricelist` that woule bypass the
            pricelist multi-company `ir.rule`. Then it would return pricelists
            from another company and the code would raise an access error when
            reading that `property_product_pricelist`.
        '''
        test_company = self.env['res.company'].create({'name': 'Test Company'})
        self.env['product.pricelist'].create({
            'name': 'Backend Pricelist For "Test Company"',
            'website_id': False,
            'company_id': test_company.id,
            'sequence': 1,
        })

        r = self.url_open('/shop')
        self.assertEqual(r.status_code, 200, "The page should not raise an access error because of reading pricelists from other companies")

