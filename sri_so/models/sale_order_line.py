from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sri_total = fields.Float(string='SRI Total', compute='_compute_sri_total', store=True)
    piece_price = fields.Float(string='Piece Price', compute='_compute_piece_price', store=True)

    @api.depends('product_template_id')
    def _compute_piece_price(self):
        for line in self:
            line.piece_price = 0.0
            if line.product_template_id:
                for bom in line.product_template_id.bom_ids:
                    if bom.type == 'phantom' and bom.bom_line_ids:
                        bom_line = bom.bom_line_ids[0]
                        if bom_line.parent_product_tmpl_id == line.product_template_id:
                            line.piece_price = bom_line.product_id.product_tmpl_id.list_price

    @api.depends('product_template_id')
    def _compute_sri_total(self):
        for line in self:
            if line.product_template_id:
                for bom in line.product_template_id.bom_ids:
                    if bom.type == 'phantom':
                        quantity = sum(bom.bom_line_ids.mapped('product_qty'))
                        line.sri_total = quantity

    # def _prepare_invoice_line(self, **optional_values):
    #     res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
    #     res.update({
    #         'sri_total': self.sri_total if self.sri_total else 0.0,
    #         'piece_price': self.piece_price if self.piece_price else 0.0,
    #     })
    #     return res