import os
from random import sample
from string import digits
from string import ascii_lowercase

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import resolve
from django.template.context import Context
from django.http import HttpResponse
from django.conf import settings
from .models import Photo

from portraitimage import portrait


def index(request):
    context = Context({})
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
                portrait.onRequest(code, portraitRel, get_data())
                portrait.joinLayers(code, portraitRel)

                context['photo'] = portrait.getDataPortrait(portraitRel, code)
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


def get_data():
    return ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est."
            " Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, "
            "justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. "
            "Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum."
            " Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. "
            "Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. "
            "Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. "
            "Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. "
            "Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. "
            "Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. "
            "Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. "
            "Praesent nibh felis, sagittis mollis mi id, varius fermentum felis."
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est."
            " Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, "
            "justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. "
            "Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum."
            " Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. "
            "Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. "
            "Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. "
            "Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. "
            "Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. "
            "Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. "
            "Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. "
            "Praesent nibh felis, sagittis mollis mi id, varius fermentum felis."
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est."
            " Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, "
            "justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. "
            "Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum."
            " Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. "
            "Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. "
            "Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. "
            "Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. "
            "Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. "
            "Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. "
            "Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. "
            "Praesent nibh felis, sagittis mollis mi id, varius fermentum felis."
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est."
            " Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, "
            "justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. "
            "Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum."
            " Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. "
            "Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. "
            "Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. "
            "Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. "
            "Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. "
            "Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. "
            "Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. "
            "Praesent nibh felis, sagittis mollis mi id, varius fermentum felis."
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est."
            " Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, "
            "justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. "
            "Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum."
            " Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. "
            "Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. "
            "Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. "
            "Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. "
            "Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. "
            "Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. "
            "Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. "
            "Praesent nibh felis, sagittis mollis mi id, varius fermentum felis."
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ut aliquet est."
            " Sed convallis dignissim justo nec porta. Sed volutpat, purus et efficitur porta, "
            "justo dui ornare eros, eget dictum dui massa nec massa. Nunc finibus gravida euismod. "
            "Praesent quis dui pellentesque, egestas nibh sit amet, fermentum dolor. Donec viverra pretium elementum."
            " Proin fermentum velit a nibh rutrum feugiat. Aliquam vehicula lorem quis justo pretium egestas. "
            "Aliquam erat volutpat. Suspendisse vestibulum tempor dui, ac mollis dolor pellentesque et. "
            "Vestibulum pharetra vel mauris eu egestas. Sed at placerat ligula. In hac habitasse platea dictumst. "
            "Etiam semper sollicitudin velit et hendrerit. Mauris eu pharetra libero.Aliquam vel tortor nec urna semper aliquam. "
            "Etiam at ante blandit, faucibus neque at, eleifend urna. Ut urna odio, tempor non ex nec, tristique volutpat sem. "
            "Quisque libero lorem, pulvinar in faucibus non, vulputate ut elit. Phasellus scelerisque lacinia mi, ut euismod felis mollis id. "
            "Cras pulvinar massa non ultricies ullamcorper. Mauris orci tellus, malesuada sed pellentesque rhoncus, condimentum sed sem. "
            "Praesent nibh felis, sagittis mollis mi id, varius fermentum felis."
            ).upper()