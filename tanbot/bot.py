from dotenv import load_dotenv
import os
import re
import pandas as pd
from .handlers.hugo.hugoHandler import HugoHandler
from .handlers.instagram.instagramHandler import InstagramHandler # WIP
from .handlers.facebook.facebookHandler import FacebookHandler  # WIP
from .handlers.base import BaseImageHandler # testing purposes
from .handlers.line.linebotHandler import LinebotHandler

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
                       rel_path_to_hugo="content/tan/tan-bot",
                       rel_path_to_line="linebot",
                       rel_path_to_image="images"):
        
        self.name = "TAN-bot"
        self.description = "A bot to fetch data from Google Sheets."

        # set the path to be the TANBot object's path
        self.path = os.path.abspath(path)
        self.hugo_post_path = os.path.join(self.path, rel_path_to_hugo)
        self.line_post_path = os.path.join(self.path, rel_path_to_line)
        self.image_path = os.path.join(self.path, rel_path_to_image)

        # 
        self.hugo = HugoHandler(self.hugo_post_path)
        self.line = LinebotHandler(self.line_post_path)  # for testing purposes
        self.instagram = InstagramHandler(self.image_path)  # WIP, for future use
        self.facebook = FacebookHandler(self.image_path)  # WIP, for future use
        self.image = BaseImageHandler(self.image_path)  # for testing purposes

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
            self.line.df = self.df  # Set the DataFrame in the LINE handler for testing purposes
            self.instagram.df = self.df  # Set the DataFrame in the Instagram handler
            self.facebook.df = self.df  # Set the DataFrame in the Facebook handler
            self.image.df = self.df  # Set the DataFrame in the image handler for testing purposes
            print(f"Data loaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to load Google Sheet data: {e}")

    def broadcast(self, line=True, instagram=False, facebook=False):
        """
        Broadcast new posts from HugoHandler to other handlers.
        """
        new_posts = self.hugo.new_posts
        if len(new_posts) == 0:
            print("No new posts to broadcast.")
            return      
        if instagram:
            # Note: Instagram broadcasting is not allowed by Instagram's API.
            raise NotImplementedError("Instagram broadcasting is not implemented yet.")
        if facebook:
            # Note: Facebook fan-page auto post is not implmented yet.
            raise NotImplementedError("Facebook broadcasting is not implemented yet.")
        if line:
            for post in new_posts:
                # WIP: Implement the LINE broadcasting logic here
                self.line.broadcast_a_hugo_post(post)
            

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
    
    
