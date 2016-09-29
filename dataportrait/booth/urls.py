from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_random_codes', views.random_codes, name='random_codes'),
    url(r'^photo/$', views.picture, name='picture'),
    url(r'^auth-canceled/$', views.authcancel, name='authcancel'),
    url(r'^photo/(?P<code>[-\w\d]+)/(?P<network>[facebook|linkedin]+)$', views.picture_generator, name='picture_generator'),
    url(r'^portrait/(?P<code>[-\w\d]+)', views.generated_portrait, name='generated_portrait'),
]