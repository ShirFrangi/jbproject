class Like:
    def __init__(self, like_id: int, user_id: int, vacation_id: int):
        self.like_id = like_id
        self.user_id = user_id
        self.vacation_id = vacation_id
        
    def __repr__(self):
        return f"Like(like_id={self.like_id}, user_id={self.user_id}, vacation_id={self.vacation_id})"

# 
  