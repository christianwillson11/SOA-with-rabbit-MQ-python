import json
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from nameko.web.handlers import http

from dependencies import circulation_dependencies

class CirculationService:
    name="circulation_service"
    

    database = circulation_dependencies.Database()   

    #Publish Subscribe
    dispatch = EventDispatcher()

    #Handle Event  (Orchestration)
    @event_handler("orchestration_service", "circulation_event")
    def handle_event_method(self, payload):
        print(payload)

    @rpc
    def get_room_item_by_id(self, id_room, id_item):
        room_item = self.database.get_room_item_by_id(id_room, id_item)
        return room_item

    @rpc
    def add_room_item(self, id_room, id_item, qty):
        new_room_item = self.database.add_room_item(id_room, id_item, qty)
        return new_room_item

    @rpc
    def add_circulation(self, id_room, id_item, id_employee, id_purchase, qty, status):
        new_circulation = self.database.add_circulation(id_room, id_item, id_employee, id_purchase, qty, status)
        return new_circulation

    