from src.test_runner import TestRunner

def main():
    # Initialize the test runner
    runner = TestRunner()
    
    # Define variables for the test
    variables = {
        "SEARCH_TERM": "Python programming tutorial"
    }
    
    # Run the test case
    runner.run_test(
        "config/test_cases/youtube_search.json",
        variables=variables
    )

if __name__ == "__main__":
    main() 