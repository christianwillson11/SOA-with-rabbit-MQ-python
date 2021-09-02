from nameko.rpc import rpc
import sys

from dependencies import db_dependencies

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies

class ServiceUser:
    
    name = "service_pelacakan"

    db = db_dependencies.DBProvider()
    session = session_dependencies.SessionProvider()


    @rpc
    def get_all_item(self):
        result = self.db.get_all_item()
        self.db.close_connection()
        return result

    @rpc
    def get_item_by_id(self, id):
        result = self.db.get_item_by_id(id)
        self.db.close_connection()
        return result
    
    @rpc
    def get_all_itemtype(self):
        result = self.db.get_all_itemtype()
        self.db.close_connection()
        return result

    @rpc
    def get_itemtype_by_id(self, id):
        result = self.db.get_itemtype_by_id(id)
        self.db.close_connection()
        return result

    ##here
    @rpc
    def update_item_status(self, session_id, id, status):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            result = self.db.update_item_status(id, status, data['id_employee'])
            self.db.close_connection()
            status = True
        else:
            err_msg = 'You are not logged in'
            result = ''
            status = False
        
        return {
            "result": result,
            "err_msg": err_msg,
            "status": status
        }

    @rpc
    def update_item2(self, id_item, qty_in_hand, unit, employee_id):
        result = self.db.update_item2(id_item, qty_in_hand, unit, employee_id)
        self.db.close_connection()
        return result


    # @rpc
    # def delete_item_by_id(self,id,employeeid):
    #     result = self.db.delete_item_by_id(id,employeeid)
    #     self.db.close_connection()
    #     return result

    @rpc
    def insert_item(self,id_type,name,barcode,qty_in_hand,qty_broken,qty_lost,unit,status,employeeid):
        result = self.db.insert_item(id_type,name,barcode,qty_in_hand,qty_broken,qty_lost,unit,status,employeeid)
        self.db.close_connection()
        return result

    @rpc
    def insert_itemtype(self,name,status):
        result = self.db.insert_itemtype(name,status)
        self.db.close_connection()
        return result

    # @rpc
    # def update_itemtype(self,name,status):
    #     result = self.db.update_itemtype(name,status)
    #     self.db.close_connection()
    #     return result

    # @rpc
    # def delete_itemtype_by_id(self,id):
    #     result = self.db.delete_itemtype_by_id(id)
    #     self.db.close_connection()
    #     return result

    # View laporan masih get all, belum bentuk laporan
    @rpc
    def view_laporan(self):
        result = self.db.get_all_item()
        self.db.close_connection()
        return result
