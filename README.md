# POS Print Session Details (Odoo 20)

**POS Print Session Details** (`print_sessions_details`) displays key information and one-click print buttons for closed POS sessions directly on the **Odoo 20** POS Login Screen when the register is closed.

---

## Features

- **Closed Session Summary Card on Login Screen**:
  - **Session ID & Cashier Name** *(configurable)*
  - **Opening Date & Time** (converted to the user's local timezone)
  - **Closing Date & Time** (converted to the user's local timezone)
  - **Orders Count & Total Sales** *(configurable)*
  - **Opening Cash & Cash Difference** *(configurable)*
  - **Ending Balance**
- **Recent Sessions Navigation (`‹` / `›`)**:
  - Browse through the last **10 closed sessions** directly from the POS Login Screen card and print reports for any of them.
- **Direct Printing (Browser Preview & QZ Tray)**:
  - **Print**: Prints a concise receipt-style summary of the selected session.
  - **Print Details**: Prints the full **Custom Sales Details** report from `pos_hide_closing_register`.
  - Automatically uses **QZ Tray** when configured on the POS terminal, or falls back to Browser Print Preview.

---

## Configuration

Go to **Point of Sale → Configuration → Settings** (or edit an individual POS terminal under **Point of Sale → Configuration → Point of Sale**):
1. Enable **Show Session Details on Login**.
2. Toggle optional fields:
   - **Allow Browsing Recent Closed Sessions**
   - **Show Session Name & Cashier**
   - **Show Total Sales & Orders Count**
   - **Show Opening Cash & Difference**
3. Click **Save**.

---

## Technical Details

- **Module Name**: `print_sessions_details`
- **Odoo Version**: `20.0.2.0.0`
- **Dependencies**: `point_of_sale`, `pos_hide_closing_register`
- **Odoo 20 Architecture**:
  - **OWL 3**: Uses `proxy()` reactive state, mandatory `this.` template bindings, and `t-out` directives.
  - **Material Symbols**: Uses Odoo 20 Material Symbols ligature icons (`print`, `description`, `chevron_left`, `chevron_right`).
  - **Timezone Handling**: Uses Python's `zoneinfo.ZoneInfo` (`self.env.tz`).
- **License**: LGPL-3