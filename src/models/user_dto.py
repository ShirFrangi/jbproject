# built-in packages
from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    role_id: int

# 
