from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling


class DatabaseWrapper:

    def __init__(self, connection):
        self.connection = connection

    def create_accident(self, id_booking, id_employee, description, compensation, compensation_cost):
        cursor = self.connection.cursor(dictionary=True)
        sql = "INSERT INTO accident VALUES (NULL,{},{},CURDATE(),'{}',{},{},0)".format(
            id_booking, id_employee, description, compensation, compensation_cost)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Add Accident Success"

    def update_accident(self, id_accident, status):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE `accident SET status={} WHERE id = {}".format(
            status, id_accident)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        return "Edit Accident Success"
        
    def get_compensation(self,id_booking):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT compensation, compensation_cost FROM `accident` WHERE id_booking = {}".format(
            id_booking)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_accident_report(self, start_date, end_date):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT COUNT(id) AS jumlah_accident from `accident` WHERE '{}' <= date  AND '{}' >= date".format(
            start_date, end_date)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_all_accident(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM `accident`"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

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
