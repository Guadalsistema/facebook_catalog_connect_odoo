# -*- coding: utf-8 -*-

import logging
import csv
from io import StringIO

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class FacebookCatalogController(http.Controller):

    @http.route('/facebook_catalog_feed', auth='public', method=["GET"], sitemap=False)
    def facebook_catalog_feed(self):
        """ Publish the catalog to be available in the endpoint """
        _logger.info("Facebook catalog feed hitted")
        # Filter products with the necesary info
        product_template_list = request.env["product.template"].search([
            ("active", "=", True),
            ("is_published", "=", True),
            ("sale_ok", "=", True),
            ("available_in_facebook", "=", True),
        ])

        product_list = request.env["product.product"].search([
            ("product_tmpl_id", "in", product_template_list.ids),
            ("active", "=", True),
            '|',
            '|',
            ("product_tmpl_id.image_1920", "!=", False),
            ("image_1920", "!=", False),
        ])

        pricelist = request.website.get_current_pricelist()
        partner = request.env.user.partner_id
        def product_price_tax(product):
            combination_info = product.product_tmpl_id.sudo()._get_combination_info(product_id = product.id)
            taxes = partner.property_account_position_id.map_tax(product.sudo().taxes_id.filtered(lambda x: x.company_id == company_id), product, self.env.user.partner_id)
            return taxes.compute_all(combination_info['price'], pricelist.currency_id, 1, product, partner)['tax_included']

        fc_fields = (
                'item_group_id',  # template
                'id',  # barcode
                'title',  # display_name
                'description',  # description_sale
                'availability',
                'inventory',
                'condition',
                'price',
                'link',
                'image_link',
                'brand'
                )

        # TODO cache
        with StringIO() as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(fc_fields)
            for p in pp:
                csvwriter.writerow((
                    p.product_tmpl_id.default_code,
                    p.barcode,
                    p.display_name,
                    p.description_sale,
                    "on stock" if p.qty_available > 0 else "out of stock",
                    p.qty_available,
                    "new",
                    product_price_tax(p),
                    request.website.url + p.website_url,
                    "",
                    p.product_tmpl_id.brand_id.name or "Guadalstore"
                    ))

            return request.make_response(csv)

        return request.not_found()
