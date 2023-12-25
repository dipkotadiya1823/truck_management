from odoo import fields,models,api
import base64
import io
from odoo import tools
from xlsxwriter.utility import xl_rowcol_to_cell

class WizardXlsxReport(models.TransientModel):
    _name = "wizard.xlsx"
    _description = "xlsx report useing wizard"

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")

    def confirm(self):
        print(self)
        data = {
            'date_from' : self.date_from,
            'date_to' : self.date_to
        }
        return self.env.ref('sa_truck.action_sa_truck_xls_report').report_action(self, data = data) 
    
class wizardCXlsxReport(models.AbstractModel):
    _name = "report.sa_truck.satruck_xls_report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Xlsx Report Abstract Model"
    
    def generate_xlsx_report(self, workbook, data, driver):
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        docs = self.env['sa.truck'].search([('create_datetime', '>=', date_from), ('create_datetime', '<=', date_to)])

        if date_from and date_to:
            driver = docs
        
        bold = workbook.add_format({'bold' : True})
        format_1 = workbook.add_format({'bold' :True, 'align' : 'center', 'bg_color' : 'blue'})
        format_2 = workbook.add_format( {'bold' : True, 'align' : 'center','bg_color' : '#C0C0C0'})
        format_3 = workbook.add_format({'align' : 'center' })
        right = workbook.add_format({'align': 'right', 'border': 1})
                            
        for obj in driver:
            # print(obj)
            sheet= workbook.add_worksheet(obj.driver_id.name)
            sheet.set_column('E:F', 20)
            sheet.set_column('G:H', 20)
            sheet.set_column('I:J', 20)
            row = 3
            col = 3

            if obj.company_id.logo:
                col += 1
                sheet.set_row(row, 60)
                # image_file = open('/home/entrivis/Downloads/unnamed.png', 'rb')
                driver_images = io.BytesIO(base64.b64decode(obj.company_id.logo))
                sheet.insert_image(row, col,'image.jpg', {'image_data' : driver_images, 'x_offset': 5, 'y_offset': 5, 'x_scale' : 0.1, 'y_scale' : 0.1})
                
                from_cell = xl_rowcol_to_cell(row, col)
                if obj.state:
                    col += 5
                else:
                    col += 6
                to_cell = xl_rowcol_to_cell(row, col)
                # sheet.merge_range(tools.ustr(from_cell) + ':' + tools.ustr(to_cell), obj.company_id.name + '\n' + obj.company_id.street + '\n' + obj.company_id.city + obj.company_id.zip + '\n'
                #                       + obj.company_id.state_id.name + obj.company_id.country_id.name, right)
            col -= 6
            col += 1
            row += 2
            sheet.merge_range(row, col, row, col + 1, 'Driver Trip Information', format_1)

            row += 2
            sheet.write(row, col, 'Trip Code', bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'Driver Name', bold)
            sheet.write(row, col + 1, obj.driver_id.name)
            row += 1
            sheet.write(row, col, 'Vehicle Model', bold)
            sheet.write(row, col + 1, obj.vehicle_idd.name)
            row += 1
            sheet.write(row, col, 'Company Name', bold)
            sheet.write(row, col + 1, obj.company_id.name)
            
            row += 1
            sheet.write(row , col, 'From City', bold)
            sheet.write(row , col + 1, obj.from_city_id.name)
            sheet.write(row + 1, col, 'To City', bold)
            sheet.write(row + 1, col + 1, obj.to_city_id.name)
            sheet.write(row + 2, col, 'Manager', bold)
            sheet.write(row + 2, col + 1, obj.manager_idd.name)
            # sheet.write(row, col, 'Create Date Time', bold)
            # sheet.write(row, col +1, obj.create_datetime)      
            
            row += 4
            sheet.merge_range(row, col, row, col + 5,'Driver Expenses', format_1)

            row += 1
            sheet.write(row, col, 'CheckList', format_2)
            sheet.write(row , col + 1, 'Additional Amount', format_2)
            sheet.write(row , col + 2, 'Unit Price', format_2)
            sheet.write(row, col + 3, 'Quantity', format_2)
            sheet.write(row ,col + 4, 'Sub Total', format_2)
            sheet.write(row, col + 5, 'Total Amount', format_2)

            for rec in obj.driverinfo_ids:
                row += 1
                sheet.write(row, col, rec.checklist_id.name, format_3)
                print(rec.checklist_id.name)
                sheet.write(row, col + 1, rec.additional_amount_ids.name, format_3)
                sheet.write(row, col + 2, rec.unit_price, format_3)
                sheet.write(row, col + 3, rec.quantity, format_3)
                sheet.write(row, col + 4, rec.subtotal, format_3)
                sheet.write(row, col + 5, rec.total_amount, format_3)
            
            sheet.write(row + 2, col + 4, 'Total', format_2)
            sheet.write(row + 2, col + 5, obj.total_with_addisnal_amount)

            sheet.write(row + 4, col + 4, 'Approved By', format_2)
            sheet.write(row + 4, col + 5, obj.manager_idd.name, format_3)

