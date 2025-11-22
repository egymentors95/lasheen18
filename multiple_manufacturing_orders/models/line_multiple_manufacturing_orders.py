# -*- coding: utf-8 -*-
# (C) 2025 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com

from odoo import fields, models

class LineMultipleManufacturingOrders(models.Model):
    _name = 'line.multiple.manufacturing.orders'
    _description = "Line Multiple Manufacturing Orders"

    product_id = fields.Many2one(comodel_name='product.product', string="Product")
    quantity = fields.Float(string="Quantity", digits='Product Unit of Measure')
    multiple_manufacturing_orders_id = fields.Many2one('multiple.manufacturing.orders', readonly=True,
                                                       string='Multiple Mmanufacturing Orders', ondelete='cascade')

    def write(self, values):
        res = super().write(values)
        if 'quantity' in values:
            self._action_refresh_calcultaing()
        return res

    def _action_refresh_calcultaing(self):
        self.multiple_manufacturing_orders_id.is_action_refresh_calcultaing = True
