from tanbot import TANBot
import pandas as pd

def test_load_gsheet():
    """Test if the Google Sheet data can be loaded."""
    bot = TANBot()
    bot.load_gsheet()
    df = bot.hugo.df
    assert not df.empty, "DataFrame should not be empty"

def test_hugo():
    bot = TANBot()
    bot.load_gsheet()
    has_updated = bot.hugo.generate_posts()