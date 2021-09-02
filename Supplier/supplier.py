from nameko.rpc import rpc

from dependencies import supplier_dependencies


class Supplier:
    name = 'supplier_service'

    database = supplier_dependencies.Database()

    @rpc
    def get_all_item(self):
        all_item = self.database.get_all_item()
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

    # @rpc
    # def get_all_purchase_order(self):
    #     all_purchase_order = self.database.get_all_purchase_order()
    #     return all_purchase_order

    # @rpc
    # def get_all_detail_purchase_order(self):
    #     all_detail_purchase_order = self.database.get_all_detail_purchase_order()
    #     return all_detail_purchase_order

    @rpc
    def get_supplier_by_id(self, id_supplier):
        supplier = self.database.get_supplier_by_id(id_supplier)
        return supplier