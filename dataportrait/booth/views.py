import os
from random import sample
from random import shuffle
from string import digits
from string import ascii_lowercase
import requests
import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import resolve
from django.template.context import Context
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import logout
from .models import Photo

from portraitimage import portrait


def index(request):
    context = Context({})
    # always logout user
    logout(request)
    return render(request, 'index.html', context)


def picture(request):
    context = Context({})

    code = request.POST.get('code', None)
    code = str(code).lower()

    if code is not None:
        try:
            photo = Photo.objects.get(code=code)
            context['photo'] = photo
        except Photo.DoesNotExist:
            context['error'] = True

        return render(request, 'photo.html', context)


def picture_generator(request, code, network):
    context = Context({})

    if not request.user.is_authenticated():
        return redirect(resolve('booth:index'))

    if code and network:
        code = str(code).lower()
        if code is not None:
            try:
                photo = Photo.objects.get(code=code)
                context['network'] = network

                # generate portrait
                portraitRel = os.path.join(settings.MEDIA_ROOT, 'uploads')

                network_text = get_network_data(request)
                if len(network_text) <= 0:
                    context['no_content_error'] = True
                else:
                    print('calling onUpload')
                    #portrait.onUpload(code, portraitRel)
                    print('calling onRequest')
                    #portrait.onRequest(code, portraitRel, network_text)
                    print('calling joinLayers')
                    #portrait.joinLayers(code, portraitRel)

                    print('photo complete, sending data to template')
                    context['photo'] = portrait.getDataPortrait(portraitRel, code)
                    context['photo_path'] = settings.MEDIA_URL + 'uploads/' + code + '/' + code + '_def.png'

                    #get layers filenames for animation
                    print('Code: ' + code)
                    context['layers'] = [
                        portrait.getLayerURL(code, settings.MEDIA_URL + 'uploads/',1),
                        portrait.getLayerURL(code, settings.MEDIA_URL + 'uploads/',2),
                        portrait.getLayerURL(code, settings.MEDIA_URL + 'uploads/',3),
                        portrait.getLayerURL(code, settings.MEDIA_URL + 'uploads/',4),
                        portrait.getLayerURL(code, settings.MEDIA_URL + 'uploads/',5),
                    ]
            except Photo.DoesNotExist:
                context['error'] = True

            return render(request, 'photo_generator.html', context)


def random_codes(request):
    max_codes = 2000
    current_codes = Photo.objects.count()
    if current_codes< max_codes:
        missing_codes = max_codes - current_codes
        chars = digits + ascii_lowercase

        codes_list = []
        while len(codes_list) < missing_codes:
            s = ''.join(sample(chars, 4))
            if s not in codes_list:
                codes_list.append(s)

        print(codes_list)

        for code in codes_list:
            print('Crating: {0}'.format(code))
            try:
                p = Photo(code=code, image='')
                p.save()
            except Exception as ex:
                print('Error type ({0})'.format(type(ex)))

        return HttpResponse('Created {0} codes'.format(missing_codes))
    else:
        return HttpResponse('Already {0} codes on database. Clear from admin'.format(max_codes))


def authcancel(request):
    context = Context({})
    return render(request, 'auth_canceled.html', context)


def get_network_data(request):
    print('get_network_data START')

    if request.user.social_auth:
        print('user is auth')
        if request.user.social_auth.first().provider == 'linkedin-oauth2':
            print('user has linkedin')
            ln_token = request.user.social_auth.get(provider='linkedin-oauth2').extra_data['access_token']
            ln_url = 'https://api.linkedin.com/v1/people/~:(headline,firstName,lastName,location,industry,summary,specialties,positions)?oauth2_access_token={0}&format=json'.format(ln_token)
            print('fetching from linkedin')
            ln_resp = requests.get(url=ln_url)
            ln_data = json.loads(ln_resp.text)
            print('linkedin data fetched. parsing...')
            ln_list = []

            ln_list.append("{0} {1}".format(ln_data['firstName'], ln_data['lastName']))

            if 'headline' in ln_data:
                ln_list.append(sanitize_social_text(ln_data['headline']))

            if 'industry' in ln_data:
                ln_list.append(sanitize_social_text(ln_data['industry']))

            if 'summary' in ln_data:
                ln_list.append(sanitize_social_text(ln_data['summary']))

            if 'positions' in ln_data:
                for position in ln_data['positions']['values']:
                    if 'title' in position:
                        ln_list.append(sanitize_social_text(position['title']))

                    if 'summary' in position:
                        ln_list.append(sanitize_social_text(position['summary']))

                    if 'company' in position:
                        if 'industry' in position['company']:
                            ln_list.append(sanitize_social_text(position['company']['industry']))

                        if 'name' in position['company']:
                            ln_list.append(sanitize_social_text(position['company']['name']))

            shuffle(ln_list)

            ln_text = ' '.join(ln_list)
            if len(ln_text) <= 0:
                return ln_text

            while len(ln_text) < 7000:
                ln_text *= 2
            print('linkedin parsing complete. returning string')
            return ln_text

        elif request.user.social_auth.first().provider == 'facebook':
            print('user has facebook')
            fb_social_auth = request.user.social_auth.get(provider='facebook')
            fb_url = 'https://graph.facebook.com/v2.7/{0}/feed?access_token={1}'.format(fb_social_auth.uid, fb_social_auth.extra_data['access_token'])
            print('fetching from facebook')
            fb_resp = requests.get(url=fb_url)
            fb_data = json.loads(fb_resp.text)
            print('facebook data fetched. parsing...')
            full_name = request.user.get_full_name()
            print('full name: {0}'.format(request.user.get_full_name()))
            print('raw_facebook_data: ' + fb_resp.text)
            fb_list = []
            fb_banned_words = [full_name]

            for post in fb_data['data']:
                if 'story' in post:
                    fb_list.append(sanitize_social_text(post['story'], fb_banned_words))

                if 'message' in post:
                    fb_list.append(sanitize_social_text(post['message'], fb_banned_words))

            shuffle(fb_list)

            fb_text = ' '.join(fb_list)

            if len(fb_text) <= 0:
                return fb_text

            while len(fb_text) < 7000:
                fb_text *= 2
            print('facebook parsing complete. returning string')
            return fb_text


def sanitize_social_text(social_text, banned_words=[]):
    # remove line feeds, carriage returns and double spaces
    social_text = social_text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
    # remove surrounding whitespace
    social_text = social_text.strip()
    # add ending period if missing
    if social_text[-1:] is not '.':
        social_text += '.'

    # remove banned words ie: the username
    for word in banned_words:
        social_text = social_text.replace(word, '')

    return social_text
