import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

class InternshalaSpider(scrapy.Spider):
    name = 'internshala'
    start_urls = ['https://internshala.com/internships/']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(random.uniform(5, 10))

        wait = WebDriverWait(self.driver, 20)
        internships = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "internship_meta")))

        for internship in internships:
            try:
                title = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.view_detail_button"))).text
                company = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.link_display_like_text"))).text
                location = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a#location_names"))).text
                stipend = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.stipend"))).text
                
                yield {
                    'title': title,
                    'company': company,
                    'location': location,
                    'stipend': stipend
                }
                
                time.sleep(random.uniform(1, 3))
            except (TimeoutException, NoSuchElementException) as e:
                self.logger.error(f"Error extracting internship details: {e}")

    def closed(self, reason):
        self.driver.quit()