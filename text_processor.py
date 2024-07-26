import re

import pandas as pd


class TextProcessor:
    def __init__(self, text, desired_numbers):
        self.text = text
        self.desired_numbers = desired_numbers

    def format_text(self):
        lines = self.text.split("\n")
        data = {}
        current_number = None
        ignore_lines = False

        for line in lines:
            line = line.strip()
            if re.match(r"^\d+\.\s", line):
                current_number = line.split(".")[0].strip()
                data[current_number] = []
                ignore_lines = False
            elif re.match(r"^[IVXLCDM]+\.\s", line):
                ignore_lines = True
            elif current_number and not ignore_lines and line:
                data[current_number].append(line)

        # Filter the data based on the desired numbers
        filtered_data = {
            k: " ".join(v) for k, v in data.items() if k in self.desired_numbers
        }
        return filtered_data

    def to_dataframe(self, formatted_data, url):
        # Convert formatted data to a DataFrame with URL as one of the columns
        df = pd.DataFrame([formatted_data])
        df["URL"] = url
        return df

    def to_excel(self, dataframes, file_path):
        # Combine all DataFrames into a single DataFrame and save as Excel
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_excel(file_path, index=False)
