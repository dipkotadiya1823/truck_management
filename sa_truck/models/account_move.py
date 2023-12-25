from odoo import fields, models, api

class accountmove(models.Model):
    _inherit = "account.move"

    sa_truck_id = fields.Many2one("sa.truck", string = "Trip Code")
    # trip_code = fields.Char("Trip Code")
    company_name = fields.Char("Company Name")      