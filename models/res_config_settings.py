from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_enable_session_details = fields.Boolean(
        related='pos_config_id.enable_session_details',
        readonly=False,
    )
    pos_psd_show_cashier = fields.Boolean(
        related='pos_config_id.psd_show_cashier',
        readonly=False,
    )
    pos_psd_show_total_sales = fields.Boolean(
        related='pos_config_id.psd_show_total_sales',
        readonly=False,
    )
    pos_psd_show_cash_diff = fields.Boolean(
        related='pos_config_id.psd_show_cash_diff',
        readonly=False,
    )
    pos_psd_allow_session_navigation = fields.Boolean(
        related='pos_config_id.psd_allow_session_navigation',
        readonly=False,
    )