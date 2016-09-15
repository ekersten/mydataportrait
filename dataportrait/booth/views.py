from django.shortcuts import render
from django.template.context import Context


def index(request):
    context = Context({})
    return render(request, 'index.html', context)