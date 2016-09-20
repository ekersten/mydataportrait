from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^photo/$', views.picture, name='picture'),
    url(r'^photo/(?P<code>[-\w\d]+)/(?P<network>[facebook|linkedin]+)$', views.picture_generator, name='picture_generator'),
]