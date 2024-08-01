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

# Set up the Chrome driver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Comment out this line to use non-headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

service = Service(ChromeDriverManager().install())

driver = None
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to Internshala
    url = "https://internshala.com/internships/"
    driver.get(url)

    # Wait for the page to load
    time.sleep(random.uniform(5, 10))

    # Wait for the internship listings to load
    wait = WebDriverWait(driver, 20)
    internships = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "internship_meta")))

    # Extract information from each internship listing
    for internship in internships:
        try:
            # Use more specific CSS selectors and add waits
            title = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.view_detail_button"))).text
            company = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.link_display_like_text"))).text
            location = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a#location_names"))).text
            stipend = WebDriverWait(internship, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.stipend"))).text
            
            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"Stipend: {stipend}")
            print("---")
            
            # Add a random delay between processing internships
            time.sleep(random.uniform(1, 3))
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error extracting internship details: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    if driver:
        driver.quit()