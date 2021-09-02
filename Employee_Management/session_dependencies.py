from nameko.extensions import DependencyProvider

import redis
import pickle

class RedisSessionWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    def set_session_data(self, key, value, ex = 30 * 60):
        value_byte = pickle.dumps(value)
        self.connection.set(key, value_byte)
        self.connection.expire(key, ex)

    def delete_session_data(self, key):
        self.connection.expire(key, 0)

    def get_session_data(self, key):
        value_byte = self.connection.get(key)
        result = pickle.loads(value_byte)
        return result   
    
    def get_all_online_employee(self):
        return self.connection.keys()
    
    def is_employee_online(self, key):
        for k in self.connection.keys():
            if k.decode('utf-8') == key:
                return True
        return False


class SessionProvider(DependencyProvider):
    
    connection_pool = None

    def __init__(self):
        self.connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    
    def get_dependency(self, worker_ctx):
        return RedisSessionWrapper(redis.Redis(connection_pool=self.connection_pool))
