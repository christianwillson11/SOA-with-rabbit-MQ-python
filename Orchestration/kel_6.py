from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler


class OrchestrationService:
    name = "catalog_orchestration_service"

    catalog = RpcProxy('catalog')

    # Publish Subscribe
    dispatch = EventDispatcher()

    result1 = {
        'all_item': None
    }
    result2 = {
        'all_item_type': None
    }
    result3 = {
        'all_supplier': None
    }
    result4 = {
        'all_catalog' : None
    }
    result5 = {
        'all_purchase_order' : None
    }
    result6 = {
        'all_detail_purchase_order' : None
    }

    # Cth Pub Subs
    @rpc
    def dispatch_method(self, payload):
        self.dispatch("catalog_event", payload)

    # Orchestration
    @rpc
    def get_all_item(self, id, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by):
        result1 = {
            'all_item': self.catalog.get_all_item(id, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by),
        }
        return result1

    # Orchestration
    @rpc
    def get_all_item_type(self, id, name, status):
        result2 = {
            'all_item_type': self.catalog.get_all_item_type(id, name, status)
        }
        return result2

    # Orchestration
    @rpc
    def get_all_supplier(self, id, name, address, phone_number2, phone_number1, email, status, last_update, last_update_by):
        result3 = {
            'all_supplier': self.catalog.get_all_supplier(id, name, address, phone_number2, phone_number1, email, status, last_update, last_update_by)
        }
        return result3

        # Orchestration

    @rpc
    def get_all_catalog(self, id, id_type, id_supplier, date, unit, price_per_unit, status, last_update,
                         last_update_by):
        result4 = {
            'all_catalog': self.catalog.get_all_catalog(id, id_type, id_supplier, date, unit, price_per_unit,
                                                             status, last_update, last_update_by)
        }
        return result4

        # Orchestration

    @rpc
    def get_all_purchase_order(self, id, id_employee, id_supplier, date, status):
        result5 = {
            'all_purchase_order': self.catalog.get_all_purchase_order(id, id_employee, id_supplier, date, status)
        }
        return result5

        # Orchestration

    @rpc
    def get_all_detail_purchase_order(self, id, id_item, id_purchase, qty, unit, price_per_unit):
        result6 = {
            'all_detail_purchase_order': self.catalog.get_all_detail_purchase_order(id, id_item, id_purchase, qty, unit, price_per_unit)
        }
        return result6


# Codingan lama
    # from nameko.rpc import Rpc, rpc, RpcProxy
    # from nameko.events import EventDispatcher, event_handler 

    # class OrchestrationService:
    #     name = "supplier_orchestration_service"

    #     supplier_service = RpcProxy('supplier_service')
    #     stock_management_service = RpcProxy('service_pelacakan')
        
    #     @rpc
    #     def pemilihan_unit_barang_dan_jumlah(self):
    #         all_catalog = self.supplier_service.get_all_catalog()
            
    #         result = []
    #         for catalog in all_catalog:
    #             result.append(
    #                 {
    #                     'id': catalog['id'],
    #                     'item': self.stock_management_service.get_item_by_id(catalog['id_item'])['name'],
    #                     'date': catalog['date'],
    #                     'unit': catalog['unit'],
    #                     'price_per_unit': catalog['price_per_unit'],
    #                     'status': catalog['status']
    #                 }
    #             )
    #         return result

    #     @rpc
    #     def pengecekan_catalog_supplier(self):
    #         all_catalog = self.supplier_service.get_all_catalog()
            
    #         result = []
    #         for catalog in all_catalog:
    #             result.append(
    #                 {
    #                     'id': catalog['id'],
    #                     'item': self.stock_management_service.get_item_by_id(catalog['id_item'])['name'],
    #                     'supplier': self.supplier_service.get_supplier_by_id(catalog['id_supplier'])['name'],
    #                     'date': catalog['date'],
    #                     'unit': catalog['unit'],
    #                     'price_per_unit': catalog['price_per_unit'],
    #                     'status': catalog['status']
    #                 }
    #             )
    #         return result

    