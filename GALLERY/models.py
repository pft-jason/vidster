from django.db import models
from django.contrib.auth.models import User
import re
from django.utils.timezone import now
import requests
from bs4 import BeautifulSoup
from GALLERY.platforms import youtube, vimeo, pornhub, gayporntube, twitch, porkytube

PLATFORM_CLASSES = {
    'YouTube': youtube.YouTube,
    'Vimeo': vimeo.Vimeo,
    'Pornhub': pornhub.Pornhub,
    'GayPornTube': gayporntube.GayPornTube,
    'Twitch': twitch.Twitch,
    'PorkyTube': porkytube.PorkyTube,
}

class Media(models.Model):
    url = models.URLField(unique=True)
    video_id = models.CharField(max_length=100, blank=True)
    site = models.CharField(max_length=50, blank=True, null=True) 
    title = models.CharField(max_length=255, blank=True, null=True)
    embed_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    thumbnail_url_override = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # New field with the through model
    users = models.ManyToManyField('auth.User', through='UserMedia', related_name='media')

    def __str__(self):
        return f"{self.site or 'Unknown'}: {self.url}"
    
    @property
    def thumbnail(self):
        """Return the thumbnail_url_override if it exists, otherwise thumbnail_url."""
        return self.thumbnail_url_override or self.thumbnail_url
    
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
            'PorkyTube': {
                'domain': r'porkytube\.com',  # Match Pornhub domain
                'regex': r'porkytube\.com\/videos\/(\d+)'  # Extract video id
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
    
class UserMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=now)  # Track when the user added the media

    def __str__(self):
        return f"{self.user.username} added {self.media.url} at {self.added_at}"

class PlatformInfo(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('under_development', 'Under Development'),
    ]
    name = models.CharField(max_length=50, unique=True)
    homepage_url = models.URLField()
    logo_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    nsfw = models.BooleanField(default=False) 

    def __str__(self):
        return self.name