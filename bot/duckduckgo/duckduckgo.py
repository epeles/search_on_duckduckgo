import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import duckduckgo.constants as const
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Duckduckgo(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver_path = ChromeDriverManager().install()
        service = ChromeService(executable_path=driver_path)
        super(Duckduckgo, self).__init__(service=service, options=options)

    def land_main_page(self):
        self.get(const.BASE_URL)

    def search_item(self):
        # Validate search term
        if len(sys.argv) < 2:
            raise ValueError("Error: Please provide a search term. Usage: python run.py 'search term'")
        
        item_to_search = sys.argv[1]
        
        if not item_to_search.strip():
            raise ValueError("Error: Search term cannot be empty")
        
        search = self.find_element(By.NAME, 'q')
        search.send_keys(item_to_search)
        search.send_keys(Keys.RETURN)       
       
        wait = WebDriverWait(self, 10)
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']")))
        except TimeoutException:
            print("Warning: No search results found or page took too long to load")
            return
       
        pages = 1
        max_pages = 10  # Prevent infinite loop
        
        while pages < max_pages:
            try:
                more = self.find_element(By.ID, 'more-results')
                if more:
                    more.click()
                    pages += 1
                    try:
                        wait.until(EC.element_to_be_clickable((By.ID, 'more-results')))
                    except TimeoutException:
                        break   
                else:
                    break
            except NoSuchElementException:
                # No more results button found
                break
        
        results = self.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
        urls = self.find_elements(By.CSS_SELECTOR,'a[data-testid="result-extras-url-link"]')
        
        if not results:
            print("No results found for the search term")
            return
        
        combined = list(zip(results, urls))
        for i, (result, url) in enumerate(combined, start=1):
            print(f"{i}. {result.text}, URL: {url.get_attribute('href')}")
        print(f"Total pages loaded: {pages}")

    def quit_test(self):
        self.quit()