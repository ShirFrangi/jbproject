class Country():
    def __init__(self, country_id: int, country_name: str):
        self.country_id = country_id
        self.country_name = country_name
    
    def __repr__(self):
        return f"Country(country_id={self.country_id}, country_name='{self.country_name}')"

# 
