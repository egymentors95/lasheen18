from odoo import models, fields, api

class worksiteType(models.Model):
    _name = 'worksite.type'
    _description = 'worksite type'

    
    name = fields.Char(string="Project Name", required=True)