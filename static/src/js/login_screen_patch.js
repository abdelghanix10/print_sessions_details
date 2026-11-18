/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { LoginScreen } from "@point_of_sale/app/screens/login_screen/login_screen";
import { proxy, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(LoginScreen.prototype, {
  setup() {
    super.setup(...arguments);
    this.orm = useService("orm");

    // OWL 3 in Odoo 20 uses proxy() instead of useState()
    this.sessionDetails = proxy({
      show: false,
      loading: true,
      currentIndex: 0,
      history: [],
    });

    onWillStart(async () => {
      await this._loadLastSessionDetails();
    });

    onMounted(async () => {
      await this._loadLastSessionDetails();
    });
  },

  get showSessionDetailsBlock() {
    if (!this.pos?.config?.enable_session_details) return false;
    return this.sessionDetails.show;
  },

  get currentSessionItem() {
    return (
      this.sessionDetails.history[this.sessionDetails.currentIndex] || null
    );
  },

  get canGoOlderSession() {
    return (
      this.pos?.config?.psd_allow_session_navigation &&
      this.sessionDetails.currentIndex < this.sessionDetails.history.length - 1
    );
  },

  get canGoNewerSession() {
    return (
      this.pos?.config?.psd_allow_session_navigation &&
      this.sessionDetails.currentIndex > 0
    );
  },

  olderSession() {
    if (this.canGoOlderSession) {
      this.sessionDetails.currentIndex++;
    }
  },

  newerSession() {
    if (this.canGoNewerSession) {
      this.sessionDetails.currentIndex--;
    }
  },

  async _loadLastSessionDetails() {
    const configId = this.pos?.config?.id || odoo.pos_config_id;
    if (!configId) {
      this.sessionDetails.show = false;
      this.sessionDetails.loading = false;
      return;
    }
    try {
      const info = await this.orm.call(
        "pos.session",
        "get_last_closed_session_info",
        [configId],
      );
      if (info && info.history && info.history.length > 0) {
        this.sessionDetails.history = info.history;
        this.sessionDetails.currentIndex = 0;
        this.sessionDetails.show = true;
      } else {
        this.sessionDetails.show = false;
      }
    } catch {
      this.sessionDetails.show = false;
    } finally {
      this.sessionDetails.loading = false;
    }
  },

  async _dispatchPrintHtml(title, bodyHtml, width = 600, height = 500) {
    const printMethod = this.pos?.config?.print_method || "chrome_preview";
    const fullHtml = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>${title}</title>
                <style>
                    body {
                        font-family: "Courier New", Courier, monospace;
                        font-size: 14px;
                        font-weight: bold;
                        margin: 15px;
                    }
                    table { width: 100%; border-collapse: collapse; }
                    td { padding: 4px 0; }
                    td:last-child { text-align: right; }
                    hr { border: none; border-top: 1px dashed #000; margin: 8px 0; }
                    .title { text-align: center; font-size: 16px; margin-bottom: 10px; }
                    @media print { body { margin: 0; } }
                </style>
            </head>
            <body>
                ${bodyHtml}
                <script>
                    window.onload = function () {
                        window.print();
                        window.onafterprint = function () { window.close(); };
                    };
                </script>
            </body>
            </html>
        `;

    if (printMethod === "qz_tray") {
      const qzService = this.env.services.qz_tray;
      if (qzService) {
        try {
          await qzService.connect();
          const qzLib = qzService.getQZ();
          const printerName = await qzLib.printers.getDefault();
          await qzService.print(
            printerName,
            `<html><body>${bodyHtml}</body></html>`,
            "pixel",
            { scaleContent: false },
          );
          return;
        } catch (err) {
          console.warn(
            "QZ Tray print failed, falling back to browser preview:",
            err,
          );
        }
      }
    }

    const printWin = window.open(
      "",
      "_blank",
      `width=${width},height=${height}`,
    );
    if (printWin) {
      printWin.document.write(fullHtml);
      printWin.document.close();
    }
  },

  /** Print the summary card for the currently selected closed session */
  async printSessionSummary() {
    const item = this.currentSessionItem;
    if (!item) return;

    const cfg = this.pos.config;
    let rowsHtml = "";
    if (cfg.psd_show_cashier) {
      rowsHtml += `<tr><td>Session</td><td>${item.name}</td></tr>`;
      rowsHtml += `<tr><td>Cashier</td><td>${item.cashier}</td></tr>`;
    }
    rowsHtml += `<tr><td>Opening Date</td><td>${item.opening_date}</td></tr>`;
    rowsHtml += `<tr><td>Closing Date</td><td>${item.closing_date}</td></tr>`;
    if (cfg.psd_show_total_sales) {
      rowsHtml += `<tr><td>Orders</td><td>${item.order_count}</td></tr>`;
      rowsHtml += `<tr><td>Total Sales</td><td>${item.total_sales}</td></tr>`;
    }
    if (cfg.psd_show_cash_diff) {
      rowsHtml += `<tr><td>Opening Cash</td><td>${item.opening_balance}</td></tr>`;
      rowsHtml += `<tr><td>Cash Diff</td><td>${item.cash_difference}</td></tr>`;
    }
    rowsHtml += `<tr><td>Ending Balance</td><td>${item.ending_balance}</td></tr>`;

    const bodyHtml = `
            <div class="title">SESSION SUMMARY</div>
            <hr/>
            <table>${rowsHtml}</table>
            <hr/>
        `;
    await this._dispatchPrintHtml("Session Summary", bodyHtml, 600, 450);
  },

  /** Print the full sale-details report for the currently selected closed session */
  async printSessionDetails() {
    const item = this.currentSessionItem;
    if (!item || !item.session_id) return;

    try {
      const reportHtml = await this.orm.call(
        "pos.session",
        "get_session_details_report_html",
        [item.session_id],
      );
      await this._dispatchPrintHtml("Session Details", reportHtml, 800, 600);
    } catch (err) {
      console.error("print_sessions_details: failed to fetch report HTML", err);
    }
  },
});
