from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    discount = fields.Float(string='Discount in %', help="Discount percentage for the product")

