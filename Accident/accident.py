from nameko.rpc import rpc

from dependencies import accident_dependencies 

class AccidentService:

    name = 'accident_service'

    database = accident_dependencies.Database()

    @rpc
    def create_accident(self, id_booking, id_employee, description, compensation, compensation_cost):
        accident = self.database.create_accident(id_booking, id_employee, description, compensation, compensation_cost)
        return accident

    @rpc
    def get_compensation(self,id_booking):
        compensation = self.database.get_compensation(id_booking)
        return compensation

    @rpc
    def get_accident_report(self, start_date, end_date):
        accident_report = self.database.get_accident_report(start_date, end_date)
        return accident_report

    @rpc
    def update_accident(self, id_accident, status):
        updated_accident = self.database.update_accident(
            id_accident, status)
        return updated_accident

    @rpc
    def get_all_accident(self):
        accident=self.database.get_all_accident()
        return accident
    