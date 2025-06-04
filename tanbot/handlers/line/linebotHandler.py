import os
import time
import glob
from dataclasses import dataclass
from ..base import BaseImageHandler
from ..hugo.hugoHandler import HugoPost
from dotenv import load_dotenv
import importlib.resources as pkg_resources
import requests  
import json  

@dataclass
class LinebotPost:
    title: str
    content: str
    post_url: str
    img_url: str

class LinebotHandler(BaseImageHandler):
    """
    Handler for Linebot posts.
    Inherits from BaseImageHandler.
    """

    def __init__(self, post_dir, flex_img="tan-banner.jpeg"):
        super().__init__(post_dir)
        self.flex_img = pkg_resources.files("tanbot.resources.images").joinpath(flex_img)

    def get_line_post_from_hugo_post(self, hugo_post: HugoPost):
        """
        Broadcast a post from a HugoPost object.
        :param hugo_post: The HugoPost object to broadcast.
        """
        baseUrl= "https://asroc-taiwan.github.io/website/en/tan/tan-bot/"
        post_url = f"{baseUrl}{hugo_post.filename_head}/"
        post = LinebotPost(
            title=hugo_post.title,
            content=hugo_post.content,
            post_url=post_url,
            img_url=self.flex_img
        )
        return post
    
    def broadcast_a_hugo_post(self, hugo_post: HugoPost):
        """
        Broadcast a Hugo post.
        :param hugo_post: The HugoPost object to broadcast.
        """
        post = self.get_line_post_from_hugo_post(hugo_post)
        self.broadcast_a_linebot_post(post)
        return

    def broadcast_a_linebot_post(self, post: LinebotPost):
        """
        Broadcast a Linebot post.
        :param post: The LinebotPost object to broadcast.
        """
        # Load environment variables
        load_dotenv()
        token = os.getenv("LINE_TOKEN")
        url = "https://api.line.me/v2/bot/message/broadcast"
        
        print(f"Broadcasting post: {post.title}")
        print(f"Content: {post.content}")
        print(f"Image URL: {post.img_url}") # not used

        headers = {  
	    "Content-Type": "application/json",  
	    "Authorization": f"Bearer {token}"  
        }
        data = get_flex_message2(post.title, post.content, post.post_url)

        res = requests.post(url, headers = headers, data = json.dumps(data))  
        if res.status_code in (200, 204):  
            print(f"Request fulfilled with response: {res.text}")  
        else:  
            print(f"Request failed with response: {res.status_code}-{res.text}")
        
        return


def get_flex_message(title, content, post_url="", img_url="https://asroc-taiwan.github.io/website/img/tan-banner.jpeg"):
    data = {
        "messages": [
        {
            "type": "flex",
            "altText": "A New TAN Event!",
            "contents": {

        "type": "bubble",
        "hero": {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
            },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "maxLines": 1,
                        "weight": "bold",
                        "style": "normal",
                    "wrap": True
                    },
                    {
                        "type": "text",
                        "text": content,
                        "wrap": True,
                        "align": "start",
                        "scaling": True,
                        "maxLines": 100,
                        "offsetTop": "md"
                    }
                    ]
                }
            }
        }
        ]
    }

    return data

    
def get_flex_message2(title, content, post_url="", img_url="https://asroc-taiwan.github.io/website/img/tan-banner.jpeg"):
    data = {
        "messages": [
        {
            "type": "flex",
            "altText": "A New TAN Event!",
            "contents": {
                "type": "bubble",
                "hero": {
                "type": "image",
                "url": img_url,
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "size": "full"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "wrap": True,
                    "maxLines": 3
                    },
                    {
                    "type": "text",
                    "text": content,
                    "wrap": True,
                    "maxLines": 12,
                    "offsetTop": "md"
                    }
                ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                    "type": "uri",
                    "label": "Read the full content",
                    "uri": post_url
                }
        }
        ]
        }
        }
        }
        ]
    }

    return data
