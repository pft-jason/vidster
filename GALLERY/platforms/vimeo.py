import re
import requests
from bs4 import BeautifulSoup
from .base import PlatformBase

class Vimeo(PlatformBase):
    @staticmethod
    def detect_video_id(url):
        match = re.search(r'vimeo\.com\/(\d+)', url)
        return match.group(1) if match else None

    @staticmethod
    def generate_embed_url(video_id):
        return f"https://player.vimeo.com/video/{video_id}"

    @staticmethod
    def fetch_thumbnail_and_title(video_id, url=None):
        try:
            response = requests.get(f'https://vimeo.com/api/oembed.json?url=https://vimeo.com/{video_id}')
            if response.status_code == 200:
                data = response.json()
                return data.get('thumbnail_url'), data.get('title')
        except Exception as e:
            print(f"Error fetching Vimeo thumbnail or title: {e}")
        return None, None