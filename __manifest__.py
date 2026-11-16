{
    'name': 'POS Print Session Details',
    'version': '20.0.2.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Show recent closed sessions info and print reports on POS login screen',
    'description': """
POS Print Session Details (Odoo 20)
===================================
Displays closed session details (Session Name, Cashier, Opening/Closing Date,
Total Sales, Orders, Opening/Ending Balance, Cash Difference) on the POS login screen
when the register is closed, with navigation across recent closed sessions and
one-click Print Summary & Print Details (supporting both Browser Print and QZ Tray).
    """,
    'author': 'Custom',
    'depends': ['point_of_sale', 'pos_hide_closing_register'],
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'print_sessions_details/static/src/css/login_screen.css',
            'print_sessions_details/static/src/js/login_screen_patch.js',
            'print_sessions_details/static/src/xml/login_screen_patch.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}