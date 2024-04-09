import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import duckduckgo.constants as const
from selenium import webdriver
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
        item_to_search = sys.argv[1]
        search = self.find_element(By.NAME, 'q')
        search.send_keys(item_to_search)
        search.send_keys(Keys.RETURN)       
       
        wait = WebDriverWait(self, 10)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']")))
       
        pages = 1
        while True:
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
        
        results = self.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
        urls = self.find_elements(By.CSS_SELECTOR,'a[data-testid="result-extras-url-link"]')
        combined = list(zip(results, urls))
        for i, (result, url) in enumerate(combined, start=1):
            print(f"{i}. {result.text}, URL: {url.get_attribute('href')}")
        print(f"Total pages: {pages}")

    def quit_test(self):
        self.quit