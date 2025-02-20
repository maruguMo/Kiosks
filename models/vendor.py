from odoo import models, fields, api
from datetime import date

class Vendor(models.Model):
    _name = "kiosks.vendor"
    _description = "Kiosk Vendor"
    _rec_name = "vendor_full_name"

    first_name = fields.Char(string="First Name", required=True)
    second_name = fields.Char(string="Second Name", required=True)
    vendor_full_name = fields.Char(string="Vendor Name", compute="_compute_display_name", store=True)

    email = fields.Char(string="E-Mail", required=True)
    phone = fields.Char(string ="Phone", required =True)

    id_document = fields.Selection([
        ("national_id", "National ID"),
        ("passport", "Passport"),
        ("other", "Other")
    ], string="ID Document Type", required=True)
    id_number = fields.Char(string="ID Number", size=10, required=True)

    lease_ids = fields.One2many("kiosks.license", "vendor_id", string="Leases")

    lease_count = fields.Integer('Number of Leases', compute='_compute_lease_count')

    @api.depends('lease_ids')
    def _compute_lease_count(self):
        for record in self:
            record.lease_count = len(record.lease_ids)

    @api.depends("first_name", "second_name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.first_name} {record.second_name}"