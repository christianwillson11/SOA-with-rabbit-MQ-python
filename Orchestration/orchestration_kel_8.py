from nameko.rpc import rpc, RpcProxy
from nameko.events import event_handler
import json
import sys

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies

class PO_Orchestration:
    name = 'po_orchestration_service'
    session = session_dependencies.SessionProvider()

    po_service = RpcProxy('po_service')
    supplier_service = RpcProxy('supplier_service')
    employee_service = RpcProxy('service_employee')
    item_service = RpcProxy('service_pelacakan')

    # PubSub for circulation
    @event_handler("po_service", "circulation_item_event")
    def handle_circulation_item(self, payload):
        stat = self.session.is_employee_online(payload[0])
        #stat = True
        if stat:
            data = self.session.get_session_data(payload[0])
            detail_purchase_order = self.po_service.get_detail_po_by_id(payload[1])
            for detail in detail_purchase_order:
                self.item_service.update_item2(detail['id_item'], detail['qty'], detail['unit'], data['id_employee'])
            return "Circulation success"
        else:
            return {
                "result": '',
                "err_msg": "You are not logged in",
                "status": False
            }
            

    #Orchestration purchase order
    @rpc
    def create_po(self, session_id, supplier_id, detail_purchase_order):
          
        stat = self.session.is_employee_online(session_id)

        if stat:
            data = self.session.get_session_data(session_id)

            check_employee = bool(self.employee_service.get_employee_by_id(data['id_employee']))
            check_supplier = bool(self.supplier_service.get_supplier_by_id(supplier_id))      

            if check_employee == True and check_supplier == True:
                result = self.po_service.create_po(data['id_employee'], supplier_id, detail_purchase_order)
                return result
            else:
                return "Employee or supplier invalid"
        else:
            return {
                "result": '',
                "err_msg": "You are not logged in",
                "status": False
            }

    @rpc
    def get_report(self, purchase_id):
        purchase_order = self.po_service.get_po_by_id(purchase_id)
        detail_purchase_order = self.po_service.get_detail_po_by_id(purchase_id)
        detail_po_result = []
        for detail in detail_purchase_order:
            item = self.item_service.get_item_by_id(detail['id_item'])
            detail_result = {
                "name" : item['name'],
                "barcode" : item['barcode'],
                "quantity" : detail['qty'],
                "unit" : detail['unit'],
                "price_per_unit" : detail['price_per_unit']
            }
            detail_po_result.append(detail_result)

        employee = self.employee_service.get_employee_by_id(purchase_order[0]['id_employee'])
        supplier = self.supplier_service.get_supplier_by_id(purchase_order[0]['id_supplier'])
        result = {
            "date" : purchase_order[0]['date'],
            "employee" : {
                "name" : employee['name'],
                "date_of_birth" : employee['date_of_birth'],
                "citizen_number" : employee['citizen_number'],
                "gender" : employee['gender'],
                "address" : employee['address'],
                "phone_number_1" : employee['phone_number1'],
                "phone_number_2" : employee['phone_number2'],
                "email" : employee['email']
            },
            "supplier" : {
                "name" : supplier['name'],
                "address" : supplier['address'],
                "phone_number_1" : supplier['phone_number1'],
                "phone_number_2" : supplier['phone_number2'],
                "email" : supplier['email']
            },
            "detail_purchase_order" : detail_po_result
        }
        
        return result