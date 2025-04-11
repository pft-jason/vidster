from django.shortcuts import render
from .models import * 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Media
from django.utils.timezone import now

def gallery_home(request):
    media = Media.objects.all().order_by('-created_at')
    
    context = {
        'media': media,
    }
    return render(request, 'GALLERY/gallery_home.html', context)

def media_detail(request, id):
    media = Media.objects.get(pk=id)
    
    context = {
        'item': media,
    }
    return render(request, 'GALLERY/media_detail.html', context)

def platform_list(request):
    platforms = PlatformInfo.objects.all()
    
    context = {
        'platforms': platforms,
    }
    return render(request, 'GALLERY/platform_list.html', context)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SaveUrlView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            url = data.get('url')
            if not url:
                return JsonResponse({'error': 'No URL provided'}, status=400)

            # Get or create the Media object
            media, created = Media.objects.get_or_create(url=url)

            # Add or update the UserMedia relationship
            user_media, user_media_created = UserMedia.objects.get_or_create(user=request.user, media=media)
            if not user_media_created:
                user_media.added_at = now()  # Update the added_at timestamp if it already exists
                user_media.save()

            print(f"{request.user} submitted: {url}")

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(f"Error: {e}")  # Log the error
            return JsonResponse({'error': str(e)}, status=500)
