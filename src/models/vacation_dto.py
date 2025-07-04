# built-in packages
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Vacation:
    vacation_id: int
    country_id: int
    vacation_info: str
    vacation_start_date: date
    vacation_end_date: date
    price: int
    photo_file_path: str
    country_name: Optional[str] = None
    likes_count: Optional[int] = 0

# 
