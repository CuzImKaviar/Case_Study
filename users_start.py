import os
from tinydb import TinyDB, Query
from database_start import DatabaseConnector
from serializer_data import Serializable

class User(Serializable):

    def get_db_connector(self):
        return DatabaseConnector().get_users_table()
    
    @classmethod
    def get_all_names(cls):
        return [user['name'] for user in User.get_db_connector(User)]

    def get_all_ids(self):
        return [user['id'] for user in User.get_db_connector(User)]

    def __init__(self, email, name, location, job) -> None:

        super().__init__(email)
        
        self.name = name
        self.email = email
        self.location = location
        self.job = job
        

    @classmethod
    def load_data_by_id(cls, id):
        query = Query()
        result = cls.get_db_connector(cls).search(query.id == id)
        if result:
            data = result[0]
            return cls(data['email'], data['name'], data['location'], data['job'])
        else:
            return None
    
    @classmethod
    def load_data_by_name(cls, name):
        query = Query()
        result = cls.get_db_connector(cls).search(query.name == name)
        if result:
            data = result[0]
            return cls(data['email'], data['name'], data['location'], data['job'])
        else:
            return None
        

    def __str__(self):
        return f'User: {self.name} ({self.email}), MCI: {self.location} as {self.job}'

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Create a device
    user1 = User("one@mci.edu", "User One", "Innsbruck", "Student")
    user2 = User("two@mci.edu", "User Two", "Imst", "Student") 
    user3 = User("three@mci.edu", "User Three", "Landeck", "Student") 
    user1.store()
    user2.store()
    user3.store()
    user1.delete_user()
    user4 = User("four@mci.edu", "User Four", "Landeck", "Professor") 
    user4.store()

    User.get_all_names()

    loaded_user = User.load_data_by_id('four@mci.edu')
    if loaded_user:
        print(f"Loaded: {loaded_user}")
    else:
        print("User not found.")