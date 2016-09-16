from django.shortcuts import render
from django.template.context import Context

from .models import Photo


def index(request):
    context = Context({})
    return render(request, 'index.html', context)


def picture(request):
    context = Context({})

    code = request.POST.get('code', None)

    if code is not None:
         try:
             photo = Photo.objects.get(code=code)
             context['photo'] = photo
             return render(request, 'photo.html', context)
         except Photo.DoesNotExist:
             context['error'] = True
             return render(request, 'photo.html', context)