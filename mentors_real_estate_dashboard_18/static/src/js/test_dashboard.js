/** @odoo-module */
import {registry} from  '@web/core/registry'
const {Component, useState, onWillStart, onMounted} = owl  
import { rpc } from "@web/core/network/rpc";  
import {useService} from "@web/core/utils/hooks";
export class ProjectDashboard extends Component{ 
        static props = {
            action: { type: Object, optional: true },
            actionId: { type: Number, optional: true },
            updateActionState: { type: Function, optional: true },
            className: { type: String, optional: true },
            globalState: { type: Object, optional: true }  
        };
    setup(){  
        this.action = useService("action"); 
        this.project_state = useState({
            companies: [
                { id: 1, name: "mohamed " },
                { id: 2, name: "elahmady  " },
                { id: 3, name: "ali " },
            ], 
            projects: [], 
            selected_projects: [], 
            number_of_properties: 0,        
            available_properties: 0,        
            booking_properties: 0,        
            lease_properties: 0,    
            total_invoice: 0,    
            selected_companies: [], 
   
        
        });

        onWillStart(async () => { 
            await this.fetchDataProject();
        });
        onMounted(async () => { 
            await this.render_projects_hours();
            await this.ahmady_test();
          
        }); 
    }
 
    fetchDataProject(company_ids = [], projectId =[]) {
        console.log("Fetching data for companies:", company_ids, "and project:", projectId);  
        rpc("/get/project_real_estate/data", { company_ids: company_ids ,project_id: projectId}).then((data_result) => {  
                if (!data_result || !data_result.companies) {
                    console.error("No companies returned from server.");
                    return;
                }
                this.project_state.companies = data_result.companies;
                this.project_state.projects = data_result.projects|| [];  
                this.project_state.sold_records = data_result.sold_records || 0;  
                this.project_state.number_of_properties = data_result.number_of_properties || 0;  
                this.project_state.available_properties = data_result.available_properties || 0;  
                this.project_state.booking_properties = data_result.booking_properties || 0;  
                this.project_state.lease_properties = data_result.lease_properties || 0;  
                this.project_state.total_invoice = (data_result.total_invoice || 0).toLocaleString();
                this.render_projects_hours();
                this.ahmady_test();
            })
            .catch((error) => {
                console.error("Error in fetchDataProject:", error);
            });
    }
    _onCompanyCheckboxChange(event) {
        const checkbox = event.target;
        const companyId = parseInt(checkbox.value);
    
        if (checkbox.checked) {
            if (!this.project_state.selected_companies.includes(companyId)) {
                this.project_state.selected_companies.push(companyId);
            }
        } 
        else {
            this.project_state.selected_companies = this.project_state.selected_companies.filter(id => id !== companyId);
        }
    
        this.fetchDataProject(this.project_state.selected_companies);
    }
    _onProjectCheckboxChange(event) {
        const checkbox = event.target;
        const projectId = parseInt(checkbox.value);
    
  
        if (!this.project_state.selected_projects) {
            this.project_state.selected_projects = [];
        }
    
        if (checkbox.checked) {
        
            if (!this.project_state.selected_projects.includes(projectId)) {
                this.project_state.selected_projects.push(projectId);
            }
        } else {
     
            this.project_state.selected_projects = this.project_state.selected_projects.filter(
                (id) => id !== projectId
            );
        }
    
   
        this.fetchDataProject(this.project_state.selected_companies, this.project_state.selected_projects);
    }
      
    _onClick_create_region(){ 
            this.action.doAction({
                name : ("region"),
                type: 'ir.actions.act_window',
                res_model:'regions',
                view_mode:'form',
                views:[[false, 'form' ]], 
                target :'current'
            }, ) } 
     _onClick_create_project(){ 
        this.action.doAction({
            name : ("project"),
            type: 'ir.actions.act_window',
            res_model:'project.worksite',
            view_mode:'form',
            views:[[false, 'form' ]], 
            target :'current'
        }, ) } 
     _onClick_create_block(){ 
        this.action.doAction({
            name : ("block"),
            type: 'ir.actions.act_window',
            res_model:'building',
            view_mode:'form',
            views:[[false, 'form' ]], 
            target :'current'
        }, ) } 
     _onClick_create_booking(){ 
        this.action.doAction({
            name : ("Booking"),
            type: 'ir.actions.act_window',
            res_model:'unit.reservation',
            view_mode:'form',
            views:[[false, 'form' ]], 
            target :'current'
        }, ) } 
     _onClick_create_contract(){ 
        this.action.doAction({
            name : ("ownership contract"),
            type: 'ir.actions.act_window',
            res_model:'ownership.contract',
            view_mode:'form',
            views:[[false, 'form' ]], 
            target :'current'
        }, ) } 
        render_projects_hours() {
            var self = this;
            var ctx = $('.project_hours')[0];  
            if (!ctx) {
                console.error("Canvas element not found.");
                return;
            }
            if (self.projectHoursChart) {
                self.projectHoursChart.destroy();
                self.projectHoursChart = null;  
            }
            var data = {
                labels: ['Available Properties', 'Booking Properties', 'Sold Properties','Lease Properties'],
                datasets: [
                    {
                        label: "Dataset",
                        data: [this.project_state.available_properties, this.project_state.booking_properties, this.project_state.sold_records,this.project_state.lease_properties],
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)',
                            'rgb(95, 95, 93)'
                        ],
                        hoverOffset: 4
                    }
                ]
            };
            self.projectHoursChart = new Chart(ctx.getContext('2d'), {
                type: 'doughnut',
                data: data,
            });
        }
        ahmady_test() {
            var canvas = document.querySelector('.project_count_per_emp');
            if (!canvas) {
                console.error("Canvas element not found in the DOM.");
                return;
            }
            canvas.style.width = '100%';
            canvas.style.height = '400px';  
            var ctx = canvas.getContext('2d');
            if (this.chartInstance) {
                this.chartInstance.destroy();  
                this.chartInstance = null;  
            }
            var data = {
                labels: ['Available Properties', 'Booking Properties', 'Sold Properties'],
                datasets: [{
                    label: 'Projects',
                    data: [this.project_state.available_properties, this.project_state.booking_properties, this.project_state.sold_records],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.4)',
                        'rgba(54, 162, 235, 0.4)',
                        'rgba(255, 205, 86, 0.4)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            };
            this.chartInstance = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,  
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Projects by Status'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        _onSelectAllChange(ev) {
            const isChecked = ev.target.checked;
            const checkboxes = document.querySelectorAll('.project-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = isChecked; 
            });
        }
} 
ProjectDashboard.template ="template_name_real_estate_ProjectDashBoardMain"
registry.category("actions").add("tag_real_estate_dashboard_main", ProjectDashboard)  


