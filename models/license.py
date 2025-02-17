from odoo import models, fields, api
from datetime import datetime, timedelta

class KioskLicense(models.Model):
    _name = "kiosks.license"
    _description = "Kiosk License (Lease)"

    name = fields.Char(string="License(Lease Type)", required=True)
    annual_fee = fields.Float(string="Annual Fee")
    date_start = fields.Date(string="Lease Start Date", required=True)
    date_end = fields.Date(string="Lease End Date")
    
    kiosk_id = fields.Many2one("kiosks.kiosk", string="Kiosk", required=True)
    vendor_id = fields.Many2one("kiosks.vendor", string="Vendor", required=True)

    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")

    geolocation = fields.Char(string="Geolocation", compute="_compute_geolocation") #incase the kiosk is moved
    is_expired = fields.Boolean('Expired', compute='_compute_is_expired', store=True)
    vendor_full_name = fields.Char('Vendor Name', compute='_compute_vendor_full_name', store=True)

    @api.depends("latitude", "longitude")
    def _compute_geolocation(self):
        for rec in self:
            rec.geolocation = f"{rec.latitude}, {rec.longitude}" if rec.latitude and rec.longitude else ""

    @api.depends('date_end')
    def _compute_is_expired(self):
        today = date.today()
        for record in self:
            record.is_expired = record.date_end < today if record.date_end else False

    @api.depends('vendor_id.first_name', 'vendor_id.second_name')
    def _compute_vendor_full_name(self):
        for record in self:
            if record.vendor_id:
                record.vendor_full_name = f"{record.vendor_id.first_name} {record.vendor_id.second_name}"
            else:
                record.vendor_full_name = ""
    
    @api.model
    def _send_lease_expiry_reminders(self):
        today = datetime.now().date()
        one_month_from_now = today + timedelta(days=30)
        
        expiring_soon = self.search([('date_end', '<=', one_month_from_now), ('date_end', '>=', today)])
        
        for lease in expiring_soon:
            if lease.vendor_id.email:
                template = self.env.ref('kiosks.lease_expiry_email_template')
                template.send_mail(lease.id, force_send=True)