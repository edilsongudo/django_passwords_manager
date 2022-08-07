from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Views already touyched in the refactor proccess
    path('', views.home, name='home'),
    path('new/', views.new, name='new'),
    path('delete/', views.delete, name='delete'),
    path('master/', views.master, name='master'),
    path('new_master/', views.new_master, name='new_master'),
    path(
        'generate_password/', views.generate_password, name='generate_password'
    ),
    # path('entry/<int:pk>/delete/', views.delete, name='entry-delete'),
    # path('entry/<int:pk>/edit/', views.edit, name='entry-edit'),
]
