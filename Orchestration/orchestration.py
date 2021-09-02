from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler 
import json,sys

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies

class EntryDataBooking:
    name = 'entry_booking_service'
    room_service = RpcProxy('room_service')
    booking_service = RpcProxy('booking_service')


    session = session_dependencies.SessionProvider()
    
    #orchestration
    @rpc
    def entry_booking(self, session_id, room_type_name, start_date, end_date, description, services):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)

            id_room_type = self.room_service.get_room_type_by_name(room_type_name)[0]['id'] 
            room = self.room_service.get_room_by_type(id_room_type)

            check = False
            for room_info in room:
                print (room_info['id'])
                check_booking_sebelumnya = self.booking_service.get_booking_by_room(room_info['id'], start_date, end_date)
                if check_booking_sebelumnya == True:
                    insert_data = self.booking_service.add_booking(1, id_room_type, room_info['id'], data['id_employee'], start_date, end_date, description, 0)
                    for service in services:
                        service_from_db = self.booking_service.get_service(service_name = service['name'])
                        price = service_from_db['cost']
                        self.booking_service.add_detail_booking(service_from_db['id'], insert_data['id'], service['qty'], service['qty']*price)                        
                    
                    check = True
                    break
                
            if check == False:
                err_msg = 'Maaf, kamar tidak tersedia untuk saat ini'
                result = ''
                status = False
                
            elif check == True:
                err_msg = ''
                result = insert_data
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
    def swap_booking_room(self, session_id, id_booking):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        booking_data = self.booking_service.get_booking(id_booking = id_booking)
        if booking_data['status'] <= 0:
            if stat:
                data = self.session.get_session_data(session_id)
                id_room_type = self.booking_service.get_booking(id_booking = id_booking)['id_room_type']
                start_date = booking_data['start_date']
                end_date = booking_data['end_date']
                room = self.room_service.get_room_by_type(id_room_type) 
                
                check = False
                for room_info in room:
                    print (room_info['id'])
                    check_booking_sebelumnya = self.booking_service.get_booking_by_room(room_info['id'], start_date, end_date)
                    if check_booking_sebelumnya == True:
                        update_data = self.booking_service.update_booking_room(id_booking, room_info['id'], id_room_type, data['id_employee'])
                        check = True
                        break
                    
                if check == False:
                    result = ""
                    err_msg = "Maaf, penukaran kamar tidak tersedia untuk saat ini"
                    status = False
                    # return {'status': 0, 'message': 'Maaf, penukaran kamar tidak tersedia untuk saat ini'}
                elif check == True:
                    result = update_data
                    err_msg = ""
                    status = True
                    # return update_data
            
            else:
                err_msg = 'You are not logged in'
                result = ''
                status = False
        else:
            err_msg = "Pelanggan yang bersangkutan sudah menginap atau telah menyelesaikan transaksi. Penukaran tidak dapat dilakukan."
            result = ''
            status = False
        
        return {
            "result": result,
            "err_msg": err_msg,
            "status": status
        }

    @rpc
    def update_booking_room(self, session_id, id_booking, room_type_new):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)

        booking_data = self.booking_service.get_booking(id_booking = id_booking)

        if booking_data['status'] <= 0:
        
            if stat:
                data = self.session.get_session_data(session_id)
                id_room_type = self.room_service.get_room_type_by_name(room_type_new)[0]['id']
                room = self.room_service.get_room_by_type(id_room_type)
                
                start_date = booking_data['start_date']
                end_date = booking_data['end_date']

                check = False
                for room_info in room:
                    print (room_info['id'])
                    check_booking_sebelumnya = self.booking_service.get_booking_by_room(room_info['id'], start_date, end_date)
                    if check_booking_sebelumnya == True:
                        update_data = self.booking_service.update_booking_room(id_booking, room_info['id'], id_room_type, data['id_employee'])                 
                        check = True
                        break
                    
                if check == False:
                    err_msg = 'Maaf, penukaran tipe kamar tidak tersedia untuk saat ini'
                    result = ''
                    status = False
                elif check == True:
                    err_msg = ''
                    result = update_data
                    status = True
            else:
                err_msg = 'You are not logged in'
                result = ''
                status = False
        else:
            err_msg = "Pelanggan yang bersangkutan sudah menginap atau telah menyelesaikan transaksi. Penukaran tidak dapat dilakukan."
            result = ""
            status = False
        return {
            "result": result,
            "err_msg": err_msg,
            "status": status
        }

    
    @rpc
    def check_order_review(self, ktp):

        customer_data = self.booking_service.get_customer(ktp = ktp)
        id_customer = customer_data['id']
        customer_name = customer_data['name']
        
        result = {
            "cust_id": id_customer,
            "cust_name": customer_name,
            "booking": []
        }

        booking_data = self.booking_service.get_booking(id_customer = id_customer)
        i = 0
        for booking in booking_data:    
            room_number = self.room_service.get_room_num(booking['id_room'])['room_number']
            room_type = self.room_service.get_room_type_by_id(booking['id_room_type'])['name']
            result['booking'].append(
                {
                    "room_number": room_number,

                    "room_type": room_type,
                    "booking_date": booking['booking_date'],
                    "start_date": booking['start_date'],
                    "end_date": booking['end_date'],
                    "description": booking['description'],
                    "services": []
                }
            )
            detail_booking = self.booking_service.get_detail_booking(id_booking = booking['id'])
            
            for detail in detail_booking:
                service_data = self.booking_service.get_service(id_service = detail['id_service'])
                result['booking'][i]['services'].append(
                    {
                        "service_name": service_data['name']
                    }
                )
            
            i = i+1
    
        return result