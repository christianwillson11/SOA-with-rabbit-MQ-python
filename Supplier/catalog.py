from nameko.rpc import rpc

from dependencies import catalogdependencies


class Catalog:
    name = 'catalog_service'

    database = catalogdependencies.Database()

    @rpc
    def get_all_item(self, id, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by):
        all_item = self.database.get_all_item(id, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by)
        return all_item

    @rpc
    def get_all_item_type(self):
        all_item_type = self.database.get_all_item_type()
        return all_item_type

    @rpc
    def get_all_supplier(self):
        all_supplier = self.database.get_all_supplier()
        return all_supplier

    @rpc
    def get_all_catalog(self):
        all_catalog = self.database.get_all_catalog()
        return all_catalog

    @rpc
    def get_all_purchase_order(self):
        all_purchase_order = self.database.get_all_purchase_order()
        return all_purchase_order

    @rpc
    def get_all_detail_purchase_order(self):
        all_detail_purchase_order = self.database.get_all_detail_purchase_order()
        return all_detail_purchase_order