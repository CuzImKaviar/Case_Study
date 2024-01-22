import os
from tinydb import TinyDB, Query
from database_start import DatabaseConnector
from serializable_start import Serializable

class User(Serializable):

    def get_db_connector(self):
        return DatabaseConnector().get_users_table()

    def __init__(self, name, email) -> None:
        super().__init__(email)
        self.name = name
        self.email = email

    @classmethod
    def load_data_by_id(cls, id):
        query = Query()
        result = cls.get_db_connector(cls).search(query.id == id)
        if result:
            data = result[0]
            return cls(data['name'], data['email'])
        else:
            return None
        

    def __str__(self):
        return f'User: {self.name} ({self.id})'

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Create a device
    user1 = User("User One", "one@mci.edu")
    user2 = User("User Two", "two@mci.edu") 
    user3 = User("User Three", "three@mci.edu") 
    user1.store()
    user2.store()
    user3.store()
    user4 = User("User Four", "four@mci.edu") 
    user4.store()

    loaded_user = User.load_data_by_id('four@mci.edu')
    if loaded_user:
        print(f"Loaded: {loaded_user}")
    else:
        print("User not found.")