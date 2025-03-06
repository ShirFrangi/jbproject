class User:
    def __init__(self, user_id: int, first_name: str, last_name: str, email: str, password: str, role_id: int):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role_id = role_id
        
    def __repr__(self):
        return f"User(user_id={self.user_id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', password='{self.password}' role_id={self.role_id})"


# 
    