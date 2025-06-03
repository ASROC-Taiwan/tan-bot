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

# test baseImageHandler
def test_base_image_handler():
    bot = TANBot()
    bot.load_gsheet()
    image_handler = bot.image
    assert image_handler is not None, "Image handler should be initialized"
    
    # Test if the DataFrame is set correctly
    assert image_handler.df is not None, "DataFrame in image handler should not be None"
    
    # Test if the DataFrame is a pandas DataFrame
    assert isinstance(image_handler.df, pd.DataFrame), "DataFrame in image handler should be a pandas DataFrame"
    
    # Test if the DataFrame is not empty
    assert not image_handler.df.empty, "DataFrame in image handler should not be empty"

    # test draw images
    df = image_handler.df
    for _, row in df.iterrows():
        post = image_handler.prepare_a_post(row)
        image_handler.write_image_post(post)

