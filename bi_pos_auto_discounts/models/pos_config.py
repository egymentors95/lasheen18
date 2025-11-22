# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PosConfig(models.Model):
	_inherit = 'pos.config'

	allow_automatic_discount = fields.Boolean('Allow Custom Discount')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_allow_automatic_discount = fields.Boolean(related='pos_config_id.allow_automatic_discount', readonly=False)
