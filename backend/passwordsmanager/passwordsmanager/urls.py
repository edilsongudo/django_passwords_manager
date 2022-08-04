from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('passmanager.urls')),
    path('api/', include('api.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]

handler404 = 'passmanager.views.error_404_view'
handler403 = 'passmanager.views.error_403_view'
handler500 = 'passmanager.views.error_500_view'
