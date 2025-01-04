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
            ('Scottsdale', 'AZ', '85251')
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