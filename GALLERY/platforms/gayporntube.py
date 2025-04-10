import re
import requests
from bs4 import BeautifulSoup
from .base import PlatformBase

class GayPornTube(PlatformBase):
    @staticmethod
    def detect_video_id(url):
        # Extract the video ID from the URL
        match = re.search(r'gayporntube\.com\/video\/(\d+)', url)
        return match.group(1) if match else None

    @staticmethod
    def generate_embed_url(video_id):
        # Use the video ID to generate the embed URL
        return f"https://www.gayporntube.com/embed/{video_id}"

    @staticmethod
    def fetch_thumbnail_and_title(video_id, url=None):
        thumbnail_url = None
        title = None
        try:
            # Use the full URL to fetch the page
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract thumbnail URL
                meta_tag = soup.find('meta', property='og:image')
                if meta_tag:
                    thumbnail_url = meta_tag['content']
                # Extract title
                title_tag = soup.find('meta', property='og:title')
                if title_tag:
                    title = title_tag['content']
        except Exception as e:
            print(f"Error fetching GayPornTube thumbnail or title: {e}")
        return thumbnail_url, title