# -*- coding: utf-8 -*-
# (C) 2025 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com

from odoo import fields, models, api

class MultipleManufacturingOrders(models.Model):
    _name = 'multiple.manufacturing.orders'
    _description = "Multiple Manufacturing Orders"

    name = fields.Char('Name', readonly=True)
    product_id = fields.Many2one(comodel_name='product.template', string="Product")
    quantity = fields.Float(string="Quantity", digits='Product Unit of Measure')
    line_multiple_manufacturing_orders_ids = fields.One2many('line.multiple.manufacturing.orders',
                                                             'multiple_manufacturing_orders_id',
                                                             'Lines Multiple Manufacturing Orders')
    state = fields.Selection([
        ('to_draft', 'To draft'),
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], string='State', copy=False, index=True, readonly=True, default='to_draft',
        store=True, tracking=True,
        help=" * Draft: The MO is not confirmed yet.\n"
             " * Confirmed: The MO is confirmed, the stock rules and the reordering of the components are trigerred.\n"
             " * Done: The MO is closed, the stock moves are posted.")
    state_screen = fields.Selection([
        ('new', 'New'),
        ('created', 'Created'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('aborted', 'Aborted')], string='Screen Status', copy=False, index=True, readonly=True, default='new',
        store=True, tracking=True)
    account_mrp_production_ids = fields.Integer(string='Manufacturing Orders',
                                                compute='_compute_account_mrp_production_ids')
    is_action_refresh_calcultaing = fields.Boolean(string="Action Refresh Calcultaing", default=False)

    @api.depends('product_id')
    def _compute_line_multiple_manufacturing_orders_ids(self):
        for m_m_o_id in self:
            m_m_o_id.line_multiple_manufacturing_orders_ids.unlink()
            for l_m_m_o_id in m_m_o_id.product_id.product_variant_ids:
                l_m_m_o_values = {'quantity': 0, 'product_id': l_m_m_o_id.id,
                                  'multiple_manufacturing_orders_id': m_m_o_id.id}
                self.env['line.multiple.manufacturing.orders'].sudo().create(l_m_m_o_values)
            m_m_o_id.line_multiple_manufacturing_orders_ids = [(6, 0, self.line_multiple_manufacturing_orders_ids.ids)]

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for m_m_o_id in self:
            m_m_o_id.line_multiple_manufacturing_orders_ids.unlink()
            for l_m_m_o_id in m_m_o_id.product_id.product_variant_ids:
                l_m_m_o_values = {'quantity': 0, 'product_id': l_m_m_o_id.id,
                                  'multiple_manufacturing_orders_id': m_m_o_id.id}
                self.env['line.multiple.manufacturing.orders'].sudo().create(l_m_m_o_values)
            m_m_o_id.line_multiple_manufacturing_orders_ids = [(6, 0, self.line_multiple_manufacturing_orders_ids.ids)]

    @api.onchange('quantity')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        for l_m_m_o_id in self.line_multiple_manufacturing_orders_ids:
            l_m_m_o_id.quantity = self.quantity / len(self.line_multiple_manufacturing_orders_ids)

    @api.onchange('line_multiple_manufacturing_orders_ids')
    def _onchange_line_multiple_manufacturing_orders_ids(self):
        if not self.product_id:
            return
        self.is_action_refresh_calcultaing = False

    def action_creation(self):
        for l_m_m_o_id in self.line_multiple_manufacturing_orders_ids:
            self.env['mrp.production'].create({'product_id': l_m_m_o_id.product_id.id,
                                               'product_qty': l_m_m_o_id.quantity,
                                               'multiple_manufacturing_orders_id': self.id})
        self.write({'state_screen': 'created', 'state': 'draft'})

    def action_confirm(self):
        mrp_production_ids = self.env['mrp.production'].search([('multiple_manufacturing_orders_id', '=', self.id),
                                                                ('state', '=', 'draft')])
        if not mrp_production_ids:
            return
        for m_p_id in mrp_production_ids:
            m_p_id.action_confirm()
        self.write({'state_screen': 'in_progress', 'state': 'confirmed'})

    def button_mark_done(self):
        mrp_production_ids = self.env['mrp.production'].search([('multiple_manufacturing_orders_id', '=', self.id),
                                                                ('state', '=', 'confirmed')])
        if not mrp_production_ids:
            return
        for m_p_id in mrp_production_ids:
            m_p_id.button_mark_done()
        self.write({'state_screen': 'completed', 'state': 'done'})

    def _compute_account_mrp_production_ids(self):
        for m_m_o in self:
            mrp_production_ids = self.env['mrp.production'].search(
                [('multiple_manufacturing_orders_id', '=', m_m_o.id)])
            m_m_o.account_mrp_production_ids = len(mrp_production_ids) if mrp_production_ids else 0

    def action_open_multiple_manufacturing_orders_mrp_production(self):
        return {
            'name': 'Manufacturing Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'mrp.production',
            'domain': [('multiple_manufacturing_orders_id', '=', self.id)],
            'target': 'current'
        }

    @api.model_create_multi
    def create(self, vals):
        res = super(MultipleManufacturingOrders, self).create(vals)
        for m_m_o_id in res:
            m_m_o_id.name = self.env['ir.sequence'].next_by_code('multiple.manufacturing.orders.sequence.code') or '/'
        return res

    def action_cancel(self):
        mrp_production_ids = self.env['mrp.production'].search([('multiple_manufacturing_orders_id', '=', self.id),
                                                                ('state', '!=', 'done')])
        if not mrp_production_ids:
            return
        for m_p_id in mrp_production_ids:
            m_p_id.action_cancel()
        self.write({'state_screen': 'aborted', 'state': 'cancel'})

    def action_refresh_calcultaing(self):
        total_quantity = sum(line.quantity for line in self.line_multiple_manufacturing_orders_ids)
        self.quantity = total_quantity
        self.is_action_refresh_calcultaing = False
