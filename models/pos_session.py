from zoneinfo import ZoneInfo
import traceback

from odoo import models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def get_last_closed_session_info(self, config_id):
        """
        Return info about recent closed sessions for the given POS config.
        Prioritizes sessions with non-zero activity while also returning
        a `sessions_list` (up to 10 recent sessions) for prev/next browsing.
        """
        config = self.env['pos.config'].sudo().browse(config_id)
        if not config.exists():
            return False

        closed_sessions = self.sudo().search(
            [
                ('config_id', '=', config_id),
                ('state', '=', 'closed'),
            ],
            order='stop_at desc, id desc',
            limit=50,
        )

        if not closed_sessions:
            return False

        user_tz = self.env.tz or ZoneInfo(self.env.user.tz or 'UTC')
        if isinstance(user_tz, str):
            user_tz = ZoneInfo(user_tz)
        utc_tz = ZoneInfo('UTC')

        def fmt_dt(dt):
            if not dt:
                return '-'
            local_dt = dt.replace(tzinfo=utc_tz).astimezone(user_tz)
            return local_dt.strftime('%b %d, %H:%M')

        currency = config.currency_id
        symbol = getattr(config, 'sale_details_currency_symbol', False) or currency.symbol or 'DH'

        def serialize_session(s):
            valid_orders = s.order_ids.filtered(lambda o: o.state not in ('draft', 'cancel'))
            total_sales = sum(valid_orders.mapped('amount_total'))
            opening_bal = getattr(s, 'cash_register_balance_start', 0.0) or 0.0
            ending_bal = getattr(s, 'cash_register_balance_end_real', 0.0) or 0.0
            if ending_bal == 0.0:
                ending_bal = getattr(s, 'cash_register_balance_end', 0.0) or 0.0
            cash_diff = getattr(s, 'cash_register_difference', 0.0) or 0.0

            return {
                'session_id': s.id,
                'name': s.name,
                'cashier': s.user_id.name or '-',
                'opening_date': fmt_dt(s.start_at),
                'closing_date': fmt_dt(s.stop_at),
                'order_count': len(valid_orders),
                'total_sales': f"{total_sales:.2f} {symbol}",
                'opening_balance': f"{opening_bal:.2f} {symbol}",
                'ending_balance': f"{ending_bal:.2f} {symbol}",
                'cash_difference': f"{cash_diff:+.2f} {symbol}" if cash_diff != 0 else f"0.00 {symbol}",
                'has_negative_diff': cash_diff < 0,
                'currency_symbol': symbol,
                '_raw_activity': abs(ending_bal) + abs(total_sales),
            }

        serialized_all = [serialize_session(s) for s in closed_sessions]
        non_zero = [item for item in serialized_all if item['_raw_activity'] > 0]
        session_history = (non_zero or serialized_all)[:10]

        primary = session_history[0]
        primary['history'] = session_history
        return primary

    @api.model
    def get_session_details_report_html(self, session_id):
        """
        Render the sale-details report HTML for a given session_id.
        Delegates to the report defined in pos_hide_closing_register.
        """
        try:
            session = self.sudo().browse(session_id)
            if not session.exists():
                return "<html><body><h1>Session not found</h1></body></html>"
            report = self.env.ref('pos_hide_closing_register.sale_details_report').sudo()
            html = report._render_qweb_html(report.report_name, [session_id])[0].decode('utf-8')
            return html
        except Exception as exc:
            return (
                f"<html><body><h1>Error</h1><p>{exc}</p>"
                f"<pre>{traceback.format_exc()}</pre></body></html>"
            )