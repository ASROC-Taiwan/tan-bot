import os
import time
import glob
import pandas as pd
from dataclasses import dataclass
from ..base import Post, BaseHandler

@dataclass
class HugoPost(Post):
    filename: str = '2025_01_01_00_00_00-00000.zh-Hant.md'  # default filename, will be overwritten
  
class HugoHandler(BaseHandler):
    def __init__(self, post_dir):
        """
        Initialize the HugoHandler with the directory to save posts.
        :param post_dir: The directory where the posts will be saved.
        """
        super().__init__(post_dir)
        self._new_post = []
        return
    
    @property
    def new_posts(self):
        """
        Return the new posts that have been generated.
        """
        return self._new_post

    def generate_posts(self):
        df = self.df

        all_posts = glob.glob(os.path.join(self.post_dir, '*.zh-Hant.md'))
        last_post = None
        if len(all_posts) == 0:
            print("No posts found in the directory. Generate all posts from the data.")
        else:
            # search the lastest post from the file name
            # file name format: YYYY-MM-DDTHH:MM:SS-message_id.md
            all_posts.sort(reverse=True)
            last_post = all_posts[0] # is the latest post filename
            print(f"Latest post found: {last_post}")
            # find the datatime of the latest post from the filename
            last_datetime = last_post.split('/')[-1].split('-')[0:1]
            last_datetime = '-'.join(last_datetime)
            last_datetime = time.strptime(last_datetime, self.filedate_format)

        # iterate through the DataFrame to find the latest post
        has_updated = False
        for index, row in df.iterrows():
            post = self.prepare_a_post(row)
            
            if last_post is not None:
                # if the post date is earlier than the last post, skip it
                post_date = time.strptime(post.date, self.date_format)
                if post_date <= last_datetime:
                    print(f"Skipping post {post.filename} as it is older than the last post.")
                    continue
            self.write_post(post)
            self._new_post.append(post)
            has_updated = True
        return has_updated

    def write_post(self, post):
        """
        Write the post to a file.
        """

        if not os.path.exists(self.post_dir):
            os.makedirs(self.post_dir)
            print(f"Created directory {self.post_dir}.")

        filepath = os.path.join(self.post_dir, post.filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f'title: "{post.title}"\n')
            f.write(f"date: {post.date}+08:00\n") # ensure it's GMT+8
            f.write(f"draft: {str(post.draft).lower()}\n")
            #f.write(f"author: {post.author}\n")
            #f.write(f'summary: "{post.summary}"\n')
            f.write(f"---\n\n")
            f.write(post.content)
        print(f"Post {post.filename} written successfully.")
        return

    def prepare_a_post(self, row):
        """
        Save a post from a row in the data.
        """
        base_post = super().prepare_a_post(row)
        filename = f"{base_post.filename_head}.zh-Hant.md"

        post = HugoPost(
            title=base_post.title,
            date=base_post.date,
            author=base_post.author,
            summary=base_post.summary,
            content=base_post.content,
            filename_head=base_post.filename_head,
            filename=filename,
            draft=base_post.draft
        )
        return post
