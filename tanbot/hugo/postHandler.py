import os
import time
import glob
import pandas as pd
from dataclasses import dataclass

@dataclass
class HugoPost:
    title: str
    date: str
    author: str
    summary: str
    content: str
    filename: str
    draft: bool = False

class PostHandler:
    def __init__(self, post_dir):
        self.post_dir = post_dir
        self._df = None

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

    def generate_posts(self):
        df = self.df

        all_posts = glob.glob(os.path.join(self.post_dir, '*.md'))
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
            last_datetime = last_post.split('/')[-1].split('-')[0:3]
            last_datetime = '-'.join(last_datetime)
            last_datetime = time.strptime(last_datetime, '%Y-%m-%dT%H:%M:%S')

        # iterate through the DataFrame to find the latest post
        has_updated = False
        for index, row in df.iterrows():
            post = self.prepare_a_post(row)
            
            if last_post is not None:
                # if the post date is earlier than the last post, skip it
                post_date = time.strptime(post.date, '%Y-%m-%dT%H:%M:%S')
                #print(f"debug: {last_datetime} vs {post_date}")
                if post_date <= last_datetime:
                    print(f"Skipping post {post.filename} as it is older than the last post.")
                    continue
            self.write_post(post)
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
            f.write(f"date: {post.date}\n")
            f.write(f"draft: {str(post.draft).lower()}\n")
            f.write(f"author: {post.author}\n")
            f.write(f'summary: "{post.summary}"\n')
            f.write(f"---\n\n")
            f.write(post.content)
        print(f"Post {post.filename} written successfully.")


    def prepare_a_post(self, row):
        """
        Save a post from a row in the data.
        """
        timestamp = row['Timestamp']
        subject = row['Subject']
        sender = row['Sender']
        snippet = row['Snippet']
        content = self._clean_content(row['Full Body'])
        msg_id = row['Message ID']

        # Convert the str time to a time object
        timestamp = time.strptime(timestamp, '%m/%d/%Y %H:%M:%S')
        date = time.strftime('%Y-%m-%dT%H:%M:%S', timestamp)
        
        # Create the filename
        filename = f"{date}-{msg_id}.md"

        post = HugoPost(
            title=subject,
            date=date,
            author=sender,
            summary=snippet,
            content=content,
            filename=filename
        )
        return post
