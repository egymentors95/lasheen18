from odoo import models, fields


class ProjectNew(models.Model):
    _name = 'project.worksite'
    _description = 'Project'
    _inherit = ['mail.thread']

    # الحقول الأساسية

    accumulated = fields.Float(string="Accumulated %")
    name = fields.Many2one('project.project', string="Project Name", required=True)
    personal_image = fields.Binary("Personal Image", help="Upload your photo")
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    regions_id = fields.Many2one('regions', string="region")
    # تفاصيل العنوان
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")

    # معلومات الموقع
    date = fields.Date(string="Date")
    owner = fields.Char(string="Owner")
    company_id = fields.Many2one('res.company', string="Company")

    worksite_type = fields.Many2one('worksite.type', string="Project Type")

    # تفاصيل الوحدات والمساحة
    available_units = fields.Float(string="Available Units", readonly=True)
    sold_units = fields.Float(string="Sold Units", readonly=True)
    available_area = fields.Float(string="Available Area", readonly=True)
    sold_area = fields.Float(string="Sold Area", readonly=True)

    #  page Basic Information 
    total_towers = fields.Integer(string="Total No. of Towers")
    floors = fields.Integer(string="Floors #")
    properties_per_floor = fields.Integer(string="Properties per Floor")
    shops = fields.Integer(string="Shops #")

    amenities = fields.Text(string="Amenities")

    # إجمالي المساحة وقيمة المشروع
    total_property_area = fields.Float(string="Total Property Area", readonly=True)
    total_value = fields.Float(string="Total Value of Project", readonly=True)
    total_maintenance_collection = fields.Float(string="Total Maintenance Collection", readonly=True)

    # page مرفقات
    project_floor_plan_image_ids = fields.One2many('floor.plans', 'project_worksite_id', string="Floor Plans",
                                                   copy=True)
    project_image_ids = fields.One2many('building.images', 'project_worksite_id', string="Building Images", copy=True)

    # page project
    parent_id = fields.Many2one('project.worksite', string="parent")
    child_ids = fields.One2many('project.worksite', 'parent_id', string="parent")
    block_ids = fields.One2many('building', 'project_id', string="blocks")
    # page additional information
    license_code = fields.Char(string="License Code")
    license_date = fields.Date(string="License Date")
    license_added = fields.Date(string="Date Added to Notarization")
    license_notarization = fields.Char(string="License Notarization")
    # page  notes
    notes = fields.Text(string="License Notarization")

    # page  address
    address = fields.Char(string="Address")

    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Distribution')

    def create_sup_project(self):
        if self.total_towers > 0:
            for i in range(1, self.total_towers + 1):
                self.create({
                    'parent_id': self.id,
                    'name': self.name.id,
                    'code': f"{self.code or ''} {i}",
                    'company_id': self.company_id.id,
                })

        if self.shops > 0:
            self.create({
                'parent_id': self.id,
                'name': f"shop {self.name.name or ''}",
                'code': str(self.code or ''),
                'company_id': self.company_id.id,
            })

    def edit_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Worksite',
            'res_model': 'project.worksite',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    def delete_action(self):
        self.unlink()

    def open_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Edit Worksite',
            'res_model': 'project.worksite',
            'view_mode': 'kanban,list,form',
            'domain': [('parent_id', '=', self.id)],
            'target': 'current',
        }
