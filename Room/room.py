from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from nameko.web.handlers import http
import json, sys

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies


from dependencies import room_dependencies

class RoomService:
    name = 'room_service'

    db = room_dependencies.DBProvider()
    session = session_dependencies.SessionProvider()
    
    dispatch=EventDispatcher()
    @event_handler("orchestration_service", "room_event")
    def handle_event_method(self, payload):
        print(payload)

    @rpc
    def get_room_by_id(self, id_room):
        result = self.db.get_room_by_id(id_room)
        self.db.close_connection()
        return result
    
    @rpc
    def get_room_type_by_name(self, room_type_name):
        room_type = self.db.get_room_type_by_name(room_type_name)
        self.db.close_connection()
        return room_type

    @rpc
    def get_room_by_type(self, id_room_type):
        room = self.db.get_room(id_room_type)
        self.db.close_connection()
        return room
    
    @rpc
    def get_room_type_by_id (self, id_room_type):
        room_type = self.db.get_room_type_by_id(id_room_type)
        self.db.close_connection()
        return room_type


    @rpc
    def get_all_roomtype(self):
        result = self.db.get_all_room_type()
        self.db.close_connection()
        return result

    #ini diletakkan di gateway (UPDATE ROOM TYPE)
    @rpc
    def update_room_type(self, session_id, typeid):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            result = self.db.update_room_type(typeid, data['id_employee'])
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
    def add_roomtype(self, _name, _price, _capacity, _last_update_by):
        result = self.db.add_room_type(_name, _price, _capacity, _last_update_by)
        self.db.close_connection()
        return result

    @rpc
    def delete_room_type(self, typeid):
        result = self.db.delete_room_type(typeid)
        self.db.close_connection()
        return result

    @rpc
    def get_count_room(self):
        result = self.db.get_count_room()
        self.db.close_connection()
        return result

    #ini diletakkan di gateway (UPDATE ROOM STATUS)
    @rpc
    def update_room(self, session_id, roomid):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            result = self.db.update_room(roomid, data['id_employee'])
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
    def add_room(self, session_id, typeid, roomnum):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            result = self.db.add_room(typeid, roomnum, data['id_employee'])
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
    def delete_room(self, roomid):
        result = self.db.delete_room(roomid)
        self.db.close_connection()
        return result

    @rpc
    def get_room_num(self, roomid):
        result = self.db.get_room_num(roomid)
        self.db.close_connection()
        return result

    @rpc
    def update_cancel_room(self, typeid, idlogin):
        result = self.db.update_cancel_room(typeid, idlogin)
        self.db.close_connection()
        return result

    @rpc
    def update_cancel_room_bybooking(self, idbook, idlogin):
        result = self.db.update_cancel_room_by_booking(idbook, idlogin)
        self.db.close_connection()
        return result