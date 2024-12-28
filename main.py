import argparse
import logging
from src.ai_tester import AIWebTester

def setup_argument_parser():
    parser = argparse.ArgumentParser(
        description='AI-powered web testing automation'
    )
    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='The URL to test'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum depth for page exploration'
    )
    return parser

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Parse arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Initialize tester
    tester = AIWebTester(headless=args.headless)
    tester.max_depth = args.max_depth

    try:
        logger.info(f"Starting test exploration of {args.url}")
        tester.explore_page(args.url)
        logger.info("Testing completed successfully")
    except Exception as e:
        logger.error(f"Error during testing: {e}")
    finally:
        tester.close()

if __name__ == "__main__":
    main()