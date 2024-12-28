import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
from .ai_tester import AIWebTester
from .utils.config import load_config
from .utils.reporting import TestReport

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

    def run_test(self, test_case_path: str, variables: Dict[str, str] = None):
        """Run a specific test case"""
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
        finally:
            self.report.generate_report()
            self.tester.close()

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
                    self.tester.page.goto(step['url'])
                    # Wait for the main content to load
                    self.tester.page.wait_for_selector('ytd-app', state='visible')
                    self.tester.page.wait_for_load_state('networkidle')
                    self.tester.page.wait_for_load_state('domcontentloaded')
                    # Add a small delay to ensure JavaScript is fully loaded
                    self.tester.page.wait_for_timeout(3000)
                
                elif action == 'click':
                    try:
                        # For optional steps, use a shorter timeout
                        timeout = 5000 if is_optional else self.config.get('element_timeout', 30000)
                        element = self.tester.page.wait_for_selector(
                            step['selector'], 
                            state='visible',
                            timeout=timeout
                        )
                        if element:  # Element might be None for optional steps
                            # Make sure the element is interactable
                            self.tester.page.wait_for_selector(step['selector'], state='visible')
                            element.scroll_into_view_if_needed()
                            # Add a small delay before clicking
                            self.tester.page.wait_for_timeout(500)
                            element.click()
                            self.tester.page.wait_for_timeout(1000)
                    except Exception as e:
                        if not is_optional:
                            raise
                        self.logger.info(f"Skipping optional step {step['id']}: {e}")
                
                elif action == 'type':
                    element = self.tester.page.wait_for_selector(
                        step['selector'], 
                        state='visible',
                        timeout=self.config.get('element_timeout', 30000)
                    )
                    # Make sure the element is ready
                    self.tester.page.wait_for_timeout(500)
                    # Clear the field first
                    element.fill("")
                    # Type with delay to simulate human input
                    element.type(step['value'], delay=100)
                    self.tester.page.wait_for_timeout(500)
                
                elif action == 'wait':
                    self.tester.page.wait_for_selector(
                        step['selector'], 
                        state='visible',
                        timeout=self.config.get('element_timeout', 30000)
                    )
                
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
                        if self.config.get("screenshot_on_error"):
                            screenshot_path = self.report.save_screenshot(
                                self.tester.page,
                                f"error_step_{step['id']}"
                            )
                            self.report.add_result(
                                f"Error in step: {step['id']}",
                                "failure",
                                str(e),
                                screenshot_path
                            )
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