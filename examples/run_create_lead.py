import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.test_runner import TestRunner
from src.utils.lead_data_generator import LeadDataGenerator
import logging

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Initialize the test runner with headless=False
        config = {
            "headless": False,  # This will show the browser
            "slowMo": 1000,     # This will slow down operations
            "output_dir": "{{local_file_path}}"  # Add your absolute path here
        }
        runner = TestRunner(config_path="config/config.json")

        # Initialize data generator
        data_gen = LeadDataGenerator()
        
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

        # Generate and use random lead data
        lead_variables = data_gen.generate_lead_data()
        
        logger.info(f"Starting lead creation process with data: {lead_variables}")
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
