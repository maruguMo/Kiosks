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
    ], string="Status", default="available", compute='_compute_status', store=True)

    manufacture_date = fields.Date(string="Manufacture Date")
    manufacture_id = fields.Char(string="Manufacture ID", size=10)

    lease_ids = fields.One2many("kiosks.license", "kiosk_id", string="Lease History")

    transaction_id = fields.Many2one('kiosks.transaction', string="Sale Transaction")
 
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

    # compute if a kiosk has an active lease and set status automatically                
    @api.depends('lease_ids.is_expired', 'status')
    def _compute_status(self):
        for record in self:
            active_lease = record.lease_ids.filtered(lambda l: not l.is_expired)
            if not active_lease and record.status != 'sold':
                record.status = 'available'
            else:
                record.status = 'rented'

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'sold':
            if not self.transaction_id:
                raise exceptions.ValidationError("A sale transaction must be recorded when marking a kiosk as sold.")
            # Terminate active leases
            active_leases = self.env['kiosks.license'].search([('kiosk_id', '=', self.id), ('is_expired', '=', False)])
            for lease in active_leases:
                lease.action_terminate_lease()

    @api.model
    def action_save(self):
        # Perform any custom operations here if necessary
        return {'type': 'ir.actions.act_window_close'}
