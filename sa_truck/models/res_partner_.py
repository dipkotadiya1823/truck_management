from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit="res.partner"

    active_driver = fields.Boolean("Active Driver")
    car = fields.Char("Car")

    @api.onchange('company_type')
    def active_driver_onchange(self):
        if self.company_type == 'person':
            self.active_driver = True
        else:
            self.active_driver = False