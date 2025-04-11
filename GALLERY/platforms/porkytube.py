import re
import requests
from bs4 import BeautifulSoup
from .base import PlatformBase

class PorkyTube(PlatformBase):
    @staticmethod
    def detect_video_id(url):
        # Extract the video ID from the URL
        match = re.search(r'porkytube\.com\/videos\/(\d+)', url)
        return match.group(1) if match else None

    @staticmethod
    def generate_embed_url(video_id):
        # Use the video ID to generate the embed URL
        return f"https://www.porkytube.com/embed/{video_id}"

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
                with open("output.html", "w", encoding="utf-8") as file:
                    file.write(soup.prettify())
                    
                video_tag = soup.find('video', id='thisPlayer')
                if video_tag and 'poster' in video_tag.attrs:
                    thumbnail_url = video_tag['poster']   
                           

                # Extract title from the <title> element
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.strip()
        except Exception as e:
            print(f"Error fetching PorkyTube thumbnail or title: {e}")
        return thumbnail_url, title