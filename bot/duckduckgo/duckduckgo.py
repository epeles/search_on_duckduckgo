"""
DuckDuckGo Search Automation Module.

This module provides a class to automate searches on DuckDuckGo using Selenium WebDriver.
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import duckduckgo.constants as const


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Represents a single search result from DuckDuckGo."""
    
    title: str
    url: str
    position: int


class DuckDuckGoSearcher(webdriver.Chrome):
    """
    A Selenium WebDriver wrapper for automating DuckDuckGo searches.
    
    This class inherits from Chrome WebDriver and provides methods to search
    DuckDuckGo, retrieve results, and handle pagination.
    
    Attributes:
        timeout (int): Maximum wait time for elements in seconds.
        max_pages (int): Maximum number of result pages to load.
    """
    
    def __init__(
        self,
        headless: bool = True,
        timeout: int = 10,
        max_pages: int = 10
    ) -> None:
        """
        Initialize the DuckDuckGo searcher.
        
        Args:
            headless: Run Chrome in headless mode (no GUI). Default is True.
            timeout: Maximum wait time for elements in seconds. Default is 10.
            max_pages: Maximum number of result pages to load. Default is 10.
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        
        driver_path = ChromeDriverManager().install()
        service = ChromeService(executable_path=driver_path)
        super(DuckDuckGoSearcher, self).__init__(service=service, options=options)
        
        self.timeout = timeout
        self.max_pages = max_pages
        logger.info(f"Initialized DuckDuckGoSearcher (timeout={timeout}s, max_pages={max_pages})")

    def navigate_to_homepage(self) -> None:
        """Navigate to DuckDuckGo's homepage."""
        logger.info(f"Navigating to {const.BASE_URL}")
        self.get(const.BASE_URL)

    def search(self, search_term: str) -> List[SearchResult]:
        """
        Perform a search on DuckDuckGo and return results.
        
        Args:
            search_term: The term to search for.
            
        Returns:
            A list of SearchResult objects containing titles and URLs.
            
        Raises:
            ValueError: If search_term is None or empty.
            TimeoutException: If results take too long to load.
        """
        # Validate search term
        if not search_term:
            raise ValueError("Search term cannot be None or empty")
        
        if not search_term.strip():
            raise ValueError("Search term cannot be only whitespace")
        
        logger.info(f"Searching for: '{search_term}'")
        
        # Find search box and enter search term
        search_box = self.find_element(By.NAME, 'q')
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)       
       
        # Wait for results
        wait = WebDriverWait(self, self.timeout)
        try:
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a[data-testid='result-title-a']")
                )
            )
        except TimeoutException:
            logger.warning("No search results found or page took too long to load")
            return []
        
        # Load additional pages
        pages_loaded = self._load_more_results(wait)
        logger.info(f"Loaded {pages_loaded} page(s) of results")
        
        # Extract and return results
        results = self._extract_results()
        logger.info(f"Found {len(results)} total results")
        
        return results

    def _load_more_results(self, wait: WebDriverWait) -> int:
        """
        Click the "more results" button to load additional pages.
        
        Args:
            wait: WebDriverWait instance for waiting on elements.
            
        Returns:
            The number of pages loaded.
        """
        pages = 1
        
        while pages < self.max_pages:
            try:
                more_button = self.find_element(By.ID, 'more-results')
                if more_button:
                    logger.debug(f"Loading page {pages + 1}")
                    more_button.click()
                    pages += 1
                    try:
                        wait.until(EC.element_to_be_clickable((By.ID, 'more-results')))
                    except TimeoutException:
                        logger.debug("No more pages available (timeout)")
                        break   
                else:
                    break
            except NoSuchElementException:
                logger.debug("No more results button found")
                break
        
        return pages

    def _extract_results(self) -> List[SearchResult]:
        """
        Extract search results from the current page.
        
        Returns:
            A list of SearchResult objects.
        """
        result_elements = self.find_elements(
            By.CSS_SELECTOR, "a[data-testid='result-title-a']"
        )
        url_elements = self.find_elements(
            By.CSS_SELECTOR, 'a[data-testid="result-extras-url-link"]'
        )
        
        if not result_elements:
            logger.warning("No results found on the page")
            return []
        
        results = []
        for i, (result, url) in enumerate(zip(result_elements, url_elements), start=1):
            try:
                results.append(SearchResult(
                    title=result.text,
                    url=url.get_attribute('href'),
                    position=i
                ))
            except Exception as e:
                logger.error(f"Error extracting result {i}: {e}")
                continue
        
        return results

    def close(self) -> None:
        """Close the browser and cleanup resources."""
        logger.info("Closing browser")
        self.quit()
