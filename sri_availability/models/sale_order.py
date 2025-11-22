from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """
        Override the action_confirm method to set is_sale_order to True
        when confirming a sale order.
        """
        res = super(SaleOrder, self).action_confirm()
        for picking in self.picking_ids:
            picking.is_sale_order = True
            for line in self.order_line:
                picking.mo_calculation_ids.create({
                    'stock_picking_id': picking.id,
                    'sri_product_id': line.product_id.id,
                    'sri_product_templ_id': line.product_id.product_tmpl_id.id,
                    'sri_demand': line.product_uom_qty,
                })




        return res