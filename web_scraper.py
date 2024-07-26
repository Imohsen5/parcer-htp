# web_scraper.py

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class WebScraper:
    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path
        self.driver = None

    def setup_driver(self):
        # Create a service object
        service = Service(self.chrome_driver_path)

        # Initialize the WebDriver with the service object
        self.driver = webdriver.Chrome(service=service)

    def extract_text(self, url):
        # Open the URL
        self.driver.get(url)

        # Wait for the page to load completely
        time.sleep(5)  # Adjust the sleep time as necessary

        # Extract all span elements
        spans = self.driver.find_elements(By.TAG_NAME, "span")

        # Extract and print text from all span elements
        extracted_text = "\n".join([span.text for span in spans])
        return extracted_text

    def close_driver(self):
        # Close the WebDriver
        if self.driver:
            self.driver.quit()
