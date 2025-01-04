import sqlite3
import os

def create_location_database():
    """Create SQLite database and populate it with sample location data."""
    # Define the database path
    db_path = os.path.join('config', 'data', 'locations.db')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to database (creates it if it doesn't exist)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create the locations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                UNIQUE(city, state, zip_code)
            )
        """)
        
        # Sample data - major US cities with valid ZIP codes
        sample_data = [
            # New York
            ('New York', 'NY', '10001'),
            ('New York', 'NY', '10002'),
            ('Brooklyn', 'NY', '11201'),
            # Los Angeles
            ('Los Angeles', 'CA', '90001'),
            ('Los Angeles', 'CA', '90012'),
            ('Beverly Hills', 'CA', '90210'),
            # Chicago
            ('Chicago', 'IL', '60601'),
            ('Chicago', 'IL', '60602'),
            ('Evanston', 'IL', '60201'),
            # Houston
            ('Houston', 'TX', '77001'),
            ('Houston', 'TX', '77002'),
            ('Sugar Land', 'TX', '77478'),
            # Phoenix
            ('Phoenix', 'AZ', '85001'),
            ('Phoenix', 'AZ', '85002'),
            ('Scottsdale', 'AZ', '85251'),
            # Alabama
            ('Birmingham', 'AL', '35201'),
            ('Montgomery', 'AL', '36104'),
            ('Mobile', 'AL', '36601'),
            # Alaska
            ('Anchorage', 'AK', '99501'),
            ('Fairbanks', 'AK', '99701'),
            ('Juneau', 'AK', '99801'),
            # Arkansas
            ('Little Rock', 'AR', '72201'),
            ('Fayetteville', 'AR', '72701'),
            ('Fort Smith', 'AR', '72901'),
            # California (add more since it's already started)
            ('San Francisco', 'CA', '94101'),
            ('San Diego', 'CA', '92101'),
            ('Sacramento', 'CA', '95814'),
            # Colorado
            ('Denver', 'CO', '80201'),
            ('Colorado Springs', 'CO', '80901'),
            ('Boulder', 'CO', '80301'),
            # Connecticut
            ('Hartford', 'CT', '06101'),
            ('New Haven', 'CT', '06510'),
            ('Stamford', 'CT', '06901'),
            # Delaware
            ('Wilmington', 'DE', '19801'),
            ('Dover', 'DE', '19901'),
            ('Newark', 'DE', '19711'),
            # Florida
            ('Miami', 'FL', '33101'),
            ('Orlando', 'FL', '32801'),
            ('Tampa', 'FL', '33601'),
            # Georgia
            ('Atlanta', 'GA', '30301'),
            ('Savannah', 'GA', '31401'),
            ('Augusta', 'GA', '30901'),
            # Hawaii
            ('Honolulu', 'HI', '96801'),
            ('Hilo', 'HI', '96720'),
            ('Kailua', 'HI', '96734'),
            # Idaho
            ('Boise', 'ID', '83701'),
            ('Idaho Falls', 'ID', '83401'),
            ('Pocatello', 'ID', '83201'),
            # Indiana
            ('Indianapolis', 'IN', '46201'),
            ('Fort Wayne', 'IN', '46801'),
            ('Bloomington', 'IN', '47401'),
            # Iowa
            ('Des Moines', 'IA', '50301'),
            ('Cedar Rapids', 'IA', '52401'),
            ('Davenport', 'IA', '52801'),
            # Kansas
            ('Wichita', 'KS', '67201'),
            ('Kansas City', 'KS', '66101'),
            ('Topeka', 'KS', '66601'),
            # Kentucky
            ('Louisville', 'KY', '40201'),
            ('Lexington', 'KY', '40501'),
            ('Bowling Green', 'KY', '42101'),
            # Louisiana
            ('New Orleans', 'LA', '70112'),
            ('Baton Rouge', 'LA', '70801'),
            ('Shreveport', 'LA', '71101'),
            # Maine
            ('Portland', 'ME', '04101'),
            ('Augusta', 'ME', '04330'),
            ('Bangor', 'ME', '04401'),
            # Maryland
            ('Baltimore', 'MD', '21201'),
            ('Annapolis', 'MD', '21401'),
            ('Frederick', 'MD', '21701'),
            # Massachusetts
            ('Boston', 'MA', '02201'),
            ('Cambridge', 'MA', '02138'),
            ('Worcester', 'MA', '01601'),
            # Michigan
            ('Detroit', 'MI', '48201'),
            ('Grand Rapids', 'MI', '49501'),
            ('Ann Arbor', 'MI', '48104'),
            # Minnesota
            ('Minneapolis', 'MN', '55401'),
            ('Saint Paul', 'MN', '55101'),
            ('Rochester', 'MN', '55901'),
            # Mississippi
            ('Jackson', 'MS', '39201'),
            ('Biloxi', 'MS', '39530'),
            ('Hattiesburg', 'MS', '39401'),
            # Missouri
            ('Kansas City', 'MO', '64101'),
            ('Saint Louis', 'MO', '63101'),
            ('Springfield', 'MO', '65801'),
            # Montana
            ('Billings', 'MT', '59101'),
            ('Missoula', 'MT', '59801'),
            ('Helena', 'MT', '59601'),
            # Nebraska
            ('Omaha', 'NE', '68101'),
            ('Lincoln', 'NE', '68501'),
            ('Grand Island', 'NE', '68801'),
            # Nevada
            ('Las Vegas', 'NV', '89101'),
            ('Reno', 'NV', '89501'),
            ('Carson City', 'NV', '89701'),
            # New Hampshire
            ('Manchester', 'NH', '03101'),
            ('Concord', 'NH', '03301'),
            ('Nashua', 'NH', '03060'),
            # New Jersey
            ('Newark', 'NJ', '07101'),
            ('Jersey City', 'NJ', '07301'),
            ('Atlantic City', 'NJ', '08401'),
            # New Mexico
            ('Albuquerque', 'NM', '87101'),
            ('Santa Fe', 'NM', '87501'),
            ('Las Cruces', 'NM', '88001'),
            # North Carolina
            ('Charlotte', 'NC', '28201'),
            ('Raleigh', 'NC', '27601'),
            ('Durham', 'NC', '27701'),
            # North Dakota
            ('Fargo', 'ND', '58102'),
            ('Bismarck', 'ND', '58501'),
            ('Grand Forks', 'ND', '58201'),
            # Oklahoma
            ('Oklahoma City', 'OK', '73101'),
            ('Tulsa', 'OK', '74101'),
            ('Norman', 'OK', '73069'),
            # Oregon
            ('Portland', 'OR', '97201'),
            ('Salem', 'OR', '97301'),
            ('Eugene', 'OR', '97401'),
            # Rhode Island
            ('Providence', 'RI', '02901'),
            ('Warwick', 'RI', '02886'),
            ('Newport', 'RI', '02840'),
            # South Carolina
            ('Columbia', 'SC', '29201'),
            ('Charleston', 'SC', '29401'),
            ('Myrtle Beach', 'SC', '29577'),
            # South Dakota
            ('Sioux Falls', 'SD', '57101'),
            ('Rapid City', 'SD', '57701'),
            ('Aberdeen', 'SD', '57401'),
            # Tennessee
            ('Nashville', 'TN', '37201'),
            ('Memphis', 'TN', '38101'),
            ('Knoxville', 'TN', '37901'),
            # Utah
            ('Salt Lake City', 'UT', '84101'),
            ('Provo', 'UT', '84601'),
            ('Ogden', 'UT', '84401'),
            # Vermont
            ('Burlington', 'VT', '05401'),
            ('Montpelier', 'VT', '05601'),
            ('Rutland', 'VT', '05701'),
            # Virginia
            ('Richmond', 'VA', '23218'),
            ('Virginia Beach', 'VA', '23451'),
            ('Norfolk', 'VA', '23501'),
            # Washington
            ('Seattle', 'WA', '98101'),
            ('Spokane', 'WA', '99201'),
            ('Tacoma', 'WA', '98401'),
            # West Virginia
            ('Charleston', 'WV', '25301'),
            ('Huntington', 'WV', '25701'),
            ('Morgantown', 'WV', '26501'),
            # Wisconsin
            ('Milwaukee', 'WI', '53201'),
            ('Madison', 'WI', '53701'),
            ('Green Bay', 'WI', '54301'),
            # Wyoming
            ('Cheyenne', 'WY', '82001'),
            ('Casper', 'WY', '82601'),
            ('Laramie', 'WY', '82070'),
            ('Laramie', 'WY', '82071')
        ]
        
        # Insert sample data
        cursor.executemany(
            "INSERT OR IGNORE INTO locations (city, state, zip_code) VALUES (?, ?, ?)",
            sample_data
        )
        
        # Create an index for faster random selection
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_location_lookup 
            ON locations(city, state, zip_code)
        """)
        
        # Commit the changes
        conn.commit()
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM locations")
        count = cursor.fetchone()[0]
        print(f"Database created successfully with {count} locations")

if __name__ == "__main__":
    create_location_database()