import json
import os
from typing import Dict, Any
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """Load configuration from config file and environment variables"""
    config = _load_config_file(config_path)
    config.update(_load_env_variables())
    return config

def _load_config_file(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}

def _load_env_variables() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    load_dotenv()
    
    return {
        "headless": os.getenv("TEST_HEADLESS", "").lower() == "true",
        "screenshot_on_error": os.getenv("TEST_SCREENSHOT_ON_ERROR", "").lower() == "true",
        "wait_time": int(os.getenv("TEST_WAIT_TIME", "2")),
        "max_depth": int(os.getenv("TEST_MAX_DEPTH", "3")),
        "allowed_domains": os.getenv("TEST_ALLOWED_DOMAINS", "").split(","),
        "exclude_paths": os.getenv("TEST_EXCLUDE_PATHS", "").split(","),
        "ai_model": os.getenv("TEST_AI_MODEL", "facebook/bart-large-mnli"),
        "element_timeout": int(os.getenv("TEST_ELEMENT_TIMEOUT", "30000")),
        "navigation_timeout": int(os.getenv("TEST_NAVIGATION_TIMEOUT", "30000"))
    }

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration values"""
    try:
        assert isinstance(config.get("headless"), bool), "headless must be boolean"
        assert isinstance(config.get("screenshot_on_error"), bool), "screenshot_on_error must be boolean"
        assert isinstance(config.get("wait_time"), int), "wait_time must be integer"
        assert isinstance(config.get("max_depth"), int), "max_depth must be integer"
        assert isinstance(config.get("allowed_domains"), list), "allowed_domains must be list"
        assert isinstance(config.get("exclude_paths"), list), "exclude_paths must be list"
        assert isinstance(config.get("ai_model"), str), "ai_model must be string"
        assert isinstance(config.get("element_timeout"), int), "element_timeout must be integer"
        assert isinstance(config.get("navigation_timeout"), int), "navigation_timeout must be integer"
        return True
    except AssertionError as e:
        logger.error(f"Config validation error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during config validation: {e}")
        return False