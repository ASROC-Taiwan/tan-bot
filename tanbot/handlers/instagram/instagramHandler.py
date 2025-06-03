import os
import time
import glob
from dataclasses import dataclass
from ..base import BaseImageHandler
from ..base import ImagePost
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

@dataclass
class InstagramPost(ImagePost):
    """
    Data class for Instagram posts.
    Contains the necessary fields for an Instagram post.
    """
    caption: str = 'See https://asroc-taiwan.github.io/website/en/tan/ for more information.'

class InstagramHandler(BaseImageHandler):
    """
    Handler for Instagram posts.
    Inherits from BaseImageHandler.
    """

    def __init__(self, bot):
        super().__init__(bot)

    def prepare_a_post(self, row):
        """
        Prepare a post from a DataFrame row.
        This method should be implemented in the subclass.
        """
        image_post = super().prepare_a_post(row)
        
        # we might want to provide the url from the corresponding hugo post
        caption = 'See https://asroc-taiwan.github.io/website/en/tan/ for more information.'

        # Create the Instagram post
        instagram_post = InstagramPost(
            title=image_post.title,
            date=image_post.date,
            author=image_post.author,
            summary=image_post.summary,
            content=image_post.content,
            filename_head=image_post.filename_head,
            filename=image_post.filename,
            base_image=image_post.base_image,
            caption=caption,
            draft=image_post.draft
        )
        return instagram_post

    def poblish_a_post(self, post):
        """
        Publish a post to Instagram.
        
        NOTE: Instgram does not allow bot to publish posts.
              We need to be careful with the policy of Instagram.
        """
        self.write_image_post(post)

        # Check if the post has been published or not
        if post.draft:
            print(f"Post {post.filename} is a draft, skipping publication.")
            return
        
        # TODO: we need a way to check if the post has already been published
        
        # Connect to Instagram and publish the post
        cl = Client()
        load_dotenv()
        username = os.getenv("IG_USERNAME")
        password = os.getenv("IG_PASSWORD")

        try:
            cl.load_settings("./instagram_sssion.json")
        except FileNotFoundError:
            cl.login(username, password)
            cl.dump_settings("./instagram_session.json")
        except LoginRequired:
            cl.login(username, password)
            cl.dump_settings("./instagram_session.json")

        print(cl.account_info().model_dump())
        filepath = os.path.join(self.image_dir, post.filename)
        media = cl.photo_upload(filepath, post.caption)
        print(f"Post published with ID/PD: {media.id}/{media.pk}")
        return