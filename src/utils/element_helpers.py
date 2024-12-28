from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

def get_element_attributes(element) -> Dict:
    """Extract all relevant attributes from a page element"""
    try:
        return element.evaluate("""el => {
            const attrs = {};
            for (const attr of el.attributes) {
                attrs[attr.name] = attr.value;
            }
            return {
                tagName: el.tagName.toLowerCase(),
                id: el.id,
                className: el.className,
                type: el.type,
                value: el.value,
                innerText: el.innerText,
                attributes: attrs
            };
        }""")
    except Exception as e:
        logger.error(f"Error getting element attributes: {e}")
        return {}

def is_element_visible(element) -> bool:
    """Check if an element is visible on the page"""
    try:
        return element.evaluate("""el => {
            const style = window.getComputedStyle(el);
            return style.display !== 'none' && 
                   style.visibility !== 'hidden' && 
                   style.opacity !== '0';
        }""")
    except Exception as e:
        logger.error(f"Error checking element visibility: {e}")
        return False

def get_form_inputs(form_element) -> List[Dict]:
    """Get all input elements from a form with their properties"""
    try:
        return form_element.evaluate("""form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            return Array.from(inputs).map(input => ({
                type: input.type || input.tagName.toLowerCase(),
                name: input.name,
                id: input.id,
                required: input.required,
                placeholder: input.placeholder,
                value: input.value
            }));
        }""")
    except Exception as e:
        logger.error(f"Error getting form inputs: {e}")
        return []

def wait_for_navigation(page):
    """Wait for page navigation to complete"""
    try:
        page.wait_for_load_state('networkidle')
        page.wait_for_load_state('domcontentloaded')
    except Exception as e:
        logger.error(f"Error waiting for navigation: {e}")

def safe_click(element):
    """Safely click an element with proper waiting and error handling"""
    try:
        element.wait_for_element_state('stable')
        element.scroll_into_view_if_needed()
        element.click()
        return True
    except Exception as e:
        logger.error(f"Error clicking element: {e}")
        return False