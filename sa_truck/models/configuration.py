from odoo import fields,models,api
from odoo.exceptions import UserError

class DriverInfo(models.Model):
    _name = "driver.info"
    _description = "Driver Information"

    remark = fields.Char("Remark")
    seq = fields.Integer("seq.")
    checklist_id = fields.Many2one("check.list", string="CheckList")
    states_id = fields.Many2one("states.states", string="States")
    frequency_id = fields.Many2one("frequency.frequency", string="Frequency")
    vehicle_id = fields.Many2one("vehicle.vehicle", string="Vehicle", store=True)
    City = fields.Many2one("city.city", string="City")
    satruck_id = fields.Many2one("sa.truck", string="Sa truck")
    additional_amount = fields.Float("Additional Amount(%)")
    unit_price = fields.Float("Unit Price")
    quantity = fields.Float("Quantity", default = 1)
    subtotal = fields.Float("Sub Total", compute="get_subtotal", store=True)
    total_amount = fields.Float("Total Amount (With Additional Amount)", compute="get_total_amount", store=True)
    additional_amount_ids = fields.Many2many("account.tax",
                                             "account_tax_additional_amount_rel",
                                             "account_tax",
                                             "additional_amount", 
                                             string="Additional Amount")

    @api.constrains('unit_price')
    def uni_price1(self):
        for rec in self:
            if rec.unit_price > rec.checklist_id.unit_price:
                raise UserError(f"Please Enter Less Then {rec.checklist_id.unit_price}")
            elif rec.unit_price < 0:
                raise UserError("Please Enter Positive Value")

    @api.depends('unit_price','quantity')
    def get_subtotal(self):
        for rec in self:
            rec.subtotal = rec.unit_price * rec.quantity
    
    @api.depends('subtotal','additional_amount_ids')
    def get_total_amount(self):
        for rec in self:
            for i in rec.additional_amount_ids:
                rec.total_amount = ((i.amount * rec.subtotal)/100)
            rec.total_amount = rec.total_amount + rec.subtotal

    # def action_check(self):
    #     for rec in self:
    #         pass

    # def action_cross(self):
    #     pass

class CheckList(models.Model):
    _name = "check.list"
    _description = "CheckList"

    name = fields.Char("Name")
    unit_price = fields.Float("Unit price")

    @api.constrains('unit_price')
    def get_unit_price(self):
        if self.unit_price < 0:
            raise UserError("Please Enter Positive Value")
                       
class States(models.Model):
    _name = "states.states"
    _description = "States"

    name = fields.Char("name")

class Frequency(models.Model):
    _name = "frequency.frequency"
    _description = "frequency"

    name = fields.Char("name")

class Vehicle(models.Model):
    _name = "vehicle.vehicle"
    _description = "Vehicle"

    name = fields.Char("name")
    vehicle_model_id = fields.Many2one("fleet.vehicle", string="Vehicle Model")

class City(models.Model):
    _name = "city.city"
    _description = "City"

    name = fields.Char("City")