from src.test_runner import TestRunner

def main():
    # Initialize test runner
    runner = TestRunner()
    
    # Define test variables
    variables = {
        "FIRST_NAME": "John",
        "LAST_NAME": "Doe",
        "EMAIL": "john.doe@example.com",
        "PHONE": "1234567890",
        "STREET": "123 Main St",
        "CITY": "Boston",
        "STATE": "MA",
        "ZIP": "02108"
    }
    
    # Run the test case
    runner.run_test(
        "config/test_cases/convert_lead_to_opportunity.json",
        variables=variables
    )

if __name__ == "__main__":
    main()
