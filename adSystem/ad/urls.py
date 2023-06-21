from django.urls import path
from . import views
from django.urls import re_path as url


urlpatterns = [
        url(r'^$', views.adListView.as_view(), name='ad'),
        url(r'^(?P<pk>\d+)/$', views.adDetailView.as_view(), name='ad-detail'),
        url(r'^newad$', views.create_ad, name='create-ad'),
        url(r'^(?P<pk>\d+)/delete$', views.delete_ad, name='delete_ad'),
        url(r'^editad/(?P<pk>\d+)$', views.edit_ad, name='edit-ad'),
        url(r'^edit-user$', views.edit_user, name='edit-user'),
        url(r'^create-offer$', views.create_offer, name='create-offer'),
        url(r'^delete-offer$', views.delete_offer, name='delete-offer'),
]
