from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher

from dependencies import po_dependencies

# Status Purchase Order
# 1 = CREATED
# 2 = ACCEPTED
# 3 = DELIVERED
# 4 = FINISHED
# 5 = REJECTED

class PurchaseOrderService:

    name = 'po_service'

    database = po_dependencies.Database()
    dispatch = EventDispatcher()

    @rpc
    def get_all_po(self):
        purchase_order = self.database.get_all_po()
        return purchase_order

    @rpc
    def get_po_by_id(self, purchase_id):
        purchase_order = self.database.get_po_by_id(purchase_id)
        detail_purchase_order = self.database.get_detail_po_by_id(purchase_id)
        result = [purchase_order, detail_purchase_order]
        return result

    @rpc
    def create_po(self, id_employee, id_supplier, detail_purchase_order):
        
        purchase_order = self.database.create_po(id_employee, id_supplier, detail_purchase_order)
        return purchase_order
    
    @rpc
    def get_detail_po_by_id(self, purchase_id):
        detail_purchese_order = self.database.get_detail_po_by_id(purchase_id)
        return detail_purchese_order

    @rpc
    def create_detail_po(self, detail_purchase_order):
        result = self.database.create_detail_po(detail_purchase_order)
        return result

    @rpc
    def change_status_po(self, session_id, id, status):
        if status == 3:
            status_asal = self.database.get_po_by_id(id)
            change_status_po = self.database.change_status_po(id, status)
            if status_asal['status'] != 3:
                # Run PubSub
                # result = self.po_orchestration.circulation_item(id)
                # return result
                payload = [session_id, id]
                self.dispatch("circulation_item_event", payload)
            else:
                return "Status sudah 3"
        else:
            change_status_po = self.database.change_status_po(id, status)
        return change_status_po

    @rpc
    def edit_po(self, id, id_employee, id_supplier, status):
        purchase_order = self.database.edit_po(id, id_employee, id_supplier, status)
        return purchase_order

    @rpc
    def delete_po(self, id):
        result = self.database.delete_po(id)
        return result