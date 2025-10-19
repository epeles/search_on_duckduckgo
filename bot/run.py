"""
Main entry point for DuckDuckGo search automation.

This script provides a command-line interface to search DuckDuckGo
and display results.
"""

import sys
import argparse
import logging
from typing import NoReturn

from duckduckgo.duckduckgo import DuckDuckGoSearcher, SearchResult


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging for the application.
    
    Args:
        verbose: Enable debug level logging if True.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def display_results(results: list[SearchResult]) -> None:
    """
    Display search results in a formatted way.
    
    Args:
        results: List of SearchResult objects to display.
    """
    if not results:
        print("\nNo results found.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(results)} result(s)")
    print(f"{'='*80}\n")
    
    for result in results:
        print(f"{result.position}. {result.title}")
        print(f"   URL: {result.url}")
        print()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description='Automate DuckDuckGo searches and retrieve results.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Python automation"
  %(prog)s "Selenium WebDriver" --max-pages 5
  %(prog)s "test search" --no-headless --verbose
        """
    )
    
    parser.add_argument(
        'search_term',
        type=str,
        help='The term to search for on DuckDuckGo'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        metavar='SECONDS',
        help='Maximum wait time for elements (default: 10 seconds)'
    )
    
    parser.add_argument(
        '--max-pages',
        type=int,
        default=10,
        metavar='N',
        help='Maximum number of result pages to load (default: 10)'
    )
    
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser with GUI (visible window)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose (debug) output'
    )
    
    return parser.parse_args()


def main() -> NoReturn:
    """Main execution function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    
    searcher = None
    exit_code = 0
    
    try:
        # Initialize searcher
        searcher = DuckDuckGoSearcher(
            headless=not args.no_headless,
            timeout=args.timeout,
            max_pages=args.max_pages
        )
        
        # Navigate and search
        searcher.navigate_to_homepage()
        results = searcher.search(args.search_term)
        
        # Display results
        display_results(results)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        exit_code = 1
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.", file=sys.stderr)
        exit_code = 130
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        exit_code = 1
    finally:
        # Always close the browser
        if searcher:
            try:
                searcher.close()
            except Exception as e:
                logging.error(f"Error closing browser: {e}")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
