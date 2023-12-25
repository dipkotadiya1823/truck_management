from odoo import models,fields,api
from datetime import datetime
from odoo.exceptions import UserError

class SaTruck(models.Model):
    _name = "sa.truck"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Sa Truck"
    
    name = fields.Char("Trip Code", tracking=True)
    email = fields.Char("Email", tracking=True)
    driver_image = fields.Binary("Driver Image", tracking=True)
    sequence = fields.Char("Sequence", index=True, copy=False, tracking=True)
    code = fields.Char("Code")
    # Company_name_id = fields.Many2one("res.company", string="Company Name")
    company_id = fields.Many2one("res.company", default = lambda self: self.env.company, string="Company Name", tracking=True)
    vehicle_idd = fields.Many2one("vehicle.vehicle", string="Vehicle Model", tracking=True)
    driverinfo_ids = fields.One2many("driver.info","satruck_id", string="Driver Informaton", tracking=True)
    satruck_id = fields.Many2one("sa.truck", string="SA Truck")
    state = fields.Selection([("draft","Draft"), ("to_approve","To Approve"), ("Approve","Approve")], string = "State", default = "draft", tracking=True)
    create_datetime = fields.Datetime("Create Date Time", default=datetime.today(), tracking=True)
    driver_id = fields.Many2one("res.partner", string="Driver Name", tracking=True , store=True)
    manager_idd = fields.Many2one("res.users", string="Manager", tracking=True)
    km = fields.Char("KM")
    from_city_id = fields.Many2one("city.city", string="From City", tracking=True)
    to_city_id = fields.Many2one("city.city", string="To City", tracking=True)
    total = fields.Float(compute="get_total", store=True)
    sa_addisnal_amount = fields.Float("", compute="get_sa_addisnal_amount", store=True)
    total_with_addisnal_amount = fields.Float(compute="get_total_with_addisnal_amount", store=True)   
    # sa_truck_id = fields.Many2one('sa.truck', string="SA Truck") 
    count_invoice = fields.Integer("Count Invoice", compute="get_count_invoice")
    account_move_ids = fields.One2many("account.move","sa_truck_id", string="Account Move")
    # duration = fields.Date("duration")
    duration1 = fields.Float("Duration")
    # date_stop = fields.Date("Arrival Date")
    additional_amount_tax_ids = fields.Many2many("account.tax",
                                                 "tax_additional_amount_rel",
                                                 "account_tax",
                                                 "additional_amount",
                                                 string="Additional Amount")

    def get_count_invoice(self):
        for rec in self:
            rec.count_invoice = rec.account_move_ids and len(rec.account_move_ids) or  0

    @api.onchange('driver_id')
    def res_driver_image(self):
        self.driver_image = self.driver_id.image_1920

    def action_open_invoice(self):
        print(self)
        return {
            'name': "Invoice",
            'type': "ir.actions.act_window",
            'res_model': "account.move",
            "view_mode": "tree",
            "domain": [('sa_truck_id', 'in', self.name)],
        }

    def create_invoice(self):
        new_list = []
        for rec in self.driverinfo_ids:
            vals = {  
                'name' : rec.checklist_id.name,
                'quantity' : rec.quantity,
                'price_unit' : rec.unit_price,
                'tax_ids' : rec.additional_amount_ids,
                'price_subtotal' : rec.total_amount,
            }
            new_list.append((0,None,vals))
        invoice_vals = {
            'move_type' : 'out_invoice',
            # 'name' : ,
            'partner_id' : self.driver_id.id,
            'invoice_date' : self.create_datetime,
            'sa_truck_id': self.id,
            'company_name' : self.company_id.name,
            'invoice_line_ids' : new_list,
        }
        self.env['account.move'].create(invoice_vals)
        print(invoice_vals)

    @api.constrains('driverinfo_ids')
    def checklist_name(self):
        new_list = []
        for res in self:
            for rec in res.driverinfo_ids:
                if rec.checklist_id in new_list:
                    raise UserError(f"You are Enter {rec.checklist_id.name} More then one Time")
                elif rec.checklist_id.id is False:
                    raise UserError("You are not Enter CheckList")
                else:
                    new_list.append(rec.checklist_id) 

    @api.constrains('to_city_id')
    def city(self):
        for rec in self:
            if rec.from_city_id == rec.to_city_id:
                raise UserError(f"Please Change City {rec.to_city_id.name} is use in From City")
           
    @api.depends('driverinfo_ids')
    def get_total(self):
        for rec in self:
            rec.total = rec.driverinfo_ids and sum(rec.driverinfo_ids.mapped('subtotal')) or 0

    @api.depends('driverinfo_ids')
    def get_sa_addisnal_amount(self):
        for res in self:
            sa_addisnal_amount = 0
            for rec in self.driverinfo_ids:
                for i in rec.additional_amount_ids:
                    sa_addisnal_amount += (i.amount * rec.subtotal)/100
            res.sa_addisnal_amount = sa_addisnal_amount

    @api.depends('driverinfo_ids')
    def get_total_with_addisnal_amount(self):
        for rec in self:
            rec.total_with_addisnal_amount = rec.driverinfo_ids and sum(rec.driverinfo_ids.mapped('total_amount')) or 0

    @api.model_create_multi
    def create(self, vals): 
        form_code = super(SaTruck, self).create(vals)
        form_code.sequence = self.env['ir.sequence'].next_by_code('sa.truck')
        driver_code = ''
        vehicle_code = ''
        if form_code.driver_id.name != False:
            driver_code = form_code.driver_id.name.upper()[0:3]
        if form_code.vehicle_idd.vehicle_model_id.license_plate != False:
            vehicle_code = form_code.vehicle_idd.vehicle_model_id.license_plate[2:5]
            # print("********* vehicle_code", vehicle_code)
        if driver_code == False:
            # print("********* driver_code", driver_code)
            # print("********* driver_code", vehicle_code)
            print(form_code)
        if vehicle_code == False:
            print(form_code)
        form_code.name = driver_code+'/'+vehicle_code+'/'+form_code.sequence
        return form_code    
 
    def reset_to_draft(self):
        for rec in self:    
            rec.state = "draft"
        return True

    def action_to_approve(self):
        for rec in self:
            rec.state = "to_approve"
        return True

    def action_approve(self):
        for rec in self:
            rec.state = "Approve"
        return{
            'effect':{
                'type' : 'rainbow_man',
                'message' : 'Report Approved'
            }
        }
    
    def action_send_email(self):
        temp_id=self.env.ref('sa_truck.sa_truck_email_template')
        # template=self.env['mail.template'].browse(temp_id)
        # temp_id.send_mail(self.id)
        ctx = {
            'default_model':'sa.truck',
            'default_res_id': self.id,
            'default_use_template': bool(temp_id),
            'default_template_id' : temp_id.id if temp_id else None,
            'default_composition_mode' : 'comment',
            'mark_so_as_sent':True,
            'default_email_layout_xmlid':'mail.mail_notification_layout_with_responsible_signature',
            'default_force_send':True,
        }
        return {
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'mail.compose.message',
            'views':[(False,'form')],
            'view_id': False,
            'target':'new',
            'context':ctx,
        }
    # def get_report_data(self):
    #     quary = """select * from sa_truck"""
    #     self.env.cr.execute(quary)
    #     info = self.env.cr.dictfetchall()
    #     return info
    
    # def print_pdf_report(self):
    #     data = self.get_report_data()
    #     return self.env.ref('sa_truck.action_sa_truck_report').report_action(self,data=data)

    # def action_check(self):
    #     print("Hello")

    def state_converter(self):
        draft = self.env['sa.truck'].search([('state','=','draft')])
        to_approve = self.env['sa.truck'].search([('state','=','to_approve')])
        if draft:
            draft.write({'state':'to_approve'})
        if to_approve:
            to_approve.write({'state':'Approve'})
        