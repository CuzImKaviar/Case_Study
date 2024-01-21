class User:

    _list = []

    def __init__(self, id, name, location, job) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.job = job
        User._list.append(self)

    @classmethod
    def remove(cls, name):
        for user in cls._list:
            if user.name == name:
                cls._list.remove(user)
                return True
        return False
    
    @classmethod
    def update(cls, old_name, id, name, location, job):   
        for user in cls._list:
            if user.name == old_name:
                user.id = id
                user.name = name
                user.location = location
                user.job = job
                return True
        return False
        