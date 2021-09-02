from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler 

class OrchestrationService:
    name = "stock_management_orchestration_service"

    stock_management_service = RpcProxy('service_pelacakan')
    circulation_service = RpcProxy('circulation_service')
    room_service = RpcProxy('room_service')

    #Pengecekan barang pada gudang
    @rpc
    def check_item_at_storage(self):
        all_items = self.stock_management_service.get_all_item()
        result = []
        for item in all_items:
            result.append(
                {
                    "id": item['id'],
                    "type": self.stock_management_service.get_itemtype_by_id(item['id_type'])['name'],
                    "name": item['name'],
                    "barcode": item['barcode'],
                    "qty_in_hand": item['qty_in_hand'],
                    "qty_broken": item['qty_broken'],
                    "qty_lost": item['qty_lost'],
                    "unit": item['unit'],
                    "status": item['status']
                }
            )
        return result

    #menerima laporan stock management
    @rpc
    def retrieve_stock_management_report(self):
        all_items = self.stock_management_service.get_all_item()
        result = []
        i = 0
        for item in all_items:
            result.append(
                {
                    "id": item['id'],
                    "name": item['name'],
                    "barcode": item['barcode'],
                    "In-Room": []
                }
            )
            all_room_item = self.circulation_service.get_room_item_by_id(item['id'])

            for item in all_room_item:
                result[i]['In-Room'].append(
                    {
                        'Room Number': self.room_service.get_room_by_id(item['id_room'])['room_number'],
                        'Qty-in-room': item['qty']
                    }
                )
            i = i+1
        return result
