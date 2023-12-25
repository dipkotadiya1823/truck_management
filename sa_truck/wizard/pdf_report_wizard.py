from odoo import fields,models,api

class PdfReportWizard(models.TransientModel):
    _name = "pdf.report.wizard"
    _description = "Pdf Report Using wizard"

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    def confirm(self):
        data ={
            'start_date' : self.start_date,
            'end_date' : self.end_date,
        }
        return self.env.ref('sa_truck.action_sa_truck_wizard_report').report_action(self, data = data)
    
class PdfReportWizardAbstractModel(models.AbstractModel):
    _name = "report.sa_truck.satruck_wizard_report"
    _description = "Abstract Model in wizard for pdf Report"

    def _get_report_values(self,docids,data=None):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
            
        docs = self.env['sa.truck'].search([('create_datetime', '>=', start_date), ('create_datetime', '<=', end_date)])
        return {
            'docs': docs
        }
