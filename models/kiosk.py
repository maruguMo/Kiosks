from odoo import models, fields, api
from odoo.modules.module import get_module_resource
from datetime import date
from odoo.tools import misc
import base64

class Kiosk(models.Model):
    _name = "kiosks.kiosk"
    _description = "Kiosk Details"

    name = fields.Char(string="Kiosk Name", required=True)
    size = fields.Selection([("small", "Small"), ("medium", "Medium"), ("large", "Large")], string="Size")
    size_image = fields.Binary(string="type ->", compute="_compute_size_image")
    location = fields.Char(string="Enter physical location", required=True)

    longitude=fields.Float(string="Longitude")
    latitude=fields.Float(string ="Latitude")
    geolocation = fields.Char(string="Geolocation", compute="_compute_geolocation")
    
    status = fields.Selection([
        ("available", "Available"),
        ("rented", "Rented"),
        ("sold", "Sold")
    ], string="Status", default="available")

    manufacture_date = fields.Date(string="Manufacture Date")
    manufacture_id = fields.Char(string="Manufacture ID", size=10)

    lease_ids = fields.One2many("kiosks.license", "kiosk_id", string="Lease History")
 
    @api.depends("latitude", "longitude")
    def _compute_geolocation(self):
        for rec in self:
            rec.geolocation = f"{rec.latitude}, {rec.longitude}" if rec.latitude and rec.longitude else ""
    
    @api.depends("size")
    def _compute_size_image(self):
        for record in self:
            if record.size:
                image_path = misc.file_path(f'kiosks/static/src/img/{record.size}.png')
                print(f"THIS IS THE IMAGE FILE PATH: {image_path}")
                try:
                    with open(image_path, "rb") as image_file:
                        record.size_image = base64.b64encode(image_file.read())
                except FileNotFoundError:
                    record.size_image = False
            else:
                record.size_image = False
                
    @api.onchange("status")
    def _onchange_status(self):
        for rec in self:
            if rec.status == "available":
                rec.lease_ids.filtered(lambda l: not l.end_date).write({"end_date": date.today()})

    @api.model
    def action_save(self):
        # Perform any custom operations here if necessary
        return {'type': 'ir.actions.act_window_close'}