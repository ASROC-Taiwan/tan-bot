from dotenv import load_dotenv
import os
import re
import glob
import pandas as pd
from tanbot.hugo.postHandler import PostHandler as hugo_handler
# WIP
# other handlers can be added here, such as: facebookHandler, instagramHandler, etc.

"""
The TANBot is a Telegram bot that fetches data from a Google Sheet.
It uses the Google Sheets API to read data from a specified sheet and 
returns it in a structured pandas dataframe.

Once data is fetched, it can be used for various purposes such as 
generating hugo posts for the TAN website, or any other data processing tasks.

Triggers of this bot are launched by a Github Action workflow.

Maintainer: @asroc-tw @kuochuanpan
"""
class TANBot:
    def __init__(self, path="./", 
                       rel_path_to_hugo="content/tan/tan-bot"):
        
        self.name = "TAN-bot"
        self.description = "A bot to fetch data from Google Sheets."

        # set the path to be the TANBot object's path
        self.path = os.path.abspath(path)
        self.hugo_post_path = os.path.join(self.path, rel_path_to_hugo)
        self.hugo = hugo_handler(self.hugo_post_path)

        # get the VERSION from __init_.py
        with open(os.path.join(os.path.dirname(__file__), '__init__.py'), 'r') as f:
            content = f.read()
            version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", content)
            if version_match:
                self.version = version_match.group(1)
            else:
                self.version = "25.5.31-beta"

    def _load_env(self):
        """Load environment variables from .env file."""
        load_dotenv()
        self.sheet_id = os.getenv("SHEET_ID")
        self.worksheet_gid = os.getenv("WORKSHEET_GID")

    def load_gsheet(self):
        """Load Google Sheet data into a pandas DataFrame."""
        self._load_env()
        sheet_id = self.sheet_id
        worksheet_gid = self.worksheet_gid
        if not sheet_id or not worksheet_gid:
            raise ValueError("SHEET_ID and WORKSHEET_GID must be set in the environment variables.")

        self.csv_url =f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&id={sheet_id}&gid={worksheet_gid}"
        try:
            self.df = pd.read_csv(self.csv_url)
            self.hugo.df = self.df  # Set the DataFrame in the hugo handler
            print(f"Data loaded successfully from {self.csv_url}")
        except Exception as e:
            raise RuntimeError(f"Failed to load Google Sheet data: {e}")
        

if __name__ == "__main__":

    bot = TANBot(rel_path_to_hugo="content/tan/tan-bot")
    print(bot.version)
    print(bot.hugo_post_path)
    bot.load_gsheet()
    updated = bot.hugo.generate_posts()
    if updated:
        print("Posts updated successfully.")
    else:
        print("No posts were updated.")
    
    
