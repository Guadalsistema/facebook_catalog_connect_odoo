# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class FacebookConnectProductTemplate(models.Model):
    _inherit = 'product.template'

    available_in_facebook = fields.Boolean(default=False, help="Available to Facebook catalog.")
