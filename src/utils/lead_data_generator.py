from faker import Faker
import sqlite3
import os
import random

class LeadDataGenerator:
    def __init__(self):
        self.fake = Faker('en_US')
        self.db_path = os.path.join('config', 'data', 'locations.db')
        
        # Verify database exists
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Database not found at {self.db_path}. "
                "Please run scripts/setup_location_db.py first."
            )
    
    def _get_random_location(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT city, state, zip_code 
                FROM locations 
                ORDER BY RANDOM() 
                LIMIT 1
            """)
            return cursor.fetchone()
    
    def generate_lead_data(self):
        """Generate a complete set of lead data."""
        # Get random real city/state/ZIP from database
        city, state, zip_code = self._get_random_location()
    
        # Generate realistic street address using Faker
        street_number = self.fake.building_number()
        street_name = self.fake.street_name()
        street = f"{street_number} {street_name}"
    
        return {
            "FIRST_NAME": self.fake.first_name(),
            "LAST_NAME": self.fake.last_name(),
            "EMAIL": self.fake.email(),
            "PHONE": self.generate_phone(),
            "STREET": f"{self.fake.building_number()} {self.fake.street_name()}",
            "CITY": city,
            "STATE": state,
            "ZIP": zip_code
    }

    def generate_phone(self):
        """Generate a US phone number in the format (XXX) XXX-XXXX."""
        area_code = random.randint(200, 999)  # Valid area codes
        prefix = random.randint(200, 999)     # Valid prefix
        line = random.randint(1000, 9999)     # Valid line number
        return f"({area_code}) {prefix}-{line}"
    
# Usage example:
if __name__ == "__main__":
    generator = LeadDataGenerator()
    lead_data = generator.generate_lead_data()
    print(lead_data)