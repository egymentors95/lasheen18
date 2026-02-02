from odoo import models, fields,_

class CrmLead(models.Model):
    _inherit = 'crm.lead'
 
    def action_open_block(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'kanban,form',  
            'views': [
                (self.env.ref('itsys_real_estate.building_unit_kanban').id, 'kanban'),
                (self.env.ref('itsys_real_estate.building_unit_form').id, 'form')
            ],  
            'domain': [('is_property', '=', True)],
            'target': 'current',
        }
        
class SaleOrder(models.Model):
    _inherit = 'sale.order'  
    
    
    project_milestone_id= fields.Many2one('project.milestone','Milestone')
    