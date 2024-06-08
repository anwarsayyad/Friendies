"""Urls for the Frinds API"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'friendship', views.FriendsViewSet, basename='friendship')

app_name = 'friends'

urlpatterns = [
    path('', include(router.urls))
]
