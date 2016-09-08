import urllib
import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Photo

def index(request):
    context = {}
    return render(request, 'index.html', context)


def photo(request, code):
    context = {}
    user = request.user
    if user.is_authenticated:
        try:
            photo_obj = Photo.objects.get(code=code)
            context['photo'] = photo_obj
            return render(request, 'photo.html', context)
        except ObjectDoesNotExist:
            return redirect('index')
    else:
        return redirect('index')


def validate_code(request):
    response_data = {
        'valid': False
    }
    if request.method == 'POST':
        code = request.POST.get('code', None)
        if code is not None:
            try:
                photo = Photo.objects.get(code=code)
                response_data['valid'] = True
                response_data['url'] = photo.image.url
            except ObjectDoesNotExist:
                pass
    return JsonResponse(response_data)



def get_media(request):
    response_data = {
        'media': []
    }
    context = {}
    user = request.user

    if user.is_authenticated:
        if user.social_auth.filter(provider='facebook'):
            response_data['media'] = []
            facebook_data = user.social_auth.get(provider='facebook')
            url = "https://graph.facebook.com/v2.7/{0}/albums?access_token={1}".format(facebook_data.uid, facebook_data.extra_data['access_token'])
            json_obj = urllib.request.urlopen(url)
            facebook_photos = json.loads(json_obj.readall().decode('utf-8'))

            for photo in facebook_photos['data']:
                response_data['media'].append({
                    'url': photo['images'][len(photo['images'])-1]['source']
                })

        if user.social_auth.filter(provider='instagram'):

            instagram_data = user.social_auth.get(provider='instagram')
            url = "https://api.instagram.com/v1/users/{0}/media/recent/?access_token={1}".format(instagram_data.uid, instagram_data.extra_data['access_token'])
            json_obj = urllib.request.urlopen(url)
            instagram_photos = json.loads(json_obj.readall().decode('utf-8'))

            for photo in instagram_photos['data']:
                response_data['media'].append({
                    'url': photo['images']['thumbnail']['url']
                })
    else:
        del response_data['media']

    return JsonResponse(response_data)