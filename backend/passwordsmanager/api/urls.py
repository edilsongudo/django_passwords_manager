from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('entries/', views.getEntries),
    path('entries/new/', views.newEntry),
    path('entries/delete/', views.deleteEntry),
    path('master-key/status/', views.has_user_defined_a_master_password),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
