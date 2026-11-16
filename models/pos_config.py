from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_session_details = fields.Boolean(
        string="Show Session Details on Login",
        default=True,
        help="When enabled, closed session details are shown on the POS login screen "
             "along with Print and Print Details buttons.",
    )
    psd_show_cashier = fields.Boolean(
        string="Show Session Name & Cashier",
        default=True,
    )
    psd_show_total_sales = fields.Boolean(
        string="Show Total Sales & Orders Count",
        default=True,
    )
    psd_show_cash_diff = fields.Boolean(
        string="Show Opening Cash & Difference",
        default=False,
    )
    psd_allow_session_navigation = fields.Boolean(
        string="Allow Browsing Recent Closed Sessions",
        default=True,
        help="Allow stepping through recent closed sessions using prev/next arrows on the login card.",
    )