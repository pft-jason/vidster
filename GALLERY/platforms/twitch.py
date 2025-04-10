import re
import requests
from bs4 import BeautifulSoup
from .base import PlatformBase
from dotenv import load_dotenv
import os

load_dotenv()

class Twitch(PlatformBase):
    CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
    OAUTH_TOKEN = None  # This will be set dynamically

    @staticmethod
    def get_oauth_token():
        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "client_id": Twitch.CLIENT_ID,
            "client_secret": Twitch.CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            Twitch.OAUTH_TOKEN = response.json().get("access_token")
            return Twitch.OAUTH_TOKEN
        else:
            print(f"Error fetching OAuth token: {response.text}")
            return None

    @staticmethod
    def detect_video_id(url):
        match = re.search(r'twitch\.tv\/videos\/(\d+)', url)
        return match.group(1) if match else None

    @staticmethod
    def generate_embed_url(video_id):
        return f"https://player.twitch.tv/?video={video_id}&parent=localhost&autoplay=false"

    @staticmethod
    def fetch_thumbnail_and_title(video_id, url=None):
        if not Twitch.OAUTH_TOKEN:
            Twitch.get_oauth_token()
            
        print(f"CLIENT_ID: {os.getenv('TWITCH_CLIENT_ID')}")
        print(f"CLIENT_SECRET: {os.getenv('TWITCH_CLIENT_SECRET')}")

        thumbnail_url = None
        title = None
        try:
            headers = {
                "Client-ID": Twitch.CLIENT_ID,
                "Authorization": f"Bearer {Twitch.OAUTH_TOKEN}"
            }
            response = requests.get(f"https://api.twitch.tv/helix/videos?id={video_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    video_data = data["data"][0]
                    print(video_data)
                    title = video_data.get("title")
                    thumbnail_url = video_data.get("thumbnail_url")
                    # Replace placeholder dimensions in the thumbnail URL
                    if thumbnail_url:
                        thumbnail_url = thumbnail_url.replace("%{width}", "1920").replace("%{height}", "1080")
            else:
                print(f"Error fetching Twitch video metadata: {response.text}")
        except Exception as e:
            print(f"Error fetching Twitch thumbnail or title via API: {e}")
        return thumbnail_url, title or "Unknown Title"