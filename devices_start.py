import os
from datetime import datetime

from users_start import User
from database_start import DatabaseConnector
from tinydb import TinyDB, Query
from serializer_data import Serializable


class Device(Serializable):
    # Class variable that is shared between all instances of the class
    db_connector = DatabaseConnector().get_devices_table()

    # Constructor
    def __init__(self, device_name: str, managed_by_user_id: str, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None):
        super().__init__(device_name)

        self.device_name = device_name
        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.end_of_life = end_of_life if end_of_life else datetime.today().date()
        self.__creation_date = creation_date if creation_date else datetime.today().date()
        self.__last_update = last_update if last_update else datetime.today().date()

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
            return cls(data['device_name'], data['managed_by_user_id'], data['end_of_life'], data['_Device__creation_date'], data['_Device__last_update'])
        else:
            return None
    
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
