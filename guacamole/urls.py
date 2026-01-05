from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login/', views.guac_login, name='guac_login'),
    path('session/', views.guac_session, name='guac_session'),

]
# This file defines the URL patterns for the Guacamole application.
