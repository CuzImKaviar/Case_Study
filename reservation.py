
import os
from tinydb import TinyDB, Query
from database_start import DatabaseConnector
from serializer_data import Serializable

class Reservation(Serializable):

    def get_db_connector(self):
        return DatabaseConnector().get_reservation_table()
    
    @classmethod
    def get_all_reservations(cls):
        return [reservation['title'] for reservation in Reservation.get_db_connector(Reservation)]

    @classmethod
    def get_all_ids(cls):
        return [reservation['id'] for reservation in Reservation.get_db_connector(Reservation)]

    def __init__(self, email, title, device_name, start_time, end_time) -> None:

        super().__init__(title)
        
        self.title = title
        self.email_of_user = email
        self.device = device_name
        self.start_time = start_time
        self.end_time = end_time

    @classmethod
    def load_data_by_id(cls, id):
        query = Query()
        result = cls.get_db_connector(cls).search(query.id == id)
        if result:
            data = result[0]
            return cls(data['title'], data['email'], data['device_name'], data['start_time'], data['end_time'])
        else:
            return None
    
    @classmethod
    def load_data_by_name(cls, name):
        query = Query()
        result = cls.get_db_connector(cls).search(query.name == name)
        if result:
            data = result[0]
            return cls(data['title'], data['email'], data['device_name'], data['start_time'], data['end_time'])
        else:
            return None
        
    def __str__(self):
        return f'Reservations: {self.title} {self.email_of_user} {self.device} {self.start_time}{self.end_time}'

    def __repr__(self):
        return self.__str__()

Reservation_1 = Reservation("Noel@email","Untersuchung","3D_Drucker","SO","MO")
Reservation_2 = Reservation("Noel@email","TEST","3D_Drucker","SO","MO")
Reservation_1.store()
Reservation_2.store()
print(Reservation.get_all_reservations())
print(Reservation.get_all_ids())




