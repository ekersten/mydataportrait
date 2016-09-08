"""databooth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

import booth.views

urlpatterns = [
    url(r'^$', booth.views.index, name='index'),
    url(r'^validate_code/$', booth.views.validate_code, name='validate_code'),
    url(r'^get_media/$', booth.views.get_media, name='get_media'),
    url(r'^get_raw_media/$', booth.views.get_raw_media, name='get_raw_media'),
    url(r'^photo/(?P<code>[-\w\d]+)$', booth.views.photo, name='photo'),
    url('^', include('django.contrib.auth.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)