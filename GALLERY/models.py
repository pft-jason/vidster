from django.db import models
from django.contrib.auth.models import User
import re
import requests
from bs4 import BeautifulSoup
from GALLERY.platforms import youtube, vimeo, pornhub, gayporntube, twitch

PLATFORM_CLASSES = {
    'YouTube': youtube.YouTube,
    'Vimeo': vimeo.Vimeo,
    'Pornhub': pornhub.Pornhub,
    'GayPornTube': gayporntube.GayPornTube,
    'Twitch': twitch.Twitch,
}

class Media(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    url = models.URLField(unique=True)
    video_id = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=50, blank=True, null=True) 
    title = models.CharField(max_length=255, blank=True, null=True)
    embed_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    thumbnail_file = models.ImageField(upload_to='thumbnails/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.site or 'Unknown'}: {self.url}"
    
    def save(self, *args, **kwargs):
        # Detect the site and video ID
        if not self.site or not self.video_id:
            self.site, self.video_id = self.detect_site_and_extract_video_id(self.url)

        if self.site and self.video_id:
            platform_class = PLATFORM_CLASSES.get(self.site)
            if platform_class:
                self.embed_url = platform_class.generate_embed_url(self.video_id)
                self.thumbnail_url, self.title = platform_class.fetch_thumbnail_and_title(self.video_id, self.url)

        super().save(*args, **kwargs)

    @staticmethod
    def detect_site_and_extract_video_id(url):
        # Define site-specific patterns
        patterns = {
            'YouTube': {
                'domain': r'youtube\.com|youtu\.be',  # Match YouTube domains
                'regex': r'(?:v=|\/)([0-9A-Za-z_-]{11})'  # Extract video ID
            },
            'Vimeo': {
                'domain': r'vimeo\.com',  # Match Vimeo domain
                'regex': r'vimeo\.com\/(\d+)'  # Extract video ID
            },
            'Pornhub': {
                'domain': r'pornhub\.com',  # Match Pornhub domain
                'regex': r'viewkey=([0-9A-Za-z]+)'  # Extract viewkey
            },
            'GayPornTube': {
                'domain': r'gayporntube\.com',  # Match Pornhub domain
                'regex': r'gayporntube\.com\/video\/(\d+)'  # Extract viewkey
            },
            'Twitch': {  # Add Twitch support
                'domain': r'twitch\.tv',  # Match Twitch domain
                'regex': r'twitch\.tv\/videos\/(\d+)'  # Extract video ID
            },
            # 'TikTok': {  # Add TikTok support
            #     'domain': r'tiktok\.com',
            #     'regex': r'tiktok\.com\/.*\/video\/(\d+)'
            # },
        }

        for site, data in patterns.items():
            if re.search(data['domain'], url):
                match = re.search(data['regex'], url)
                if match:
                    return site, match.group(1)

        return None, None
