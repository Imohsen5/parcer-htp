from config import CHROME_DRIVER_PATH, URLS_JSON_PATH
from text_processor import TextProcessor
from url_manager import URLManager
from web_scraper import WebScraper


def main():
    # Initialize URL manager
    url_manager = URLManager(URLS_JSON_PATH)
    unparsed_urls = url_manager.get_unparsed_urls()

    # List of desired numbers to include in the output
    desired_numbers = {
        "3",
        "14",
        "15",
        "16",
        "17",
        "24",
        "25",
    }  # Add or modify the numbers as needed

    if not unparsed_urls:
        print("All URLs have been parsed.")
        return

    # Initialize and set up the web scraper
    scraper = WebScraper(CHROME_DRIVER_PATH)
    scraper.setup_driver()

    # List to store DataFrames for each URL
    dataframes = []

    for url in unparsed_urls:
        print(f"Processing URL: {url}")

        # Extract text from the web page
        extracted_text = scraper.extract_text(url)

        # Process the extracted text
        processor = TextProcessor(extracted_text, desired_numbers)
        formatted_data = processor.format_text()

        # Convert the formatted data to a DataFrame and append to the list
        df = processor.to_dataframe(formatted_data, url)
        dataframes.append(df)

        # Update the URL status to parsed
        url_manager.update_status(url)

    # Save all DataFrames to a single Excel file
    excel_file_path = "combined_output.xlsx"
    processor.to_excel(dataframes, excel_file_path)
    print(f"Data saved to {excel_file_path}")

    scraper.close_driver()


if __name__ == "__main__":
    main()
