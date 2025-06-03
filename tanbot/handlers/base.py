import os
import time
import pandas as pd
from dataclasses import dataclass
import importlib.resources as pkg_resources
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

@dataclass
class Post:
    title: str           # the email subject
    date: str            # the email timestamp, formatted as %Y-%m-%dT%H:%M:%S
    author: str          # the email sender
    summary: str         # the email snippet
    content: str         # the email full body content
    filename_head: str   # the filename header, formatted as YYYY_MM_DD_HH_MM_SS-message_id
    draft: bool

@dataclass
class ImagePost(Post):
    filename : str
    base_image: str       # the base image file path

class BaseHandler:
    def __init__(self, post_dir):
        self.post_dir = post_dir # the directory to save posts
        self._df = None    # the DataFrame to hold the data from Google Sheets
        self.timestamp_format = '%m/%d/%Y %H:%M:%S'
        self.date_format = '%Y-%m-%dT%H:%M:%S'
        self.filedate_format = '%Y_%m_%d_%H_%M_%S'
        self.filename_head_format = '%Y_%m_%d_%H_%M_%S-message_id'
        return

    @property
    def df(self):
        if self._df is None:
            raise ValueError("DataFrame is not loaded. Please load the DataFrame first.")
        return self._df
    
    @df.setter
    def df(self, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError("Value must be a pandas DataFrame.")
        self._df = value

    def _clean_content(self, content):
        """
        Clean the footer at the end of the content.
        """
        if not content:
            return content
        parts = content.split('--')
        if len(parts) > 1:
            content = '--'.join(parts[:-1])
        return content.strip()
    
    def _clean_subject(self, subject):
        """
        Clean the subject by removing the leading [TAN] in the subject line.
        """
        if not subject:
            return subject
        # remove the leading [TAN] from the subject
        if subject.startswith('[TAN]'):
            subject = subject[5:].strip()
        return subject


    def prepare_a_post(self, row):
        """
        convert a row of DataFrame to a Post object.
        """
        timestamp = row['Timestamp']
        subject = self._clean_subject(row['Subject'])
        sender = row['Sender']
        snippet = row['Snippet']
        content = self._clean_content(row['Full Body'])
        msg_id = row['Message ID']

        # Convert the str time to a time object
        timestamp = time.strptime(timestamp, self.timestamp_format)
        date = time.strftime(self.date_format, timestamp)
        
        # Create the filename
        # the date format in the filename better simple, 
        # we use YYYY_MM_DD_HH_MM_SS-message_id.zh.md
        filedate = time.strftime(self.filedate_format, timestamp)
        filename_head = f"{filedate}-{msg_id}"

        post = Post(
            title=subject,
            date=date,
            author=sender,
            summary=snippet,
            content=content,
            filename_head=filename_head,
            draft=False
        )
        return post
    

class BaseImageHandler(BaseHandler):
    def __init__(self, post_dir, base_image='base_image.png', base_font='times.ttf'):
        """
        Initialize the BaseImageHandler with the directory to save posts and the base image.
        If no directory is provided, it defaults to the directory of this script.
        """
        file_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(post_dir)
        self.post_dir = post_dir
        self.image_dir = post_dir

        self.base_image = pkg_resources.files("tanbot.resources.images").joinpath(base_image)
        self.base_font = pkg_resources.files("tanbot.resources.fonts").joinpath(base_font)
        

    def prepare_a_post(self, row):
        """
        Save a post from a df row in the data.
        """
        post = super().prepare_a_post(row)
        
        # Create the filename
        filename = f"{post.filename_head}.png"

        post = ImagePost(
            title=post.title,
            date=post.date,
            author=post.author,
            summary=post.summary,
            content=post.content,
            filename_head=post.filename_head,
            filename=filename,
            base_image=self.base_image,
            draft=False
        )
        return post
    
    def adjust_image(self, img):
        """
        Adjust the image to RGB mode and enhance the brightness.
        """
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        #filter = ImageEnhance.Brightness(img)
        #new_image = filter.enhance(0.5)
        return img

    def write_image_post(self, post):
        """
        Write the image post to a file.
        """
        if not os.path.exists(self.post_dir):
            os.makedirs(self.post_dir)
            print(f"Created directory {self.post_dir}.")

        filepath = os.path.join(self.post_dir, post.filename)

        # if the file already exists, we skip it
        if os.path.exists(filepath):
            print(f"File {filepath} already exists, skipping.")
            return

        print(f"Writing image post to {filepath}...")
        # Here you would implement the logic to save the image post
        # For now, we just print the filepath

        # here we assume the base image is already set and the same for all posts
        # in the further, we can add a method to change the base image from each post
        base_image = self.base_image
        base_font = self.base_font 
        
        print(f"Using base image: {base_image}")

        img = Image.open(base_image)
        img = self.adjust_image(img)
        draw = ImageDraw.Draw(img)

        # find the max width and height of the image
        width, height = img.size

        fontsize = 0.05 * height  # set the font size to 20% of the height
        font_title = ImageFont.truetype(str(base_font), fontsize*1.3)
        font_subtitle = ImageFont.truetype(str(base_font), int(fontsize * 1.1))

        # draw a title on the image
        title = "TAN-bot Post"
        subtitle = "Taiwan Astronomy Network"
        draw.text(
            (width * 0.38, height * 0.06),  # position the title at the top left corner
            title,
            font=font_title,
            fill=(0, 0, 0)  # black color for the title
        )
        # draw a subtitle on the image
        draw.text(
            (width * 0.32, height * 0.14),  # position the title at the top left corner
            subtilte,
            font=font_subtitle,
            fill=(0, 0, 0)  # black color for the title
        )

        # we only draw the email subject on the image as the message
        message = textwrap.wrap(post.title, 32)

        for line in message:
            # draw the text on the image
            draw.text(
                (width * 0.1, height * 0.55 + 1.2 * fontsize * message.index(line)),  # position the text at the top left corner
                line,
                font=font_subtitle,
                fill=(0, 0, 0)  # black color for the text
            )

        # save the image
        filepath = os.path.join(self.image_dir, post.filename)
        img.save(filepath, format='PNG')
        return
    
