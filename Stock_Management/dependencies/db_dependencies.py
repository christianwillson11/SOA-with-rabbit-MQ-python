from nameko.extensions import DependencyProvider

import pymysqlpool
import pymysql

class Item:
    connection = None
    
    # Constructor
    def __init__ (self, connection):
        self.connection = connection

    # Get ALL ITEM
    def get_all_item(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM item'
        cursor.execute(sql)
        return cursor.fetchall()

    def get_all_itemtype(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM item_type'
        cursor.execute(sql)
        return cursor.fetchall()

    # Get ITEM by ID
    def get_item_by_id(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM item WHERE id = {}'.format(id)
        cursor.execute(sql)
        return cursor.fetchone()

    def get_itemtype_by_id(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM item_type WHERE id = {}'.format(id)
        cursor.execute(sql)
        return cursor.fetchone()

    # Asumsi yang dapat diupdate stock dan status serta kapan dan siapa yang update
    # here
    def update_item_status(self, id, status, employeeid):
        result = {
            'status': True,
            'err_msg': ''
        }

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE item SET status = {}, last_update = SYSDATE(), last_update_by = {} WHERE id = {}'
        sql = sql.format(status,  employeeid , id)
        cursor.execute(sql)

        return result

    def update_item2(self, id_item, qty_in_hand, unit, employee_id):
        result = {
            'status': True,
            'err_msg': ''
        }

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE item SET qty_in_hand = qty_in_hand + {}, unit = unit + {}, last_update = SYSDATE(), last_update_by = {} WHERE id = {}'
        sql = sql.format(qty_in_hand, unit, employee_id , id_item)
        cursor.execute(sql)

        return result

    def delete_item_by_id(self,id,employeeid):
        result = {
            'status': True,
            'err_msg': ''
        }

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE item SET status = "0", last_update = SYSDATE(), last_update_by="{}" WHERE id="{}"'.format(employeeid,id)
        cursor.execute(sql)

        return result

    def insert_item(self, id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, employeeid):
        result = {
            'status': True,
            'err_msg': ''
        }

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO item (id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, last_update, last_update_by) VALUES ("{}", "{}","{}","{}","{}","{}","{}","{}",SYSDATE(),"{}")'
        sql = sql.format(id_type, name, barcode, qty_in_hand, qty_broken, qty_lost, unit, status, employeeid)
        cursor.execute(sql)

        return result

    def insert_itemtype(self,name,status):
        result = {
            'status': True,
            'err_msg': ''
        }

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'INSERT INTO item_type (name,status) VALUES ("{}","{}")'
        sql = sql.format(name,status)
        cursor.execute(sql)

        return result

    # def update_itemtype(self, id, status, id_employee):
    #     result = {
    #         'status': True,
    #         'err_msg': ''
    #     }

    #     cursor = self.connection.cursor(pymysql.cursors.DictCursor)
    #     sql = 'UPDATE item_type SET name = "{}", status = "{}" WHERE id = {}'
    #     sql = sql.format(name,status,id)
    #     cursor.execute(sql)

    #     return result

    # def delete_itemtype_by_id(self,id):
    #     result = {
    #         'status': True,
    #         'err_msg': ''
    #     }

    #     cursor = self.connection.cursor(pymysql.cursors.DictCursor)
    #     sql = 'UPDATE item_type SET status = "0", WHERE id="{}"'.format(id)
    #     cursor.execute(sql)

    #     return result

    # View Laporan
    def view_laporan(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM item'
        cursor.execute(sql)
        return cursor.fetchall()
    
    def close_connection(self):
        self.connection.close()



# Class untuk DB Pool
class DBProvider(DependencyProvider):

    connection_pool = None

    def __init__(self):
        config = {
            'host': 'localhost', 
            'user': 'root', 
            'password': '', 
            'database': 'proyek soa 2', 
            'autocommit': True
        }
        self.connection_pool = pymysqlpool.ConnectionPool(size=20, name='DB Pool', **config)

    def get_dependency(self, worker_ctx):
        return Item(self.connection_pool.get_connection())