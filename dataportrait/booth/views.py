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

                portrait.onUpload(code, portraitRel)
                portrait.onRequest(code, portraitRel, get_network_data(request))
                portrait.joinLayers(code, portraitRel)

                context['photo'] = portrait.getDataPortrait(portraitRel, code)
                context['photo_path'] = settings.MEDIA_URL + 'uploads/' + code + '/' + code + '_def.png'
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


def get_network_data(request):

    if request.user.social_auth:
        if request.user.social_auth.first().provider == 'linkedin-oauth2':
            ln_token = request.user.social_auth.get(provider='linkedin-oauth2').extra_data['access_token']
            ln_url = 'https://api.linkedin.com/v1/people/~:(headline,firstName,lastName,location,industry,summary,specialties,positions)?oauth2_access_token={0}&format=json'.format(ln_token)

            ln_resp = requests.get(url=ln_url)
            ln_data = json.loads(ln_resp.text)

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
                    ln_list.append(sanitize_social_text(position['title']))
                    ln_list.append(sanitize_social_text(position['summary']))
                    ln_list.append(sanitize_social_text(position['company']['industry']))
                    ln_list.append(sanitize_social_text(position['company']['name']))

            shuffle(ln_list)

            ln_text = ' '.join(ln_list)

            while len(ln_text) < 7000:
                ln_text *= 2

            return ln_text

        elif request.user.social_auth.first().provider == 'facebook':
            fb_social_auth = request.user.social_auth.get(provider='facebook')
            fb_url = 'https://graph.facebook.com/{0}/feed?access_token={1}'.format(fb_social_auth.uid, fb_social_auth.extra_data['access_token'])

            fb_resp = requests.get(url=fb_url)
            fb_data = json.loads(fb_resp.text)

            full_name = request.user.get_full_name()

            fb_list = []
            fb_banned_words = [full_name]

            for post in fb_data['data']:
                if 'story' in post:
                    fb_list.append(sanitize_social_text(post['story'], fb_banned_words))

                if 'message' in post:
                    fb_list.append(sanitize_social_text(post['message'], fb_banned_words))

            shuffle(fb_list)

            fb_text = ' '.join(fb_list)

            while len(fb_text) < 7000:
                fb_text *= 2

            return fb_text


def sanitize_social_text(social_text, banned_words=[]):
    social_text = social_text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
    social_text = social_text.strip()
    if social_text[-1:] is not '.':
        social_text += '.'

    for word in banned_words:
        social_text = social_text.replace(word, '')

    return social_text
