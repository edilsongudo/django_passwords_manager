from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Views already touyched in the refactor proccess
    path('', views.home, name='home'),
    path('new/', views.new, name='entry-new'),
    path('master/', views.master, name='master'),

    # Views to touch/delete or use as inspiration to refactor
    path('mypasswords/', views.showpasswords, name='mypasswords'),
    path('entry/<int:pk>/delete/', views.delete, name='entry-delete'),
    path('entry/<int:pk>/edit/', views.edit, name='entry-edit'),
]
