import os
from datetime import datetime

from users_start import User
from database_start import DatabaseConnector
from tinydb import TinyDB, Query
from serializer_data import Serializable
from devices_start import Device

device_list = Device.get_db_connector(Device)
print(device_list)

if (True):
    pass