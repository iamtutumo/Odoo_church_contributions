from odoo import models, fields, api

class Archdeaconry(models.Model):
    _name = 'church.archdeaconry'
    _description = 'Church Archdeaconry'

    name = fields.Char(string='Name', required=True)
    region = fields.Char(string='Region')
    description = fields.Text(string='Description')
    gps_coordinates = fields.Char(string='GPS Coordinates')
    
    diocese_id = fields.Many2one('church.diocese', string='Diocese', required=True)
    parish_ids = fields.One2many('church.parish', 'archdeaconry_id', string='Parishes')
    
    total_contributions = fields.Float(string='Total Contributions', compute='_compute_total_contributions')
    
    @api.depends('parish_ids.total_contributions')
    def _compute_total_contributions(self):
        for archdeaconry in self:
            archdeaconry.total_contributions = sum(archdeaconry.parish_ids.mapped('total_contributions'))