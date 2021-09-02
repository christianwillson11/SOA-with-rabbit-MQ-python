from nameko.rpc import rpc
import sys

from dependencies import booking_dependencies

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies


class BookingService:
    name = 'booking_service'

    database = booking_dependencies.Database()
    session = session_dependencies.SessionProvider()

    # @rpc
    # def add_customer(self, session_id, name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status):
    
        # err_msg = ''
        # stat = self.session.is_employee_online(session_id)
        # if stat:
        #     data = self.session.get_session_data(session_id)
    #         customer = self.database.add_customer(name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, data['id_employee'])
    #         return customer
    #     else:
    #         err_msg = 'You are not logged in'
    #         result = ''
    #         status = False
    #     return {
    #         "result": result,
    #         "err_msg": err_msg,
    #         "status": status
    #     }

    @rpc
    def get_customer(self, id=-1, ktp=-1):
        customer = self.database.get_customer(id, ktp)
        return customer

    
    @rpc
    def add_booking (self, id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status):
        booking = self.database.add_booking(id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status)
        return booking
    
    
    @rpc
    def update_booking_room(self, id_booking, id_room_new, id_room_type_new, id_employee):
        updated_booking = self.database.update_booking_room(id_booking, id_room_new, id_room_type_new, id_employee)
        return updated_booking

    @rpc
    def update_booking_date(self, session_id, id_booking, start_date, end_date):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            stat = self.database.get_booking_by_room(self.database.get_booking(id_booking,-1)['id_room'], start_date, end_date)
            if stat == True :
                updated_booking = self.database.update_booking_date(id_booking, start_date,end_date, data['id_employee'])
                return updated_booking
            else :
                return {
                    "result": '',
                    "err_msg": 'Pergantian tidak dapat dilakukan pada tanggal bersangkutan',
                    "status": False
                }
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
    def update_booking_status(self, id_booking, status, id_employee):
        updated_booking = self.database.update_booking_status(id_booking, status, id_employee)
        return updated_booking

   

    @rpc
    def get_booking(self, id_booking=-1, id_customer=-1):
        booking = self.database.get_booking(id_booking, id_customer)
        return booking
    
    
    @rpc
    def get_booking_by_room(self, id_room, start_date, end_date):
        booking = self.database.get_booking_by_room(id_room, start_date, end_date)
        return booking


    @rpc
    def get_detail_booking(self, id_booking=-1):
        detail_booking = self.database.get_detail_booking(id_booking)
        return detail_booking

    @rpc
    def add_detail_booking (self, id_service, id_booking, qty, price):
        detail_booking = self.database.add_detail_booking(id_service, id_booking, qty, price)
        return detail_booking

    @rpc
    def add_service (self, session_id, name, cost, status):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            service = self.database.add_service(name, cost, status, data['id_employee'])
            err_msg = ''
            result = service
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
    def get_service(self, id_service=-1, service_name=-1):
        service = self.database.get_service(id_service, service_name)
        return service
