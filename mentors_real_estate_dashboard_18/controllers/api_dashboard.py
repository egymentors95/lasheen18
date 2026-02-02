# -*- coding: utf-8 -*-
##############################################################################
from odoo.http import request,route,Controller

class RealEstateDashboard(Controller):

        @route('/get/project_real_estate/data', auth='user', type='json' , csrf=False)
        def fetch_project_data(self, **kwargs):
            """          
            """        
            company_ids = kwargs.get('company_ids', None)
            project_id= kwargs.get('project_id', None)  
            if not company_ids:
                company_ids = [request.env.user.company_id.id]  
            if not isinstance(company_ids, list):
                company_ids = list(map(int, company_ids))
            env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
            project_ids = env['project.worksite'].sudo().search([('company_id', 'in', company_ids)])
            companies = env['res.company'].sudo().search([('id','in',request.env.user.company_ids.ids)])
            company_list = [{'id': company.id, 'name': company.name} for company in companies]
            projects_list = [{'id': project.id, 'name': project.name.name} for project in project_ids]  
            sold_records = env['product.template'].sudo().search([('project_id_new', 'in', project_id),('is_property', '=', True),('state', '=', 'sold')])
            number_of_properties = env['product.template'].sudo().search([('project_id_new', 'in', project_id),('is_property', '=', True)])
            available_properties = env['product.template'].sudo().search([('project_id_new', 'in', project_id),('is_property', '=', True),('state', '=', 'free')])
            booking_properties = env['product.template'].sudo().search([('project_id_new', 'in', project_id),('is_property', '=', True),('state', '=', 'reserved')])
            lease_properties = env['product.template'].sudo().search([('project_id_new', 'in', project_id),('is_property', '=', True),('state', '=', 'on_lease')])
            AccountMove = env['account.move'].search([('company_id', 'in', company_ids), ('payment_state', '=', 'paid'), ('move_type', '=', 'out_invoice')])
            total_invoice = round(sum(AccountMove.mapped('amount_total')), 2)
            return {
                'sold_records': len(sold_records),
                'projects': projects_list,
                'number_of_properties':len(number_of_properties), 
                'available_properties':len(available_properties), 
                'booking_properties':len(booking_properties), 
                'lease_properties':len(lease_properties), 
                'total_invoice':total_invoice, 
                'projects_count': len(project_ids),                
                'project_ids': project_ids.mapped('id'),
                'companies': company_list 
            }
            