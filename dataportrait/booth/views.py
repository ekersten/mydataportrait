import os
from random import sample
from random import shuffle
from string import digits
from string import ascii_lowercase
import requests
import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
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


def terms_and_conditions(request):
    context = Context({})
    return render(request, 'terms_and_conditions.html', context)

def picture(request):
    context = Context({})

    code = request.POST.get('code', None)
    code = str(code).lower()

    if code is not None:
        try:
            photo = Photo.objects.get(code__iexact=code)
            context['photo'] = photo
        except Photo.DoesNotExist:
            context['error'] = True

        return render(request, 'photo.html', context)


def generated_portrait(request, code):
    context = Context({
        'base_url': request.build_absolute_uri().replace(request.get_full_path(), ''),
        'share_image': get_image_url_for_code('1234')
    })
    return render(request, 'generated_portrait.html', context)



def picture_generator(request, code, network):
    context = Context({
        'base_url': request.build_absolute_uri().replace(request.get_full_path(), ''),
        'share_image': get_image_url_for_code('1234')
    })

    if not request.user.is_authenticated():
        return redirect(reverse('booth:index'))

    if code and network:
        code = str(code).lower()
        if code is not None:
            try:
                photo = Photo.objects.get(code__iexact=code)
                context['network'] = network

                # generate portrait
                portraitRel = os.path.join(settings.MEDIA_ROOT, 'uploads')

                network_text = get_network_data(request)
                if len(network_text) <= 0:
                    context['no_content_error'] = True
                else:
                    # check GET param to avoid creating image.
                    # THIS IS ONLY FOR TESTING!!!
                    if request.GET.get('nogen', 0) == 0:
                        print('calling onUpload')
                        portrait.onUpload(code, portraitRel)
                        print('calling onRequest')
                        portrait.onRequest(code, portraitRel, network_text.upper())
                        print('calling joinLayers')
                        portrait.joinLayers(code, portraitRel)

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
                    context['code'] = code
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


def get_image_url_for_code(code):
    image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', code, code + '_def.png')
    if os.path.exists(image_path) and os.path.isfile(image_path):
        return settings.MEDIA_URL + 'uploads/' + code + '/' + code + '_def.png'
    else:
        return ''


def get_network_data(request):
    print('get_network_data START')

    dummy_text = "Dive deep into digital at the DMA event. At Wunderman, data brings creativity to life. Get inspired by the data revolution. Find your inspiration in insight. Customer engagement begins with data. We’re in the inspiration business. Images are data, too: find out more with the click of a camera. Find inspiration in the mosaic of memories you create every day. The digital world is a platform where we can all leave our mark through innovation and motivation. Words paint a profile picture that speaks directly to us with their vivid clarity and personalized phrasing. The truest portrait is the one we never paint. See how the world sees you. Look data straight in the face. Data and digital combine in a portrait. The picture of perfection in a digital world. Go beyond the ones and twos to see the whole picture. Step back from the digital brink to glimpse your inner data. If you can see this, you’re missing the bigger picture. Your image of digital inspiration is pixelated with a mosaic of memories."

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
            if len(ln_text) == 0:
                ln_text = dummy_text

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

            if len(fb_text) == 0:
                fb_text = dummy_text

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
