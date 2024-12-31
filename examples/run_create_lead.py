from src.test_runner import TestRunner
import logging

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Initialize the test runner with headless=False
        config = {
            "headless": False,  # This will show the browser
            "slowMo": 1000     # This will slow down operations
        }
        runner = TestRunner(config_path="config/config.json")
        
        # Login first
        login_variables = {
            "USERNAME": "{{username}}",
            "PASSWORD": "{{password}}"
        }
        
        logger.info("Starting login process...")
        runner.run_test(
            "config/test_cases/login.json",
            variables=login_variables,
            close_after=False  # Don't close browser after login
        )

        # Create lead
        lead_variables = {
            "FIRST_NAME": "{{name}}",
            "LAST_NAME": "{{last_name}}",
            "EMAIL": "{{email}}",
            "PHONE": "{{phone}}"
        }
        
        logger.info("Starting lead creation process...")
        runner.run_test(
            "config/test_cases/create_lead.json",
            variables=lead_variables,
            close_after=True  # Close browser after creating lead
        )

    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        if 'runner' in locals():
            runner.close()
        raise

if __name__ == "__main__":
    main()
