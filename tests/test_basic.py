import pytest
from src.ai_tester import AIWebTester

def test_tester_initialization():
    """Test that the AIWebTester initializes correctly"""
    tester = AIWebTester(headless=True)
    assert tester is not None
    tester.close()

def test_page_exploration():
    """Test basic page exploration"""
    tester = AIWebTester(headless=True)
    try:
        # Use a stable test website
        tester.explore_page("https://example.com")
        assert len(tester.visited_urls) > 0
    finally:
        tester.close()

@pytest.mark.parametrize("element_type,expected", [
    ("button", True),
    ("div", False),
    ("input", True),
    ("p", False)
])
def test_element_analysis(element_type, expected):
    """Test AI element analysis"""
    tester = AIWebTester(headless=True)
    try:
        result = tester.analyze_element(
            element_text="Click me",
            element_type=element_type
        )
        assert result == expected
    finally:
        tester.close()