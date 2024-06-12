from django.urls import path
from .views import UserRegisterView, UserLoginView
from .views import get_csrf_token
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login-auth'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]
