from django.contrib import admin
from django.urls import path
from app_api import views

urlpatterns = [
    path('verify/<auth_token>', views.verify, name = 'verify'),
    path('SignUp/', views.ClientSignUp ,name='ClientSignUp'),
    path('accounts/login/' , views.login_attempt , name="login_attempt"),
    path('accounts/login/home/', views.home.as_view(), name='home'),
    path('uploads/<str:filename>', views.download, name='download')

]