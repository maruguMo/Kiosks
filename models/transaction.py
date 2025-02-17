from odoo import models, fields

class KioskTransaction(models.Model):
    _name = "kiosks.transaction"
    _description = "Kiosk Transactions"

    kiosk_id = fields.Many2one("kiosks.kiosk", string="Kiosk", required=True)
    vendor_id = fields.Many2one("kiosks.vendor", string="Vendor", required=True)
    transaction_type = fields.Selection([
        ("rent", "Rent"),
        ("sale", "Sale")
    ], string="Type", required=True)
    amount = fields.Float(string="Amount", required=True)
    due_date = fields.Date(string="Due Date")
    payment_status = fields.Selection([
        ("pending", "Pending"),
        ("paid", "Paid")
    ], string="Payment Status", default="pending")
