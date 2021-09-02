from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
class DatabaseWrapper:

    def __init__(self, connection):
        self.connection = connection
        
    def get_all_room_type(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM room_type"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'capacity': row['capacity'],
                'status': row['status'],
                'last_update' : row['last_update'],
                'last_update_by' : row['last_update_by']
            })
        cursor.close()
        return result

    # def add_customer(self, name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, employee_id):
    #     cursor = self.connection.cursor(dictionary=True)
    #     sql = "INSERT INTO customer VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),%s)"
    #     val = (name, citizen_number, date_of_birth, gender, address, email, phone_number1, phone_number2, status, employee_id)
    #     cursor.execute(sql, val)
    #     self.connection.commit()
        
    #     sql_last_customer = "SELECT id FROM customer ORDER BY ID DESC LIMIT 1"
    #     cursor.execute(sql_last_customer)
    #     res_id = cursor.fetchone()
    #     cursor.close()
        
    #     return res_id


    def get_customer(self, id, ktp):
        cursor = self.connection.cursor(dictionary=True)
        fetch_all = False
        if id == -1 and ktp == -1:
            sql = "SELECT * FROM customer"
            fetch_all = True
        elif id == -1:
            sql = "SELECT * FROM customer WHERE citizen_number = '{}'".format((ktp))
        elif ktp == -1:
            sql = "SELECT * FROM customer WHERE id = {}".format((id))
        else:
            return {'err_msg': 'You cannot search by id & citizen number at the same time', 'status': False, 'result': ''}

        cursor.execute(sql)
        if fetch_all == True:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        cursor.close()
        return result


    #JADI DIPAKE
    def add_booking(self, id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO booking VALUES (NULL,%s,%s,%s,%s,NOW(),%s,%s,%s,%s)"
        val = (id_customer, id_room_type, id_room, id_employee, start_date, end_date, description, status)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_booking = "SELECT * FROM booking ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_booking)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id

    #JADI DIPAKE
    def update_booking_room(self, id_booking, id_room_new, id_room_type_new, id_employee):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE booking SET id_room_type = %s , id_room = %s, id_employee = %s where id = %s"
        val = (id_room_type_new, id_room_new, id_employee, id_booking)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_updated_booking = "SELECT * FROM booking WHERE id = {}".format((id_booking))
        cursor.execute(sql_updated_booking)
        result = cursor.fetchone()
        cursor.close()
        
        return result

    #update booking date
    def update_booking_date(self, id_booking, start_date, end_date, id_employee):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE booking SET start_date = %s, end_date = %s, id_employee = %s where id = %s"
        val = (start_date, end_date, id_employee, id_booking)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_updated_booking = "SELECT * FROM booking WHERE id = {}".format((id_booking))
        cursor.execute(sql_updated_booking)
        result = cursor.fetchone()
        cursor.close()
        
        return result


    def update_booking_status(self, id_booking, status, id_employee):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE booking SET status = %s, id_employee = %s where id = %s"
        val = (status, id_employee, id_booking)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_updated_booking = "SELECT * FROM booking WHERE id = {}".format((id_booking))
        cursor.execute(sql_updated_booking)
        result = cursor.fetchone()
        cursor.close()
        
        return result

    def get_booking(self, id_booking, id_customer):
        cursor = self.connection.cursor(dictionary=True)
        fetch_all = False
        if id_booking == -1 and id_customer == -1:
            sql = "SELECT * FROM booking"
            fetch_all = True
        elif id_booking == -1:
            sql = "SELECT * FROM booking WHERE id_customer = {}".format((id_customer))
            fetch_all = True
        elif id_customer == -1:
            sql = "SELECT * FROM booking WHERE id = {}".format(id_booking)
            fetch_all = False
        
        cursor.execute(sql)
        if fetch_all == True:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        cursor.close()
        return result


    #Jadi dipake
    def get_booking_by_room(self, id_room, start_date, end_date):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM booking WHERE id_room = %s AND status <> 3 AND status <> 2 AND (((%s BETWEEN start_date AND end_date) OR (%s BETWEEN start_date AND end_date)) OR ((start_date BETWEEN %s AND %s) OR (end_date BETWEEN %s AND %s)))"
        val = (id_room, start_date, end_date, start_date, end_date, start_date, end_date)
        cursor.execute(sql, val)
        cursor.fetchall()
        result = cursor.rowcount
        print(result)
        cursor.close()
        if result == 0:
            return True
        else:
            return False   

    def add_service(self, name, cost, status, employee_id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO service VALUES (NULL,%s,%s,%s,NOW(),%s)"
        val = (name, cost, status, employee_id)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_service = "SELECT id FROM service ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_service)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id

    def get_service(self, id_service, service_name):
        cursor = self.connection.cursor(dictionary=True)
        fetch_all = False
        if id_service == -1 and service_name == -1:
            sql = "SELECT * FROM service"
            fetch_all = True
        elif id_service == -1:
            sql = "SELECT * FROM service WHERE name = '{}'".format((service_name))
            fetch_all = False
        elif service_name == -1:
            sql = "SELECT * FROM service WHERE id = {}".format((id_service))
            fetch_all = False
        
        cursor.execute(sql)
        if fetch_all == True:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        
        cursor.close()
        return result
    
    def add_detail_booking(self, id_service, id_booking, qty, price):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO detail_booking VALUES (NULL,%s,%s,%s,%s)"
        val = (id_service, id_booking, qty, price)
        cursor.execute(sql, val)
        self.connection.commit()
        
        sql_last_detail_booking = "SELECT id FROM detail_booking ORDER BY ID DESC LIMIT 1"
        cursor.execute(sql_last_detail_booking)
        res_id = cursor.fetchone()
        cursor.close()
        
        return res_id

    def get_detail_booking(self, id_booking):
        cursor = self.connection.cursor(dictionary=True)
        fetch_all = False
        if id_booking == -1:
            sql = "SELECT * FROM detail_booking"
            fetch_all = True
        else:
            sql = "SELECT * FROM detail_booking WHERE id_booking = {}".format((id_booking))
            fetch_all = True
        
        cursor.execute(sql)
        if fetch_all == True:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()

        cursor.close()
        return result

     
class Database(DependencyProvider):
    connection_pool = None
    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="database_pool",
            pool_size=12,
            pool_reset_session=True,
            host='localhost',
            database='proyek soa 2',
            user='root',
            password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
