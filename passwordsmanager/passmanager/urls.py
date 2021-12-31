from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Views already touyched in the refactor proccess
    path('', views.home, name='home'),
    path('new/', views.new, name='new'),
    path('master/', views.master, name='master'),
    path('new_master/', views.new_master, name='new_master'),

    # path('entry/<int:pk>/delete/', views.delete, name='entry-delete'),
    # path('entry/<int:pk>/edit/', views.edit, name='entry-edit'),
]
