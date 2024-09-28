from odoo import models, fields, api
from odoo.exceptions import UserError

class Member(models.Model):
    _name = 'church.member'
    _description = 'Church Member'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True)
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    subparish_id = fields.Many2one('church.subparish', string='Sub-Parish')
    parish_id = fields.Many2one('church.parish', string='Parish', related='subparish_id.parish_id', store=True)
    archdeaconry_id = fields.Many2one('church.archdeaconry', string='Archdeaconry', related='parish_id.archdeaconry_id', store=True)
    diocese_id = fields.Many2one('church.diocese', string='Diocese', related='archdeaconry_id.diocese_id', store=True)
    payment_ids = fields.One2many('church.payment', 'member_id', string='Payments')
    total_contributions = fields.Float(string='Total Contributions', compute='_compute_total_contributions', store=True)
    user_id = fields.Many2one('res.users', string='Related User', ondelete='restrict')

     # Add this line to explicitly define the access_token field
    access_token = fields.Char(string='Access Token', copy=False)

    @api.depends('payment_ids.amount')
    def _compute_total_contributions(self):
        for member in self:
            member.total_contributions = sum(member.payment_ids.mapped('amount'))

    @api.model
    def create(self, vals):
        res = super(Member, self).create(vals)
        res.create_portal_user()
        return res

    def create_portal_user(self):
        for member in self:
            if not member.user_id:
                user_vals = {
                    'name': member.name,
                    'login': member.email,
                    'email': member.email,
                    'partner_id': self.env['res.partner'].create({
                        'name': member.name,
                        'email': member.email,
                        'phone': member.phone,
                    }).id,
                    'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
                }
                user = self.env['res.users'].create(user_vals)
                member.user_id = user.id
                # Send email to the user with their credentials
                template = self.env.ref('portal.mail_template_data_portal_welcome')
                if template:
                    template.send_mail(user.id, force_send=True)

    def action_create_portal_user(self):
        for member in self:
            if member.user_id:
                raise UserError('This member already has a portal user.')
            member.create_portal_user()

    def _compute_access_url(self):
        super(Member, self)._compute_access_url()
        for member in self:
            member.access_url = '/my/member/%s' % member.id

