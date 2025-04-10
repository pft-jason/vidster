class PlatformBase:
    @staticmethod
    def detect_video_id(url):
        """Extract the video ID from the URL."""
        raise NotImplementedError

    @staticmethod
    def generate_embed_url(video_id):
        """Generate the embed URL for the video."""
        raise NotImplementedError

    @staticmethod
    def fetch_thumbnail_and_title(video_id, url=None):
        """Fetch the thumbnail URL and title for the video."""
        raise NotImplementedError