from transformers import pipeline
from playwright.sync_api import sync_playwright
import time
import logging
from typing import List, Optional

class AIWebTester:
    """
    AI-powered web testing automation class that combines Playwright
    with Transformers for intelligent web interaction.
    """
    
    def __init__(self, headless: bool = False):
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing AIWebTester")
        
        # Initialize AI model - using text classification for interaction decisions
        self.nlp = pipeline("text-classification", 
                          model="distilbert-base-uncased-finetuned-sst-2-english")
        
        # Setup Playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        
        # Initialize state
        self.visited_urls = set()
        self.current_depth = 0
        self.max_depth = 3
        
    def _setup_logging(self):
        """Configure logging for the tester"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('debug.log'),
                logging.StreamHandler()
            ]
        )
    
    def analyze_element(self, element_text: str, element_type: str) -> bool:
        """
        Use AI to determine if an element should be interacted with.
        Returns True if the element is likely interactive.
        """
        try:
            # Create a context string that describes the element
            context = f"This {element_type} element says '{element_text}'"
            
            # Classify the element - returns positive for interactive elements
            result = self.nlp(context)[0]
            
            # Map sentiment to interactivity (positive sentiment = interactive)
            score = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']
            
            # Consider elements like buttons and inputs as more likely to be interactive
            base_score = 0.5
            if element_type in ['button', 'input', 'select', 'a']:
                base_score = 0.7
                
            return score > base_score
            
        except Exception as e:
            self.logger.error(f"Error analyzing element: {e}")
            return False
    
    def explore_page(self, url: str):
        """
        Explore a webpage and interact with its elements intelligently.
        """
        if url in self.visited_urls or self.current_depth >= self.max_depth:
            return
        
        try:
            self.logger.info(f"Exploring: {url}")
            self.visited_urls.add(url)
            self.page.goto(url)
            self.page.wait_for_load_state('networkidle')
            
            elements = self.page.query_selector_all('button, a, input, select')
            
            for element in elements:
                self._process_element(element, url)
                
        except Exception as e:
            self.logger.error(f"Error exploring page {url}: {e}")
    
    def _process_element(self, element, base_url: str):
        """
        Process and interact with a single element on the page.
        """
        try:
            element_text = element.inner_text()
            element_type = element.evaluate('el => el.tagName.toLowerCase()')
            
            if self.analyze_element(element_text, element_type):
                self.logger.info(f"Interacting with {element_type}: {element_text}")
                self._interact_with_element(element, element_type, base_url)
                
        except Exception as e:
            self.logger.error(f"Error processing element: {e}")
    
    def _interact_with_element(self, element, element_type: str, base_url: str):
        """
        Perform the appropriate interaction based on element type.
        """
        try:
            if element_type == 'button':
                element.click()
            elif element_type == 'input':
                element.fill('test input')
            elif element_type == 'a':
                href = element.get_attribute('href')
                if href and href.startswith(base_url):
                    self.current_depth += 1
                    self.explore_page(href)
                    self.current_depth -= 1
            
            time.sleep(1)  # Wait for any reactions
            
        except Exception as e:
            self.logger.error(f"Error interacting with {element_type}: {e}")
    
    def close(self):
        """
        Clean up resources.
        """
        try:
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")
