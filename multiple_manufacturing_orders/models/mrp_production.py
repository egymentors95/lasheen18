# -*- coding: utf-8 -*-
# (C) 2024 EL MEKKAOUI BRAHIM : elmekkaoui.brahim@gmail.com

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    multiple_manufacturing_orders_id = fields.Many2one('multiple.manufacturing.orders', string='Multiple Manufacturing Orders')