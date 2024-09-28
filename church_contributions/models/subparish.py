from odoo import models, fields, api

class SubParish(models.Model):
    _name = 'church.subparish'
    _description = 'Church Sub-Parish'

    name = fields.Char(string='Name', required=True)
    region = fields.Char(string='Region')
    description = fields.Text(string='Description')
    gps_coordinates = fields.Char(string='GPS Coordinates')
    
    parish_id = fields.Many2one('church.parish', string='Parish', required=True)
    member_ids = fields.One2many('church.member', 'subparish_id', string='Members')
    
    total_contributions = fields.Float(string='Total Contributions', compute='_compute_total_contributions')
    
    @api.depends('member_ids.total_contributions')
    def _compute_total_contributions(self):
        for subparish in self:
            subparish.total_contributions = sum(subparish.member_ids.mapped('total_contributions'))