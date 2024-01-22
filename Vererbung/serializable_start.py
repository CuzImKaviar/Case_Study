from abc import ABC, abstractmethod
from tinydb import Query


class Serializable(ABC):

    def __init__(self, id):
        self.id = id

    #ToDo: Implement this class
    def store(self):
        print("Storing data...")

        query = Query()
        result = self.db_connector.search(query.id == self.id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.to_dict(), doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.to_dict())
            print("Data inserted.")

    @classmethod
    @abstractmethod
    def load_data_by_id(cls, id):
        pass

    def delete_user(self):
        query = Query()
        result = self.db_connector.remove(query.id == self.id)
        print("User deleted.")

    #Do not modify this function unless you really know what you are doing!
    def to_dict(self, obj=None):
        """
        This function converts an object recursively into a dict.
        It is not neccessary to understand how this function works!
        For the sake of simplicity it doesn't handle class attributes and callable objects like (callback) functions as attributes well
        """
        #If no object is passed to the function convert the object itself
        if obj is None:
            obj = self
            
        if isinstance(obj, dict):
            #If the object is a dict try converting all its values into dicts also
            data = {}
            for (k, v) in obj.items():
                data[k] = self.to_dict(v)
            return data
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            #If the object is iterable (lists, etc.) try converting all its values into dicts
            #Strings are also iterable, but theses should not be converted
            data = [self.to_dict(v) for v in obj]
            return data
        elif hasattr(obj, "__dict__"):
            #If its an object that has a __dict__ attribute this can be used
            data = []
            for k, v in obj.__dict__.items():
                #Iterate through all items of the __dict__ and and try converting each value to a dict
                #The resulting key value pairs are stored as tuples in a list that is then converted to a final dict
                data.append((k, self.to_dict(v)))
            return dict(data)
        else:
            return obj