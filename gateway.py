import json

from nameko.rpc import Rpc, RpcProxy
from nameko.web.handlers import http

from werkzeug import Response

from Employee_Management import session_dependencies


class GatewayService:
    name = 'gateway'
    
    #GATEWAY KELOMPOK 1
    employee_rpc = RpcProxy('service_employee')
    session = session_dependencies.SessionProvider()


    @http('POST', '/api/login')
    def login(self, request):
        payload = json.loads(request.get_data(as_text=True))
        
        result = self.employee_rpc.login(payload['username'], payload['password'])

        response = Response(json.dumps(result), mimetype='application/json')
        if result['status']:
            response.set_cookie('session_id', result['session_id'])
        return response

    @http('GET', '/api/logout')
    def logout(self, request):
        session_id = request.cookies.get('session_id')
        result = self.employee_rpc.logout(session_id)

        response = Response(json.dumps(result), mimetype='application/json')
        if result['status']:
            response.set_cookie('session_id', result['session_id'])
        return response
    
    @http('GET', '/api/employee/check')
    def is_logged_in(self, request):
        session_id = request.cookies.get('session_id')
        result = self.employee_rpc.is_logged_in(session_id)
        response = Response(json.dumps({'status': result}), mimetype='application/json')
        return response

    @http('GET', '/api/employee')
    def get_all_employee(self, request):
        session_id = request.cookies.get('session_id')
        result = {
            'status': True,
            'err_msg': '',
            'data': []
        }

        if session_id == '' or session_id is None or (not self.employee_rpc.is_logged_in(session_id)):
            result['status'] = False
            result['err_msg'] = 'You need to login to access this API ' + str(self.session.get_all_online_user())
        else:
            result['data'] = self.employee_rpc.get_all_employee()
        response = Response(json.dumps(result), mimetype='application/json')
        return response

    @http('POST', '/api/forgot_password')
    def forgot_password(self, request):
        # id = request.json['id']
        # email = request.json['email']
        payload = json.loads(request.get_data(as_text=True))

        result = self.employee_rpc.forgot_password(payload['id'], payload['email'])
        response = Response(json.dumps(result), mimetype='application/json')
        return response

    @http('POST', '/api/employee')
    def get_employee_by_id(self, request, id):
        session_id = request.cookies.get('session_id')
        result = {
            'status': True,
            'err_msg': '',
            'data': []
        }

        if session_id == '' or session_id is None or (not self.employee_rpc.is_logged_in(session_id)):
            result['status'] = False
            result['err_msg'] = 'You need to login to access this API ' + str(self.session.get_all_online_user())
        else:
            result['data'] = self.employee_rpc.get_employee_by_id(id)
        response = Response(json.dumps(result), mimetype='application/json')
        return response

    # @http('POST', '/api/register/employee')
    # def register_employee(self, request):
    #     result = self.user_rpc.register_employee(request)
    #     response = Response(json.dumps({'status' : result}), mimetype='aplication/json')
    #     return response
    
    # @http('POST', '/api/register/employee/account')
    # def register_job(self, request):
    #     result = self.user_rpc.register_job(request)
    #     response = Response(json.dumps({'status' : result}), mimetype='aplication/json')
    #     return response

    # @http('POST', '/api/register/job')
    # def register_job(self, request):
    #     result = self.user_rpc.register_job(request)
    #     response = Response(json.dumps({'status' : result}), mimetype='aplication/json') 
    #     return response
    
    @http('POST', '/api/register/employee')
    def register_employee(self, request):
        payload = json.loads(request.get_data(as_text=True))
        result = self.employee_rpc.register_employee(payload)
        response = Response(json.dumps({'status' : result}), mimetype='aplication/json')
        return response
    
    @http('POST', '/api/register/employee/account')
    def register_account(self, request):
        payload = json.loads(request.get_data(as_text=True))
        result = self.employee_rpc.register_account(payload)
        response = Response(json.dumps({'status' : result}), mimetype='aplication/json')
        return response

    @http('POST', '/api/register/job')
    def register_job(self, request):
        payload = json.loads(request.get_data(as_text=True))
        result = self.employee_rpc.register_job(payload)
        response = Response(json.dumps({'status' : result}), mimetype='aplication/json') 
        return response


    @http('PUT', '/api/employee/edit/data')
    def edit_employee_data(self, request):
        # session_id = request.json['session_id']
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))

        result = self.employee_rpc.edit_employee_data(session_id, payload['id'], payload['name'], payload['birth'], payload['c_num'], payload['address'], payload['phone_num1'], payload['phone_num2'], payload['email'])
        response = Response(json.dumps(result), mimetype='application/json')
        return response

    @http('PUT', '/api/employee/edit/job')
    def edit_employee_job(self, request):
        # session_id = request.json['session_id']
        session_id = request.cookies.get('session_id')

        payload = json.loads(request.get_data(as_text=True))
        
        result = self.employee_rpc.edit_employee_job(session_id, payload['id'], payload['id_job'])
        response = Response(json.dumps(result), mimetype='application/json')
        return response
    
    @http('PUT', '/api/employee/edit/status')
    def edit_employee_status(self, request):
        # session_id = request.json['session_id']
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))
        
        result = self.employee_rpc.delete_employee(session_id, payload['id'])
        response = Response(json.dumps(result), mimetype='application/json')
        return response




    #GATEWAY KELOMPOK 2
    room_rpc = RpcProxy('room_service')
    room_orches_rpc = RpcProxy('room_orches_service')

    @http('GET', '/get/room_type')
    def get_room_type(self, request):
        roomtype = self.room_rpc.get_all_roomtype()
        return json.dumps(roomtype, default=str)
    
    @http('GET', '/get/room/<int:id_room>')
    def get_room(self, request, id_room):
        room = self.room_rpc.get_room_num(id_room)
        return json.dumps(room)

    @http('POST', '/add/room')
    def add_room(self, request):
        data = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        result = self.room_rpc.add_room(session_id, data['typeid'], data['roomnum'])
        return json.dumps(result)
    
    @http('POST', '/add/room_type')
    def add_room_type(self, request):
        data = json.loads(request.get_data(as_text=True))
        new_roomtype = self.room_rpc.add_roomtype(data['name'], data['price'], data['capacity'], data['last_update_by']) 
        return json.dumps(new_roomtype)

    @http('PUT', '/update/room')
    def update_room(self, request):
        data = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        updated_room = self.room_rpc.update_room(session_id, data['id_room'])
        return json.dumps(updated_room)

    @http('PUT', '/update/room_type')
    def update_room_type(self, request):
        data = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        roomtype = self.room_rpc.update_room_type(session_id, data['typeid'])
        return json.dumps(roomtype)

    @http('GET', '/get/check_in')
    def retrieve_check_in(self, request):
        session_id = request.cookies.get('session_id')
        result = self.room_orches_rpc.retrieve_check_in(session_id)
        return json.dumps(result)




    #GATEWAY KELOMPOK 3
    booking_rpc = RpcProxy('booking_service')
    booking_orches_rpc = RpcProxy('entry_booking_service')

    @http('GET', '/get/booking')
    def get_all_booking(self, request):
        session_id = request.cookies.get('session_id')
        check_login = self.employee_rpc.is_logged_in(session_id)
        if check_login:
            all_booking = self.booking_rpc.get_booking()
            return json.dumps(all_booking)
        else:
            return json.dumps ({
                'err_msg': 'You are not logged in yet',
                'status': False
            })

    @http('POST', '/add/booking')
    #room_type_name, start_date, end_date, description, service: name, qty
    def entry_booking(self, request):
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))
        entry_booking = self.booking_orches_rpc.entry_booking(session_id, payload['room_type_name'], payload['start_date'], payload['end_date'], payload['description'], payload['service'])
        return json.dumps(entry_booking)

    #change room type with higher hierarchy
    @http('PUT', '/update/booking')
    def update_booking_room(self, request):
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))
        update_booking = self.booking_orches_rpc.update_booking_room(session_id, payload['id_booking'], payload['new_room_type'])
        return json.dumps(update_booking)


    @http('PUT', '/update/booking_date')
    def update_booking_date(self, request):
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))
        update_booking = self.booking_rpc.update_booking_date(session_id, payload['id_booking'], payload['start_date'], payload['end_date'])
        return json.dumps(update_booking)


    @http('PUT', '/update/swap_booking_room')
    def swap_booking_room(self, request):
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))
        booking = self.booking_orches_rpc.swap_booking_room(session_id, payload['id_booking'])
        return json.dumps(booking)


    #sudah dipakai oleh kelompok 2 / room_service
    # @http('PUT', '/update/booking_status')
    # def update_booking_status(self, request):
    #     session_id = request.cookies.get('session_id')
    #     payload = json.loads(request.get_data(as_text=True))
    #     updated_booking = self.booking_rpc.update_booking_status(session_id, payload['id_booking'], payload['new_status'])
    #     return json.dumps(updated_booking)


    @http('GET', '/get/order_review/<string:citizen_num>')    
    def check_order_review(self, request, citizen_num):
        session_id = request.cookies.get('session_id')
        check_login = self.employee_rpc.is_logged_in(session_id)
        if check_login:
            booking = self.booking_orches_rpc.check_order_review(citizen_num)
            return json.dumps(booking)
        else:
            return json.dumps ({
                'err_msg': 'You are not logged in yet',
                'status': False
            })


    @http('GET', '/get/service')
    def get_all_service(self, request):
        session_id = request.cookies.get('session_id')
        check_login = self.employee_rpc.is_logged_in(session_id)
        if check_login:
            all_service = self.booking_rpc.get_service()
            return json.dumps(all_service)
        else:
            return json.dumps ({
                'err_msg': 'You are not logged in yet',
                'status': False
            })

    @http('POST', '/add/service')
    #name, cost, status
    def add_service(self, request):
        session_id = request.cookies.get('session_id')
        payload = json.loads(request.get_data(as_text=True))
        add_service = self.booking_rpc.add_service(session_id, payload['name'], payload['cost'], payload['status'])
        return json.dumps(add_service)

    @http('GET', '/get/customer')
    def get_customer(self, request):
        session_id = request.cookies.get('session_id')
        check_login = self.employee_rpc.is_logged_in(session_id)
        if check_login:
            all_customer = self.booking_rpc.get_customer()
            return json.dumps(all_customer)
        else:
            return json.dumps ({
                'err_msg': 'You are not logged in yet',
                'status': False
            })

    @http('GET', '/get/customer/<string:citizen_num>')
    def get_customer_by_citizenNum(self, request, citizen_num):
        session_id = request.cookies.get('session_id')
        check_login = self.employee_rpc.is_logged_in(session_id)
        if check_login:
            customer = self.booking_rpc.get_customer(ktp = citizen_num)
            return json.dumps(customer)
        else:
            return json.dumps ({
                'err_msg': 'You are not logged in yet',
                'status': False
            })
    
    @http('POST', '/add/customer')
    #name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status
    def add_customer(self, request):
        payload = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        add_customer = self.booking_rpc.add_customer(session_id, payload['name'], payload['citizen_number'], payload['date_of_birth'], payload['gender'], payload['address'], payload['email'], payload['phone_number1'], payload['phone_number2'], payload['status'])
        return json.dumps(add_customer)
    



    #GATEWAY KELOMPOK 4
    stock_management_rpc = RpcProxy('service_pelacakan')
    stock_management_orches_rpc = RpcProxy('stock_management_orchestration_service')

    @http('PUT', '/update/item')
    def update_item_status(self, request):
        payload = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        updated_item = self.stock_management_rpc.update_item_status(session_id, payload['id'], payload['status'])
        return json.dumps(updated_item)

    @http('GET', '/get/stock_management_report')
    def retrieve_stock_management_report(self, request):
        result = self.stock_management_orches_rpc.retrieve_stock_management_report()
        return json.dumps(result)


    #GATEWAY KELOMPOK 5
    circulation_rpc = RpcProxy('circulation_service')
    # circulation_rpc = RpcProxy('circulation_orchestration_service')
    
    @http('GET','/room_item_by_id/<int:id_room>/<int:id_item>')
    def get_room_item_by_id(self, request, id_room, id_item):
        room_item = self.circulation_rpc.get_room_item_by_id(id_room, id_item)
        return json.dumps({'result': room_item})

    # @http('POST', '/circulation')
    # def add_circulation_method(self, request):
    #     data = json.loads(request.get_data(as_text=True))
    #     new_circulaton = self.circulation_rpc.add_circulation_method(data['id_room'], data['id_item'],  data['session_id'], data['id_purchase'], data['qty'], data['status'])
    #     return new_circulaton
    
    @http('POST', '/circulation')
    def add_circulation(self, request):
        data = json.loads(request.get_data(as_text=True))
        new_circulaton = self.circulation_rpc.add_circulation(data['id_room'], data['id_item'],  data['id_employee'], data['id_purchase'], data['qty'], data['status'])
        return new_circulaton

    # #GATEWAY KELOMPOK 5
    # circulation_rpc = RpcProxy('circulation_service')
    # @http('GET','/api/room_item_by_id/<int:id_room>/<int:id_item>')
    # def get_room_item_by_id_method(self, request, id_room, id_item):
    #     room_item = self.circulation_rpc.get_room_item_by_id(id_room, id_item)
    #     return json.dumps({'result': room_item})

    # @http('POST', '/api/room_item')
    # def add_room_item_method(self, request):
    #     data = json.loads(request.get_data(as_text=True))
    #     new_room_item = self.circulation_rpc.add_room_item(data['id_room'], data['id_item'], data['qty'])
    #     return new_room_item

    # @http('POST', '/api/circulation')
    # def add_circulation_method(self, request):
    #     data = json.loads(request.get_data(as_text=True))
    #     new_circulaton = self.circulation_rpc.add_circulation(data['id_room'], data['id_item'],  data['id_employee'], data['id_purchase'], data['qty'], data['date'], data['status'])
    #     return new_circulaton


    #GATEWAY KELOMPOK 6
    supplier_rpc = RpcProxy('supplier_service')

    # @http('GET', '/api/item')
    # def get_all_item(self, request):
    #     all_item = self.supplier_rpc.get_all_item()
    #     return json.dumps(all_item)
    
    # @http('GET', '/api/item_type')
    # def get_all_item_type(self):
    #     all_item_type = self.supplier_rpc.get_all_item_type()
    #     return json.dumps(all_item_type)

    # @http('GET', '/api/supplier')
    # def get_all_supplier(self):
    #     all_supplier = self.supplier_rpc.get_all_supplier()
    #     return json.dumps(all_supplier)

    # @http('GET', '/api/catalog')
    # def get_all_catalog(self):
    #     all_catalog = self.supplier_rpc.get_all_catalog()
    #     return json.dumps(all_catalog)

    # @http('GET', '/api/purchase_order')
    # def get_all_purchase_order(self):
    #     all_purchase_order = self.supplier_rpc.get_all_purchase_order()
    #     return json.dumps(all_purchase_order)

    # @http('GET', '/api/detail_purchase_order')
    # def get_all_detail_purchase_order(self):
    #     all_detail_purchase_order = self.supplier_rpc.get_all_detail_purchase_order()
    #     return json.dumps(all_detail_purchase_order)

    @http('GET', '/api/item')
    def get_all_item(self, id, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by):
        all_item = self.catalog_rpc.get_all_item(id, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by)
        return json.dumps(all_item)

    @http('GET', '/api/item_type')
    def get_all_item_type(self, id, name, status):
        all_item_type = self.catalog_rpc.get_all_item_type(id, name, status)
        return json.dumps(all_item_type)

    @http('GET', '/api/supplier')
    def get_all_supplier(self, id, name, address, phone_number2, phone_number1, email, status, last_update, last_update_by):
        all_supplier = self.catalog_rpc.get_all_supplier(id, name, address, phone_number2, phone_number1, email, status, last_update, last_update_by)
        return json.dumps(all_supplier)

    @http('GET', '/api/catalog')
    def get_all_catalog(self, id, id_type, id_supplier, date, unit, price_per_unit, status, last_update, last_update_by):
        all_catalog = self.catalog_rpc.get_all_catalog(id, id_type, id_supplier, date, unit, price_per_unit, status, last_update, last_update_by)
        return json.dumps(all_catalog)

    # @http('GET', '/api/purchase_order')
    # def get_all_purchase_order(self, id, id_employee, id_supplier, date, status):
    #     all_purchase_order = self.catalog_rpc.get_all_purchase_order(id, id_employee, id_supplier, date, status)
    #     return json.dumps(all_purchase_order)

    @http('GET', '/api/detail_purchase_order')
    def get_all_detail_purchase_order(self, id, id_item, id_purchase, qty, unit, price_per_unit):
        all_detail_purchase_order = self.catalog_rpc.get_all_detail_purchase_order(id, id_item, id_purchase, qty, unit, price_per_unit)
        return json.dumps(all_detail_purchase_order)

    #GATEWAY KELOMPOK 7
    a_rpc = RpcProxy('accident_service')

    @http('POST', '/api/accident')
    def create_accident(self, request):
        payload = json.loads(request.get_data(as_text=True))
        accident = self.a_rpc.create_accident(payload['id_booking'], payload['id_employee'], payload['description'], payload['compensation'], payload['compensation_cost'])
        return json.dumps(accident)

    @http('GET', '/api/accident/compensation')
    def get_compensation(self,request):
        payload = json.loads(request.get_data(as_text=True))
        compensation = self.a_rpc.get_compensation(payload['id_booking'])
        return json.dumps(compensation)

    @http('GET', '/api/accident_report/')
    def get_accident_report(self, request):
        payload = json.loads(request.get_data(as_text=True))
        accident_report = self.a_rpc.get_accident_report(payload['start_date'], payload['end_date'])
        return json.dumps(accident_report)

    @http('PUT', '/api/accident/')
    def update_accident(self, request):
        payload = json.loads(request.get_data(as_text=True))
        update_accident = self.a_rpc.update_accident(payload['id_accident'], payload['status'])
        return json.dumps(update_accident)

    @http('GET', '/api/accident/')
    def get_all_accident(self, request):
        accident = self.a_rpc.get_all_accident()
        return json.dumps(accident)
    
    #GATEWAY KELOMPOK 8
    po_rpc = RpcProxy('po_service')
    po_orches_rpc = RpcProxy('po_orchestration_service')

    @http('GET', '/api/purchase_order')
    def get_po(self, request):
        session_id = request.cookies.get('session_id')
        check_login = self.employee_rpc.is_logged_in(session_id)
        if check_login:
            po = self.po_rpc.get_all_po()
            return json.dumps(po)
        else:
            return json.dumps ({
                'err_msg': 'You are not logged in yet',
                'status': False
            })

    
    @http('GET', '/api/purchase_order_report/<int:purchase_id>')
    def get_report(self, request, purchase_id):
        report = self.po_orches_rpc.get_report(purchase_id)
        return json.dumps(report)


    @http('POST', '/api/purchase_order')
    def create_po(self, request):
        payload = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        new_po = self.po_orches_rpc.create_po(session_id, payload['id_supplier'], payload['detail_purchase_order'])
        return json.dumps(new_po)

    @http('PUT', '/api/status_purchase_order/<int:purchase_id>')
    def change_status_po(self, request, purchase_id):
        payload = json.loads(request.get_data(as_text=True))
        session_id = request.cookies.get('session_id')
        change_status = self.po_rpc.change_status_po(session_id, purchase_id, payload['status'])
        return json.dumps(change_status)

    @http('PUT', '/api/purchase_order/<int:purchase_id>')
    def edit_po(self, request, purchase_id):
        payload = json.loads(request.get_data(as_text=True))
        edit = self.po_rpc.edit_po(purchase_id, payload['id_employee'], payload['id_supplier'], payload['status'])
        return json.dumps(edit)

    @http('DELETE', '/api/purchase_order/<string:id>')
    def delete_po(self, request, id):
        result = self.po_rpc.delete_po(id)
        return result
