import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import os
from .ai_tester import AIWebTester
from .utils.config import load_config
from .utils.reporting import TestReport

logging.basicConfig(level=logging.DEBUG)  # More detailed logging

class TestRunner:
    def __init__(self, config_path: str = "config/config.json"):
        self.config = load_config(config_path)
        self.logger = logging.getLogger(__name__)
        self.report = TestReport()
        self.tester = AIWebTester(headless=self.config.get("headless", False))
        
    def load_test_case(self, test_case_path: str) -> Dict:
        """Load a test case from JSON file"""
        try:
            with open(test_case_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading test case: {e}")
            raise

    def run_test(self, test_case_path: str, variables: Dict[str, str] = None, close_after: bool = False):
        """
        Run a specific test case
        Args:
            test_case_path: Path to the test case JSON file
            variables: Dictionary of variables to use in the test
            close_after: Whether to close the browser after this test
        """
        try:
            test_case = self.load_test_case(test_case_path)
            self.logger.info(f"Running test case: {test_case['name']}")
            
            for step in test_case['steps']:
                self._execute_step(step, variables or {})
                
        except Exception as e:
            self.logger.error(f"Error running test: {e}")
            if self.config.get("screenshot_on_error"):
                screenshot_path = self.report.save_screenshot(
                    self.tester.page, 
                    f"error_{test_case['name']}"
                )
                self.report.add_result(
                    "Error",
                    "failure",
                    str(e),
                    screenshot_path
                )
            raise
        finally:
            self.report.generate_report()
            if close_after:
                self.close()

    def close(self):
        """Explicitly close the browser"""
        if hasattr(self, 'tester'):
            self.tester.close()

    def save_url_to_file(self, url: str, filename: str, variables: Dict[str, str] = None):
        """
        Save URL to a text file in the configured output directory using absolute paths
        Args:
            url: The URL to save
            filename: Name of the file to save the URL in
        """
        try:
            # Get absolute output directory from config or raise error if not set
            if "output_dir" not in self.config:
                raise ValueError("output_dir must be set in config with absolute path")
            
            # Convert to Path object and resolve to absolute path
            output_dir = Path(self.config["output_dir"]).resolve()
            
            # Create directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Add timestamp to filename (before the extension)
            file_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name, ext = os.path.splitext(filename)
            timestamped_filename = f"{base_name}_{file_timestamp}{ext}"
            
            filepath = output_dir / timestamped_filename
            
            # Get timestamp for the content
            content_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Create the log line with name if available
            log_line = f"{content_timestamp}: "
            if variables and 'FIRST_NAME' in variables and 'LAST_NAME' in variables:
                log_line += f"{variables['FIRST_NAME']} {variables['LAST_NAME']} - "
            log_line += f"{url}\n"
            
            # Write to file
            with open(filepath, 'a') as f:
                f.write(log_line)
            
            self.logger.info(f"URL saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving URL to file: {e}")
            raise

    def _execute_step(self, step: Dict, variables: Dict[str, str]):
        """Execute a single test step"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                action = step['action']
                description = step.get('description', action)
                is_optional = step.get('optional', False)
                
                # Replace variables in values
                if 'value' in step:
                    step['value'] = self._replace_variables(step['value'], variables)
                
                if action == 'navigate':
                    self.logger.debug(f"Navigating to: {step['url']}")
                    self.tester.page.goto(step['url'])
                    self.tester.page.wait_for_load_state('networkidle')
                    self.tester.page.wait_for_load_state('domcontentloaded')
                    
                elif action == 'click':
                    if 'selector' in step:
                        step['selector'] = self._replace_variables(step['selector'], variables)
                    self.logger.debug(f"Clicking element: {step['selector']}")
                    try:
                        timeout = 5000 if is_optional else self.config.get('element_timeout', 30000)
                        element = self.tester.page.wait_for_selector(
                            step['selector'], 
                            state='visible',
                            timeout=timeout
                        )
                        if element:
                            element.scroll_into_view_if_needed()
                            self.tester.page.wait_for_timeout(500)
                            element.click()
                    except Exception as e:
                        if not is_optional:
                            raise
                        self.logger.info(f"Skipping optional step {step['id']}: {e}")
                
                elif action == 'type':
                    self.logger.debug(f"Typing into element: {step['selector']}")
                    # Wait for element to be visible and ready
                    element = self.tester.page.wait_for_selector(
                        step['selector'], 
                        state='visible',
                        timeout=self.config.get('element_timeout', 30000)
                    )
                    
                    if element:
                        # Make sure element is in view
                        element.scroll_into_view_if_needed()
                        
                        # Clear the field using keyboard shortcuts
                        element.click()  # Focus the element
                        self.tester.page.keyboard.press("Control+A")  # Select all text
                        self.tester.page.keyboard.press("Backspace")  # Delete selected text
                        
                        # Type the value with a delay
                        element.type(step['value'], delay=100)
                        
                        # Wait a bit after typing
                        self.tester.page.wait_for_timeout(500)
                
                elif action == 'wait':
                    wait_time = step.get('time', 1000)
                    self.logger.debug(f"Waiting for {wait_time}ms")
                    self.tester.page.wait_for_timeout(wait_time)
                
                elif action == 'get_url':
                    current_url = self.tester.get_current_url()
                    self.logger.debug(f"Captured URL: {current_url}")
                    if 'save_to_file' in step:
                        self.save_url_to_file(current_url, step['save_to_file'], variables)
                
                # If we get here, the step was successful
                self.report.add_result(
                    description,
                    "success",
                    f"Completed {action}"
                )
                return  # Exit the retry loop on success
                
            except Exception as e:
                retry_count += 1
                self.logger.warning(f"Step {step['id']} failed (attempt {retry_count}/{max_retries}): {e}")
                
                if retry_count >= max_retries:
                    if not step.get('optional', False):
                        self.logger.error(f"Step {step['id']} failed after {max_retries} attempts")
                        raise
                    else:
                        self.logger.info(f"Skipping optional step {step['id']} after {max_retries} attempts")
                        return
                
                # Wait before retrying
                self.tester.page.wait_for_timeout(2000)

    def _replace_variables(self, value: str, variables: Dict[str, str]) -> str:
        """Replace variables in string with their values"""
        if not isinstance(value, str):
            return value
            
        for var_name, var_value in variables.items():
            placeholder = f"${{{var_name}}}"
            if placeholder in value:
                value = value.replace(placeholder, var_value)
        return value 

    def __del__(self):
        """Ensure browser is closed when TestRunner is destroyed"""
        self.close() 