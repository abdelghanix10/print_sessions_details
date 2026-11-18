from odoo import api, fields, models


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

    @api.model
    def _load_pos_data_read(self, records, config):
        read_records = super()._load_pos_data_read(records, config)
        for record, pos_config in zip(read_records, records):
            record.update({
                'enable_session_details': pos_config.enable_session_details,
                'psd_show_cashier': pos_config.psd_show_cashier,
                'psd_show_total_sales': pos_config.psd_show_total_sales,
                'psd_show_cash_diff': pos_config.psd_show_cash_diff,
                'psd_allow_session_navigation': pos_config.psd_allow_session_navigation,
            })
        return read_records