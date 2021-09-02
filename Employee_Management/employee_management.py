from nameko.rpc import rpc
import uuid

import employee_dependencies
import session_dependencies

class ServiceEmployee:
    
    name = "service_employee"

    db = employee_dependencies.DBProvider()
    session = session_dependencies.SessionProvider()

    @rpc
    def login(self, username, password):
        user, status = self.db.check_login(username, password)
        err_msg = ''
        session_id = ''

        if status:
            session_id = str(uuid.uuid1())
            while session_id in self.session.get_all_online_employee():
                session_id = str(uuid.uuid1())

            self.session.set_session_data(session_id, user)
            self.db.login(username, password)
        else:
            err_msg = 'User Not Found'
        
        return {
            'status': status,
            'err_msg': err_msg,
            'session_id': session_id
        }

    @rpc
    def logout(self, session_id):
        status = self.session.is_employee_online(session_id)
        err_msg = ''
        result = ''
        if status:
            data = self.session.get_session_data(session_id)
            self.session.delete_session_data(session_id)
            username = str(data['username'])
            password = str(data['password'])
            result = self.db.logout(username, password)
            session = ''
        else :
            session = session_id
            err_msg = 'You are not logged in yet'
        return {
            'status': status,
            'err_msg': err_msg,
            'session_id': session,
            "result": result
        }

    @rpc 
    def forgot_password(self, id, email):
        return self.db.forgot_password(id, email)
    
    @rpc 
    def is_logged_in(self, session_id):
        return self.session.is_employee_online(session_id)

    @rpc
    def get_session_data(self, session_id):
        return self.session.get_session_data(session_id)

    @rpc
    def get_all_employee(self):
        result = self.db.get_all_employee()
        self.db.close_connection()
        return result
    
    @rpc
    def get_employee_by_id(self, id):
        result = self.db.get_employee_by_id(id)
        self.db.close_connection()
        return result

    @rpc
    def register_account(self, new_account) :
        result = self.db.register_account(new_account)
        self.db.close_connection()
        return result

    @rpc
    def register_employee(self, new_employee):
        result = self.db.register_employee(new_employee)
        self.db.close_connection()
        return result

    @rpc
    def register_job(self, new_job):
        result = self.db.register_job(new_job)
        self.db.close_connection()
        return result

    @rpc
    def edit_employee_data(self, session_id, id, name, birth, c_num, address, phone_num1, phone_num2, email):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            user, status = self.db.check_login(data['username'], data['password'])

            if status:
                result = self.db.edit_employee_data(id, name, birth, c_num, address, phone_num1, phone_num2, email, user['id'])
            else:
                err_msg = 'You are not logged in yet'
            self.db.close_connection()
        else:
            err_msg = 'You are not logged in'
            result = ''
            status = False
        return {
            "result": result,
            "err_msg": err_msg,
            "status": status
        }

    @rpc
    def edit_employee_job(self, session_id, id, id_job):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        
        if stat:
            data = self.session.get_session_data(session_id)
            user, status = self.db.check_login(data['username'], data['password'])

            if status:
                result = self.db.edit_employee_job(id, id_job, data['id'])
            else:
                err_msg = 'You are not logged in yet'
            self.db.close_connection()
        else:
            err_msg = 'You are not logged in'
            result = ''
            status = False
        return {
            "result": result,
            "err_msg": err_msg,
            "status": status
        }

    @rpc 
    def delete_employee(self, session_id, id):
        err_msg = ''
        stat = self.session.is_employee_online(session_id)
        if stat:
            data = self.session.get_session_data(session_id)
            user, status = self.db.check_login(data['username'], data['password'])
    
            if status:
                result = self.db.delete_employee(id, user['id'])
            else:
                err_msg = 'You are not logged in yet'
                status = False
            self.db.close_connection()
        else:
            err_msg = 'You are not logged in'
            result = ''
            status = False
        
        return {
           "result": result,
           "err_msg": err_msg,
           "status": status
        }