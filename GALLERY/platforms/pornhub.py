import re
import requests
from bs4 import BeautifulSoup
from .base import PlatformBase

class Pornhub(PlatformBase):
    @staticmethod
    def detect_video_id(url):
        match = re.search(r'viewkey=([0-9A-Za-z]+)', url)
        return match.group(1) if match else None

    @staticmethod
    def generate_embed_url(video_id):
        return f"https://www.pornhub.com/embed/{video_id}"

    @staticmethod
    def fetch_thumbnail_and_title(video_id, url=None):
        thumbnail_url = None
        title = None
        try:
            response = requests.get(f"https://www.pornhub.com/view_video.php?viewkey={video_id}")
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
            print(f"Error fetching Pornhub thumbnail or title: {e}")
        return thumbnail_url, title