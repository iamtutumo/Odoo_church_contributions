from odoo import models, fields, api

class Payment(models.Model):
    _name = 'church.payment'
    _description = 'Church Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    member_id = fields.Many2one('church.member', string='Member', required=True)
    payment_date = fields.Date(string='Payment Date', required=True)
    amount = fields.Float(string='Amount', required=True)
    payment_channel = fields.Selection([
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('check', 'Check'),
    ], string='Payment Channel', required=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Payment Status', default='pending', required=True)
    reference_number = fields.Char(string='Reference Number')
    notes = fields.Text(string='Notes')
    access_url = fields.Char('Portal Access URL', compute='_compute_access_url')

    @api.model
    def create(self, vals):
        return super(Payment, self).create(vals)

    def _compute_access_url(self):
        for payment in self:
            payment.access_url = '/my/payment/%s' % payment.id