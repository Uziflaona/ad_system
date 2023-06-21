from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.urls import include
from ad.views import register_view, logout_view, profileView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('ad/', include('ad.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/ad/', permanent=True)),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view, name='register'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/profile/', profileView, name='profile'),
    path('accounts/profile/<int:tab>/', profileView, name='profile-tab'),
]

#TODO: remove that code

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
