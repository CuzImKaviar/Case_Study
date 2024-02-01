import os
from datetime import datetime

from users import User
from database_start import DatabaseConnector
from tinydb import TinyDB, Query
from serializer_data import Serializable


class Device(Serializable):
    # Class variable that is shared between all instances of the class
    db_connector = DatabaseConnector().get_devices_table()

    # Constructor
    def __init__(self, id, device_name, managed_by_user_id, location, tool_type, price, movable, maintenance_period, reservable, comment: str = None, reservations_start: list = None, reservations_end: list = None, reserved_by: list = None, reason_reservation: list = None) -> None:
        super().__init__(id)

        self.device_name = device_name
        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.managed_by_user_id = managed_by_user_id
        
        self.location = location if location is not None else "not defined"
        self.tool_type = tool_type if tool_type is not None else "not defined"
        self.price = price if price is not None else "not defined"
        self.movable = movable if movable is not None else "not defined"
        self.maintenance_period = maintenance_period if maintenance_period is not None else "not defined"
        self.reservable = reservable if reservable is not None else "not defined"
        self.comment = comment if comment is not None else "not defined"
        self.reservations_start = reservations_start if reservations_start is not None else []
        self.reservations_end = reservations_end if reservations_end is not None else []
        self.reserved_by = reserved_by if reserved_by is not None else []
        self.reason_reservation = reason_reservation if reason_reservation is not None else []
        self.is_active = True
        self._Device__creation_date = datetime.today().date()
        self._Device__last_update = datetime.today().date()

    def get_db_connector(self):
        return DatabaseConnector().get_devices_table()
    
    @classmethod
    def get_all_names(cls):
        return [device['device_name'] for device in Device.get_db_connector(Device)]

    @classmethod
    def get_all_ids(cls):
        return [device['id'] for device in Device.get_db_connector(Device)]
    
    def store(self):
        self.__last_update = datetime.today().date()
        super().store()
        
    # String representation of the class
    def __str__(self):
        return f'Device: {self.device_name} ({self.managed_by_user_id}) - Active: {self.is_active} - Created: {self.__creation_date} - Last Update: {self.__last_update}'

    # String representation of the class
    def __repr__(self):
        return self.__str__()
            
    # Class method that can be called without an instance of the class to construct an instance of the class
    @classmethod
    def load_data_by_id(cls, id):
        # Load data from the database and create an instance of the Device class
        query = Query()
        result = cls.get_db_connector(cls).search(query.id == id)

        if result:
            data = result[0]
            return cls(data['id'], data['device_name'], data['managed_by_user_id'], data['location'], data['tool_type'], data['price'], data['movable'], data['maintenance_period'], data['reservable'], data['comment'], data['reservations_start'], data['reservations_end'])
        else:
            return None
        

    def add_reservations(self, start, end, reserved_by, reason_reservation):
        self.reservations_start.append(start)
        self.reservations_end.append(end)
        self.reserved_by.append(reserved_by)
        self.reason_reservation.append(reason_reservation)
        self.store()
    
if __name__ == "__main__":
    # Create a device
    device1 = Device("Device1", "one@mci.edu")
    device2 = Device("Device2", "two@mci.edu") 
    device3 = Device("Device3", "two@mci.edu") 
    device1.store()
    device2.store()
    device3.store()
    device4 = Device("Device3", "four@mci.edu") 
    device4.store()

    res = Device.get_all_names()

    loaded_device = Device.load_data_by_id('Device2')
    if loaded_device:
        print(f"Loaded: {loaded_device}")
    else:
        print("Device not found.")
