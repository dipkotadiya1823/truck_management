from odoo import http
from odoo.http import request

class SA_Truck(http.Controller):

    @http.route('/sa_truck/driver/', website=True, auth="public")
    def sa_truck_driver(self, **kw):
        driver = request.env['sa.truck'].sudo().search([])

        return request.render("sa_truck.sa_truck_model_controller",{
            'driver': driver,  
        })
    
    @http.route('/sa_truck/email/', website=True, auth="public")
    def sa_truck_driver_email(self, **kw):
        email = request.env['sa.truck'].sudo().search([])

        return request.render("sa_truck.sa_truck_model_email_controller",{
            'email' : email
        })

    @http.route('/sa_truck', website=True, auth="public")
    def sa_truck_menu(self, **kw):
        return http.request.render("sa_truck.sa_truck_driver_tripform",{})
    
    @http.route('/create/sa_truck_thanks', website=True, auth="public")
    def create_driver_trip_record(self, **kw):
        show = request.env['sa.truck'].sudo().create(kw)
        return request.render("sa_truck.sa_truck_creted_driver_trip_record",{})