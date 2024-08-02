import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import CHROME_DRIVER_PATH, URLS_JSON_PATH


class WebScraper:
    def __init__(self, chrome_driver_path, base_url, output_file):
        self.chrome_driver_path = chrome_driver_path
        self.base_url = base_url
        self.output_file = output_file
        self.driver = None

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service(self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome WebDriver initialized successfully.")

    def get_page_source(self):
        print(f"Navigating to {self.base_url} ...")
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ant-table-content"))
        )
        print("Page loaded and table content is visible.")

    def wait_for_rows(self):
        print("Waiting for rows to be present...")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".ant-table-tbody .ant-table-row")
            )
        )
        print("Rows are now present.")

    def click_buttons_and_save_urls(self):
        button_urls = []
        visited_urls = set()  # Track visited URLs to avoid duplicates
        row_counter = 0

        while True:
            try:
                self.wait_for_rows()  # Wait until the rows are fully rendered

                # Re-locate rows
                rows = self.driver.find_elements(
                    By.CSS_SELECTOR, ".ant-table-tbody .ant-table-row"
                )
                if not rows:
                    print("No rows found.")
                    break

                print(f"Found {len(rows)} rows. Starting button click processing...")

                for index in range(len(rows)):
                    try:
                        row_counter += 1
                        print(
                            f"Processing button {index + 1} of {len(rows)} in row {row_counter}..."
                        )

                        # Re-locate the buttons each time
                        button = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            ".ant-table-tbody .ant-table-row button.ant-btn",
                        )[index]
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView();", button
                        )
                        ActionChains(self.driver).move_to_element(button).click(
                            button
                        ).perform()

                        print(
                            f"Clicked button {index + 1}. Waiting for page to load..."
                        )

                        # Wait for the new page to load
                        WebDriverWait(self.driver, 10).until(
                            lambda d: d.current_url != self.base_url
                        )

                        # Get the current URL
                        current_url = self.driver.current_url
                        if current_url not in visited_urls:  # Check for duplicates
                            print(
                                f"URL after clicking button {index + 1}: {current_url}"
                            )
                            button_urls.append({"url": current_url, "parsed": False})
                            visited_urls.add(current_url)
                        else:
                            print(
                                f"Duplicate URL skipped after clicking button {index + 1}: {current_url}"
                            )

                        # Navigate back to the previous page
                        print("Navigating back to the previous page...")
                        self.driver.back()
                        WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located(
                                (By.CLASS_NAME, "ant-table-content")
                            )
                        )

                        print("Page reloaded successfully after navigating back.")

                        self.wait_for_rows()  # Ensure rows are rendered after navigating back

                        # Re-locate rows after navigating back
                        rows = self.driver.find_elements(
                            By.CSS_SELECTOR, ".ant-table-tbody .ant-table-row"
                        )
                        if len(rows) <= index:
                            print("No more buttons found.")
                            break

                    except Exception as e:
                        print(
                            f"Error processing button {index + 1} in row {row_counter}: {e}"
                        )

                # Break the loop if no more new buttons found
                if len(button_urls) >= len(rows):
                    break

            except Exception as e:
                print(f"Error in button processing loop at row {row_counter}: {e}")
                break

        # Save URLs to a JSON file
        self.save_to_json(button_urls)

    def save_to_json(self, data):
        with open(self.output_file, "w") as file:
            json.dump(data, file, indent=4)
        print(f"URLs saved to {self.output_file}.")

    def close_driver(self):
        if self.driver:
            self.driver.quit()
        print("Chrome WebDriver closed successfully.")

    def run(self):
        print("Starting web scraping process...")
        self.setup_driver()
        self.get_page_source()
        self.click_buttons_and_save_urls()
        self.close_driver()
        print("Web scraping process completed successfully.")


if __name__ == "__main__":
    chrome_driver_path = CHROME_DRIVER_PATH
    base_url = "https://online.minjust.gov.kg/user/search?fullNameRu=IT&locality=41711000000000&localityType=REPUBLICAN_CITY&operator=AND&page=3&size=10"
    output_file = URLS_JSON_PATH
    scraper = WebScraper(chrome_driver_path, base_url, output_file)
    scraper.run()
