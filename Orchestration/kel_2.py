from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler 
import json,sys

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies

class EntryDataBooking:
    name = 'room_orches_service'
    room_service = RpcProxy('room_service')
    booking_service = RpcProxy('booking_service')
    employee_service = RpcProxy('service_employee')


    session = session_dependencies.SessionProvider()
    
    #orchestration
    @rpc
    def update_booking_status(self, session_id, id_booking, status):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            updated_booking = self.booking_service.update_booking_status(id_booking, status, data['id_employee'])
            return updated_booking
        else:
            err_msg = 'You are not logged in'
            result = ''
            status = False
        
        return {
            "result": result,
            "err_msg": err_msg,
            "status": status
        }

    #menerima laporan check-in
    @rpc
    def retrieve_check_in(self, session_id):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            all_booking_data = self.booking_service.get_booking()
            result = []
            for booking in all_booking_data:
                if booking['status'] == 0:
                    result.append(
                        {
                            "Employee In Charge": self.employee_service.get_employee_by_id(booking['id_employee'])['name'],
                            "Check In Room Number": self.room_service.get_room_by_id(booking['id_room'])['room_number']
                        }
                    )
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