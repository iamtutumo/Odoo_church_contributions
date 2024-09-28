from odoo import models, fields, api

class Diocese(models.Model):
    _name = 'church.diocese'
    _description = 'Church Diocese'

    name = fields.Char(string='Name', required=True)
    region = fields.Char(string='Region')
    description = fields.Text(string='Description')
    gps_coordinates = fields.Char(string='GPS Coordinates')
    
    archdeaconry_ids = fields.One2many('church.archdeaconry', 'diocese_id', string='Archdeaconries')
    
    total_contributions = fields.Float(string='Total Contributions', compute='_compute_total_contributions')
    
    @api.depends('archdeaconry_ids.total_contributions')
    def _compute_total_contributions(self):
        for diocese in self:
            diocese.total_contributions = sum(diocese.archdeaconry_ids.mapped('total_contributions'))