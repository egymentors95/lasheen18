from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_sale_order = fields.Boolean(
        string='is Sale Order',
        default=False,
    )
    mo_calculation_ids = fields.One2many(comodel_name='mo.calculation',
                                         inverse_name='stock_picking_id',
                                         string='MO Calculations',
                                         help='Related MO calculations for the stock picking')



    # def sri_calculation(self):
    #     for picking in self:
    #         for rec in picking.mo_calculation_ids:
    #             if not rec.sri_product_templ_id:
    #                 rec.sri_quantity = 0
    #                 continue
    #
    #             ratios = []
    #
    #             for bom in rec.sri_product_templ_id.bom_ids:
    #                 for line in bom.bom_line_ids:
    #                     component_product = line.product_id
    #                     bom_qty = line.product_qty
    #
    #                     matching_moves = picking.move_ids_without_package.filtered(
    #                         lambda m: m.product_id == component_product
    #                     )
    #                     move_qty = sum(matching_moves.mapped('quantity'))
    #
    #                     if bom_qty > 0:
    #                         ratio = move_qty / bom_qty
    #                         ratios.append(ratio)
    #                         print(f"Ratios for......11111111111.......: {ratios}")
    #             print(f"Ratios for.............: {ratios}")
    #
    #             rec.sri_quantity = int(min(ratios)) if ratios else 0

