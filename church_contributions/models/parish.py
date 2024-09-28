from odoo import models, fields, api

class Parish(models.Model):
    _name = 'church.parish'
    _description = 'Church Parish'

    name = fields.Char(string='Name', required=True)
    region = fields.Char(string='Region')
    description = fields.Text(string='Description')
    gps_coordinates = fields.Char(string='GPS Coordinates')
    
    archdeaconry_id = fields.Many2one('church.archdeaconry', string='Archdeaconry', required=True)
    subparish_ids = fields.One2many('church.subparish', 'parish_id', string='Sub-Parishes')
    
    total_contributions = fields.Float(string='Total Contributions', compute='_compute_total_contributions')
    
    @api.depends('subparish_ids.total_contributions')
    def _compute_total_contributions(self):
        for parish in self:
            parish.total_contributions = sum(parish.subparish_ids.mapped('total_contributions'))