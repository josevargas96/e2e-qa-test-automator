from faker import Faker
import random

class LeadDataGenerator:
    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)
    
    def generate_lead_data(self):
        """Generate a complete set of lead data."""
        return {
            "FIRST_NAME": self.fake.first_name(),
            "LAST_NAME": self.fake.last_name(),
            "EMAIL": self.fake.email(),
            "PHONE": self.generate_phone()
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