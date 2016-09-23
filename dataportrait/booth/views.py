from random import sample
from string import digits
from string import ascii_lowercase

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import resolve
from django.template.context import Context
from django.http import HttpResponse

from .models import Photo


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
                context['photo'] = photo
                context['network'] = network
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
                print('Error type ({1}): {0}'.format(ex.message, type(ex)))

        return HttpResponse('Created {0} codes'.format(missing_codes))
    else:
        return HttpResponse('Already {0} codes on database. Clear from admin'.format(max_codes))

def get_data(request):
    pass