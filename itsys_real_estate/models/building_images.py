# -*- coding: utf-8 -*-
##############################################################################
#
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
# from odoo.addons.website.tools import get_video_embed_code
import re

class building_images(models.Model):
    _name = 'building.images'
    _description = "Building Images"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    building_id = fields.Many2one('building', "Building", index=True, ondelete='cascade')
   
    # video_url = fields.Char('Video URL', help='URL of a video for showcasing your property.')
 #ahmady
    project_worksite_id= fields.Many2one('project.worksite', "project", index=True, ondelete='cascade') 


    can_image_1024_be_zoomed = fields.Boolean("Can Image 1024 be zoomed", compute='_compute_can_image_1024_be_zoomed', store=True)

    @api.depends('image_1920', 'image_1024')
    def _compute_can_image_1024_be_zoomed(self):
        for record in self:
            # استخدام خصائص Image بدلاً من is_image_size_above
            record.can_image_1024_be_zoomed = record.image_1920 and (
                (record.image_1920[0] > 1024 or record.image_1920[1] > 768) if record.image_1920 else False
            )

  
  


 