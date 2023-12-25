from odoo import fields,models,api

class PdfReportQuaryWizard(models.TransientModel):
    _name = "pdf.report.quary.wizard"
    # _inherit = "sa.truck"
    _description = "Pdf Report wizard Using SQL Quary"

    sa_truck_ids = fields.Many2many('sa.truck', string="SA Truck")
    def _fetch_data(self):
        result = []
        acc_grp_res= ",".join(map(str, self.sa_truck_ids.ids))
        self._cr.execute("""SELECT 
                                sa.name as name,
                                sa.email as email,
                                sa.create_datetime as create_datetime,
                                sa.total as total,
                                sa.sa_addisnal_amount as sa_addisnal_amount,
                                sa.total_with_addisnal_amount as total_with_addisnal_amount,
                                vehicle.name As vehicle_name,
                                partner.name AS driver_name,
                                company.name AS company_name,
                                vehicle.name AS vehicle_name,
                                city.name AS from_city,
                                city_to.name AS to_city,
                                sa.create_datetime AS datetime,
                                sa.state AS state, 
                                sa.id as sa_id
                            from
                                sa_truck as sa
                                LEFT JOIN vehicle_vehicle AS vehicle ON (vehicle.id = sa.vehicle_idd)
                                LEFT JOIN res_partner AS partner ON (partner.id = sa.driver_id)
                                LEFT JOIN res_company AS company ON (company.id = sa.company_id)
                                LEFT JOIN city_city AS city ON (city.id = sa.from_city_id)
                                LEFT JOIN city_city AS city_to ON (city_to.id = sa.to_city_id)
                            WHERE
                                sa.id IN (%s) and vehicle.id = sa.vehicle_idd and sa.state = sa.state
                            """%(acc_grp_res))
        result = self._cr.dictfetchall()
        res_list = []
        self._cr.execute("""SELECT 
                            checklist.id,
                            driver.id,
                            checklist.name AS checklist_name,
                            driver.unit_price AS unit_price,
                            driver.quantity AS quantity,
                            driver.subtotal AS sub_total,
                            driver.total_amount AS total_amount,   
                            sa.id as sa_id                    
                        from
                            sa_truck AS sa
                            JOIN driver_info AS driver ON (driver.satruck_id = sa.id)
                            JOIN check_list AS checklist ON (checklist.id = driver.checklist_id)
                        WHERE
                            sa.id IN (%s) and driver.unit_price <= checklist.unit_price
                        """%(acc_grp_res))
        # Structured Query Language
        result_check = self._cr.dictfetchall()
        for rec in result:
            chcek_list = []
            values={
                'sa_name':rec.get('name'),
                'sa_email':rec.get('email'),
                'sa_create_datetime' : rec.get('create_datetime'),
                'sa_total' : rec.get('total'),
                'sa_sa_addisnal_amount' : rec.get('sa_addisnal_amount'),
                'sa_total_with_addisnal_amount' : rec.get('total_with_addisnal_amount'),
                'sa_vehicle_name' : rec.get('vehicle_name'),
                'sa_driver_name' : rec.get('driver_name'),
                'sa_company_name' : rec.get('company_name'),
                'sa_from_city' : rec.get('from_city'),
                'sa_to_city' : rec.get('to_city'),
                'sa_state' : rec.get('state'),
            }
            print("((((((((((((((((values))))))))))))))))",values)
            for check in result_check:
                if rec.get('sa_id') == check.get('sa_id'):
                    check_vals = {
                        'check_list':check.get('checklist_name'),
                        'dri_unit_price' : check.get('unit_price'),
                        'dri_quantity' : check.get('quantity'),
                        'dri_subtotal' : check.get('sub_total'),
                        'dri_total_amount' : check.get('total_amount'),
                        # 'sa_tax_name' : rec.get('additional_amount'),
                    }
                    chcek_list.append(check_vals)
            print("(((((((((((((((check_list)))))))))))))))",chcek_list)
            values.update({
                'checklist_lines':chcek_list
            })
            res_list.append(values)
            print("(((((((((((((((((((values)))))))))))))))))))", values)
            print("(((((((((((((((((((((((((res list)))))))))))))))))))))))))",res_list)
        return res_list 

        # new_list = []
        # self._cr.execute( """ select name, create_datetime, km, email from sa_truck where id = %s """%(self.sa_truck_id.id))
        # new_list = self._cr.dictfetchall()
        # print("*****************",new_list)
        # return new_list
    def confirm(self):
        # return self.env.ref('sa_truck.action_sa_truck_quary_report').report_action(self,data=data)
        # sql = "SELECT * FROM sa_truck WHERE driver_id = %s AND manager_idd = %s"
        # params = (self.driver_id.id, self.manager_idd.id)
        # self.env.cr.execute(sql, params)
        # result = self.env.cr.fetchall()
        # print(result)
        data={
            'ids' : self.sa_truck_ids.ids,
            'data': self.read()[0],
            # 'vals':self._fetched_data(),
            'print_vals' : self._fetch_data()
        }
        return self.env.ref('sa_truck.action_sa_truck_quary_report').report_action(self,data=data)
    
class PdfReportQuaryWizard(models.AbstractModel):
    _name = "report.sa_truck.satruck_quary_report"
    _description = "Abstract Model in wizard print pdf Report Useing sql Quary"

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids'))
        print("vals............",data.get('vals'))  
        return {
            'doc_ids': docids,
            'doc_model': model,
            'docs': docs,
            'data': data,
            # 'vals':data['vals'],
            'print_vals':data['print_vals']
        }    