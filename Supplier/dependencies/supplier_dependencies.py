from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    def __init__(self, connection):
        self.connection = connection

    def get_all_item(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM item"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'id_type': row['id_type'],
                'name': row['name'],
                'barcode': row['barcode'],
                'qty_in_hand': row['qty_in_hand'],
                'qty_broken': row['qty_broken'],
                'qty_lost': row['qty_lost'],
                'unit': row['unit'],
                'status': row['status'],
                'last_update': row['last_update'],
                'last_update_by': row['last_update_by']
            })
        cursor.close()
        return result

    def get_all_item_type(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM item_type"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'status': row['status']
            })
        cursor.close()
        return result

    def get_all_supplier(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM supplier"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_supplier_by_id(self, id_supplier):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM supplier WHERE id = {}".format((id_supplier))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_all_catalog(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM catalog"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    

    # def get_all_purchase_order(self):
    #     cursor = self.connection.cursor(dictionary=True)
    #     result = []
    #     sql = "SELECT * FROM purchase_order"
    #     cursor.execute(sql)
    #     for row in cursor.fetchall():
    #         result.append({
    #             'id': row['id'],
    #             'id_employee': row['id_employee'],
    #             'id_supplier': row['id_supplier'],
    #             'date': row['date'],
    #             'status': row['status']
    #         })
    #     cursor.close()
    #     return result

    # def get_all_detail_purchase_order(self):
    #     cursor = self.connection.cursor(dictionary=True)
    #     result = []
    #     sql = "SELECT * FROM detail_purchase_order"
    #     cursor.execute(sql)
    #     for row in cursor.fetchall():
    #         result.append({
    #             'id': row['id'],
    #             'id_item': row['id_item'],
    #             'id_purchase': row['id_purchase'],
    #             'qty': row['qty'],
    #             'unit': row['unit'],
    #             'price_per_unit': row['price_per_unit']
    #         })
    #     cursor.close()
    #     return result

class Database(DependencyProvider):
    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='proyek soa 2',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())