from odoo import models, fields

class Payment(models.Model):
    _name = "kiosks.payment"
    _description = "Kiosk Payments"

    vendor_id = fields.Many2one("kiosks.vendor", string="Vendor", required=True)
    kiosk_id = fields.Many2one("kiosks.kiosk", string="Kiosk")
    amount_paid = fields.Float(string="Amount Paid", required=True)
    balance = fields.Float(string="Balance")
    payment_method = fields.Selection([
        ("mpesa", "M-Pesa"),
        ("cash", "Cash"),
        ("bank", "Bank Transfer")
    ], string="Payment Method")
    payment_date = fields.Date(string="Payment Date", default=fields.Date.today)
