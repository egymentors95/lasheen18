# -*- coding: utf-8 -*-
# (C) 2026 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com

from odoo import models, fields, api

class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'

    dirtcly_product_line = fields.Boolean("Dirtcly on Product Line")

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_list = super(LoyaltyReward, self)._load_pos_data_fields(config_id)
        fields_list.append('dirtcly_product_line')
        return fields_list
