# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductDicsount(models.Model):
    _inherit = "product.product"

    discount = fields.Float(string='Discount in %', compute='_compute_discount', store=True, help="Discount percentage for the product")

    @api.depends('product_tmpl_id.discount')
    def _compute_discount(self):
        for product in self:
            if not product.discount:
                product.discount = product.product_tmpl_id.discount
    
    
    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_list = super(ProductDicsount, self)._load_pos_data_fields(config_id)
        fields_list.append('discount')
        return fields_list

