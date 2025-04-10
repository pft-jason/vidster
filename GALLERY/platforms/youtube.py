import re
import requests
from bs4 import BeautifulSoup
from .base import PlatformBase

class YouTube(PlatformBase):
    @staticmethod
    def detect_video_id(url):
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
        return match.group(1) if match else None

    @staticmethod
    def generate_embed_url(video_id):
        return f"https://www.youtube.com/embed/{video_id}"

    @staticmethod
    def fetch_thumbnail_and_title(video_id, url=None):
        thumbnail_url = None
        title = None
        try:
            # Use YouTube's oEmbed endpoint
            response = requests.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json")
            if response.status_code == 200:
                data = response.json()
                title = data.get('title')  # Extract the video title
                thumbnail_url = data.get('thumbnail_url')  # Extract the thumbnail URL
        except Exception as e:
            print(f"Error fetching YouTube metadata via oEmbed: {e}")
        return thumbnail_url, title or "Unknown Title"