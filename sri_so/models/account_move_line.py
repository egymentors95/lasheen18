from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sri_total = fields.Float(string='SRI Total', compute='_compute_sri_total', store=True)
    piece_price = fields.Float(string='Piece Price', compute='_compute_piece_price', store=True)

    @api.depends('product_id')
    def _compute_piece_price(self):
        for line in self:
            line.piece_price = 0.0
            if line.product_id:
                for bom in line.product_id.bom_ids:
                    if bom.type == 'phantom' and bom.bom_line_ids:
                        bom_line = bom.bom_line_ids[0]
                        line.piece_price = bom_line.parent_product_tmpl_id.list_price


    @api.depends('product_id')
    def _compute_sri_total(self):
        for line in self:
            if line.product_id:
                for bom in line.product_id.bom_ids:
                    if bom.type == 'phantom':
                        quantity = sum(bom.bom_line_ids.mapped('product_qty'))
                        line.sri_total = quantity