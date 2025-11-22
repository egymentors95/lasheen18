from odoo import models, fields, api


class MoCalculation(models.Model):
    _name = 'mo.calculation'
    _description = 'Stock Calculation'

    stock_picking_id = fields.Many2one(comodel_name='stock.picking', string='Stock Picking',
                                       help='Related stock picking for the calculation')

    sri_product_id = fields.Many2one(comodel_name='product.product',
                                     string='SRI Product',
                                     help='Product used for SRI calculation')
    sri_product_templ_id = fields.Many2one(comodel_name='product.template',
                                             string='SRI Product Template',
                                             help='Product template used for SRI calculation')
    sri_demand = fields.Float(string='SRI Demand',
                              help='Demand for SRI calculation')
    sri_quantity = fields.Float(
        string='SRI Quantity',
        help='Calculated quantity for SRI',
        compute='_compute_sri_quantity',
        store=True
    )


    @api.depends('sri_product_templ_id', 'stock_picking_id.move_ids_without_package.quantity', 'stock_picking_id.move_ids_without_package.product_id')
    def _compute_sri_quantity(self):
        for rec in self:
            if not rec.sri_product_templ_id or not rec.stock_picking_id:
                rec.sri_quantity = 0
                continue

            ratios = []

            for bom in rec.sri_product_templ_id.bom_ids:
                for line in bom.bom_line_ids:
                    component_product = line.product_id
                    bom_qty = line.product_qty

                    matching_moves = rec.stock_picking_id.move_ids_without_package.filtered(
                        lambda m: m.product_id == component_product
                    )
                    move_qty = sum(matching_moves.mapped('quantity'))

                    if bom_qty > 0:
                        ratio = move_qty / bom_qty
                        ratios.append(ratio)

            rec.sri_quantity = int(min(ratios)) if ratios else 0














