from django.urls import path
from . import views
from django.urls import re_path as url



urlpatterns = [
        url(r'^$', views.adListView.as_view(), name='ad'),
        url(r'^(?P<pk>\d+)/$', views.adDetailView.as_view(), name='ad-detail'),
        url(r'^newad$', views.create_ad, name='create-ad'),
        url(r'^(?P<pk>\d+)/delete$', views.delete_ad, name='delete_ad'),
]
