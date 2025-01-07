# Suggested README Updates

## Project Structure
Add the following to the existing structure:

```
e2e-qa-test-automator/
├── ...
├── scripts/                # Utility scripts
│   └── setup_location_db.py  # Database initialization
├── config/
│   ├── ...
│   └── data/               # Data storage
│       └── locations.db    # SQLite database for locations
└── ...
```

## Location Data Management

### Initial Setup
1. Initialize the location database:
```bash
python scripts/setup_location_db.py
```
This creates a SQLite database with valid city, state, and ZIP code combinations for all 50 US states.

### Database Details
- Location: `config/data/locations.db`
- Contents: Valid city, state, and ZIP code combinations
- Coverage: Major cities from all 50 US states

### Lead Data Generation
The LeadDataGenerator now combines:
- Realistic street names (via Faker)
- Valid city, state, and ZIP combinations (via SQLite)

Example usage:
```python
from src.utils.lead_data_generator import LeadDataGenerator

# Initialize generator
data_gen = LeadDataGenerator()

# Generate lead data with valid address
lead_data = data_gen.generate_lead_data()
```

Generated data includes:
- First and last names
- Email and phone
- Complete address with:
  - Realistic street name
  - Valid city, state, ZIP combination

### Maintenance
- The database only needs to be created once
- Run setup script again to add more locations
- Uses UNIQUE constraints to prevent duplicates