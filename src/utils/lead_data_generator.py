from faker import Faker
import sqlite3
import os

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
        """Get a random city, state, and ZIP code from the database."""
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
        """Generate random but valid lead data including address."""
        # Get random real city/state/ZIP from database
        city, state, zip_code = self._get_random_location()
        
        # Generate realistic street address using Faker
        street_number = self.fake.building_number()
        street_name = self.fake.street_name()
        street = f"{street_number} {street_name}"
        
        return {
            "STREET": street,
            "CITY": city,
            "STATE": state,
            "ZIP": zip_code
        }
