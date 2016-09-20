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