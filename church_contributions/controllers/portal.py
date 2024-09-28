from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

class MemberPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payment_count' in counters:
            values['payment_count'] = request.env['church.payment'].search_count([('member_id', '=', request.env.user.partner_id.id)])
        return values

    @http.route(['/my/member/<int:member_id>'], type='http', auth="user", website=True)
    def portal_my_member(self, member_id=None, **kw):
        try:
            member_sudo = self._document_check_access('church.member', member_id)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._member_get_page_view_values(member_sudo, **kw)
        return request.render("church_contributions.portal_my_member", values)

    @http.route(['/my/payments', '/my/payments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_payments(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Payment = request.env['church.payment']

        domain = [('member_id', '=', request.env.user.partner_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'payment_date desc'},
            'amount': {'label': _('Amount'), 'order': 'amount desc'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('payment_date', '>', date_begin), ('payment_date', '<=', date_end)]

        # count for pager
        payment_count = Payment.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/payments",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=payment_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        payments = Payment.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_payments_history'] = payments.ids[:100]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'payments': payments,
            'page_name': 'payment',
            'pager': pager,
            'default_url': '/my/payments',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("church_contributions.portal_my_payments", values)

    def _member_get_page_view_values(self, member, **kwargs):
        values = {
            'page_name': 'member',
            'member': member,
        }
        return self._get_page_view_values(member, access_token=None, values=values, session_history=None, **kwargs)