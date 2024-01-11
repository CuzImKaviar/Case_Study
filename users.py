class User:
    def __init__(self, id, name, email) -> None:
        self.name = name
        self.id = id
        self.email = email
    
    def __str__(self):
        return f"{self.name} ({self.email})"
        
