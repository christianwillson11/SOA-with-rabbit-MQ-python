from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler 
import json,sys

sys.path.insert(1, 'C:/Users/sedji/Downloads/Zetra Hotel Microservice/Employee_Management')
import session_dependencies

class OrchestrationService:
    name = "circulation_orchestration_service"

    circulation_service = RpcProxy('circulation_service')
    
    session = session_dependencies.SessionProvider()

    #Publish Subscribe
    dispatch = EventDispatcher()

    result1 = {
        'add_circulation_result': None
    }
    result2 = {
        'add_room_item_result': None
    }
    result3 = {
        'room_item_by_id': None
    }

    #Cth Pub Subs
    @rpc 
    def dispatch_method(self, payload):
        self.dispatch("circulation_event", payload)

    # Orchestration
    @rpc
    def add_circulation_method(self, id_room, id_item, session_id, id_purchase, qty, status):
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            new_circulation = self.add_circulation(id_room, id_item, data['id_employee'], id_purchase, qty, status)
            return new_circulation
        else:
            err_msg = 'You are not logged in'
            return err_msg