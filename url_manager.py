# url_manager.py

import json


class URLManager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.urls_data = self.load_urls()

    def load_urls(self):
        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_urls(self):
        with open(self.json_path, "w", encoding="utf-8") as file:
            json.dump(self.urls_data, file, ensure_ascii=False, indent=4)

    def get_unparsed_urls(self):
        return [
            url_info["url"] for url_info in self.urls_data if not url_info["parsed"]
        ]

    def update_status(self, url):
        for url_info in self.urls_data:
            if url_info["url"] == url:
                url_info["parsed"] = True
                break
        self.save_urls()
