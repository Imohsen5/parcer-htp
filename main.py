import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def download_pdf(url, download_path):
    # Setup Selenium WebDriver with download settings
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome (optional)
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_path,  # Set download directory
            "download.prompt_for_download": False,  # Disable download prompt
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.always_open_pdf_externally": True,  # Disable PDF viewer
        },
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        # Wait for the download button to be clickable
        wait = WebDriverWait(driver, 30)
        download_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='Download']")
            )
        )
        download_button.click()
        print("Download button clicked.")

        # Wait for the download to complete
        time.sleep(20)  # Adjust this delay based on your download speed

        # Check for the downloaded file
        for file in os.listdir(download_path):
            if file.endswith(".pdf"):
                downloaded_file = os.path.join(download_path, file)
                print(f"PDF downloaded successfully: {downloaded_file}")
                return
        print("Failed to download the PDF. Checking directory contents:")
        print(os.listdir(download_path))

    finally:
        driver.quit()


if __name__ == "__main__":
    page_url = "https://online.minjust.gov.kg/user/view-search-result/3eb9cf31-426e-4089-ae8f-ea4eddea83f2"
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    download_pdf(page_url, download_dir)
