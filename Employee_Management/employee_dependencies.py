from nameko.extensions import DependencyProvider

import pymysqlpool
import pymysql
import smtplib, ssl

class UserWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def login(self, username, password):
        result = None
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE account SET last_login = NOW(), status = 1 WHERE username = "{}" AND password = "{}"'.format(username, password)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = cursor.fetchone()
        cursor.close

    def logout(self, username, password):
        result = None
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE account SET status = 0 WHERE username = "{}" AND password = "{}"'.format(username, password)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = cursor.fetchone()
        cursor.close

    def forgot_password(self, id, email):
        err_msg = ''
        status = True
        employee = pymysql.NULL
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "zetrahotel@gmail.com"  # Enter your address
        receiver_email = email  # Enter receiver address
        password = 'zetra_hotel123'

        if id == '':
            err_msg = 'id cannot be empty'
        else :
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            sql = 'SELECT * FROM account WHERE id = {}'.format(id)
            cursor.execute(sql)
            if cursor.rowcount > 0:
                employee = cursor.fetchone()
                status = True
            else:
                err_msg = 'id does not exist'
                status = False
            cursor.close()

        message = 'Subject: Hi there, this is your current password : '
        old_pass = str(employee['password'])
        message = message + old_pass


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        return {
            'err_msg': err_msg,
            'status': status
        }

    def check_login(self, username, password):
        result = None
        status = True
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM account WHERE username = "{}" AND password = "{}"'.format(username, password)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = cursor.fetchone()
            status = True
        cursor.close()

        return result, status

    def get_all_employee(self):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM employee'
        cursor.execute(sql)
        return cursor.fetchall()

    def get_employee_by_id(self, id):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM employee WHERE id = {}'.format(id)
        cursor.execute(sql)
        return cursor.fetchone()

    # EDIT DATA :
    def edit_employee_data(self, id, name, birth, c_num, address, phone_num1, phone_num2, email, by):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = 'UPDATE employee SET name = "{}", date_of_birth = "{}", citizen_number = "{}", address = "{}", phone_number1 = "{}",  phone_number2 = "{}", email = "{}", last_update_by = "{}" WHERE id = {}'
        sql = sql.format(name, birth, c_num, address, phone_num1, phone_num2, email, by, id)
        cursor.execute(sql)
        return cursor.fetchone()

    # EDIT JOB :
    def edit_employee_job(self, id, id_job, by):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        #sql = 'UPDATE employee SET id_job = "{}", status = "{}" WHERE id = {}'
        sql = 'UPDATE employee SET id_job = "{}", last_update_by = "{}" WHERE id = {}'
        sql = sql.format(id_job, by, id)
        cursor.execute(sql)
        return cursor.fetchone()

    # EDIT STATUS :
    def delete_employee(self, id, by):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        sql = ("UPDATE employee SET status = 0, last_update_by = %s WHERE id = %s")
        #sql = sql.format(id, by)
        cursor.execute(sql, (by, id))
        row_count = cursor.rowcount
        if row_count > 0:
            status = True
        else: 
            status = False
        return status

    #-----------------------  ANDY -------------------------
    def register_account(self, new_account):
        result = {
            'status' : True,
            'err_msg' : ''
        }

        #Validate
        if new_account['username'] == '' or new_account['password'] == '':
            result['status'] = False
            result['err_msg'] = 'Username or Password cannot be empty'
            return result
        
        #Initiate Cursor
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)

        #Check if username already exists on DB
        sql = ("SELECT username FROM account WHERE username = %s GROUP BY username")
        cursor.execute(sql, new_account['username'])
        row_count = cursor.rowcount

        if row_count > 0:
            result['status'] = False
            result['err_msg'] = 'Username already exist, please pick another one'
            return result

        #Username does not exist yet, Attempt to insert into DB
        sql = 'INSERT INTO account VALUES(default, "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(new_account['id_employee'], 
        new_account['username'],new_account['password'], new_account['last_login'], new_account['status'], new_account['last_update'], 
        new_account['last_update_by'])

        cursor.execute(sql)
        
        if sql == '':
            result['err_msg'] = 'Failed to insert data into DB'
            
        return result

    def register_employee(self, new_employee):
        result = {
            'status' : True,
            'err_msg' : ''
        }

        #Validate
        if( new_employee['citizen_number'] == '' or new_employee['name'] == '' or new_employee['date_of_birth'] == '' 
        or new_employee['gender'] == '' or new_employee['address'] == '' or new_employee['email'] == '' or new_employee['phone_number1'] == ''
        or new_employee['status'] == ''):
            result['status'] = False
            result['err_msg'] = 'Please fill out the form, only Phone Number 2 can be empty'
            return result
        
        #Create Cursor
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)

        #Check if citizen number already exists on DB
        sql = ("SELECT citizen_number FROM employee WHERE citizen_number = %s GROUP BY citizen_number")
        cursor.execute(sql, new_employee['citizen_number'])
        row_count = cursor.rowcount

        if row_count > 0:
            result['status'] = False
            result['err_msg'] = 'The citizen number you inputed have been registered before'
            return result

        #Check if email already exists on DB
        sql = ("SELECT email FROM employee WHERE email = %s GROUP BY email")
        cursor.execute(sql, new_employee['email'])
        row_count = cursor.rowcount

        if row_count > 0:
            result['status'] = False
            result['err_msg'] = 'The email you inputed have been registered before'
            return result

        #Check if phone number 1 already exists on DB
        sql = ("SELECT phone_number1 FROM employee WHERE phone_number1 = %s GROUP BY phone_number1")
        cursor.execute(sql, new_employee['phone_number1'])
        row_count = cursor.rowcount

        if row_count > 0:
            result['status'] = False
            result['err_msg'] = 'The phone_number1 you inputed have been registered before'
            return result

        #Check if phone number 2 already exists on DB
        sql = ("SELECT phone_number2 FROM employee WHERE phone_number2 = %s GROUP BY phone_number2")
        cursor.execute(sql, new_employee['phone_number2'])
        row_count = cursor.rowcount

        if row_count > 0:
            result['status'] = False
            result['err_msg'] = 'The phone_number2 you inputed have been registered before'
            return result

        #Attempt to insert into DB
        sql = 'INSERT INTO employee VALUES(default, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(new_employee['id_job'], new_employee['name'], 
        new_employee['citizen_number'],new_employee['date_of_birth'], new_employee['gender'], new_employee['address'], new_employee['email'], 
        new_employee['phone_number1'], new_employee['phone_number2'], new_employee['status'], new_employee['last_update'], new_employee['last_update_by'])

        cursor.execute(sql)
        
        if sql == '':
            result['err_msg'] = 'Failed to insert data into DB'
            
        return result

    
    def register_job(self, new_job):
        result = {
            'status' : True,
            'err_msg' : ''
        }

        #Validate
        if new_job['name'] == '' or new_job['id_manager'] == '' or new_job['status'] == '':
            result['status'] = False
            result['err_msg'] = 'Job Name or Job Manager ID or Job Status cannot be empty'
            return result

        #Initiate Cursor
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)

        #Check if job name already exists on DB
        sql = ("SELECT name FROM job WHERE name = %s GROUP BY name")
        cursor.execute(sql, new_job['name'])
        row_count = cursor.rowcount

        if row_count > 0:
            result['status'] = False
            result['err_msg'] = 'That job already exist'

        #Job does not exist yet, Attempt to insert into DB
        sql = 'INSERT INTO job VALUES(default, "{}", "{}", "{}")'.format(new_job['id_manager'], 
        new_job['name'],new_job['status'])

        cursor.execute(sql)
        
        if sql == '':
            result['err_msg'] = 'Failed to insert data into DB'
            
        return result
#-------------------------------------------------------------------------------------

    def close_connection(self):
        self.connection.close()

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
        return UserWrapper(self.connection_pool.get_connection())