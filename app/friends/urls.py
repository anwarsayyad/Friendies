"""Urls for the Frinds API"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'friendship', views.FriendsViewSet, basename='friendship')
router.register(
    r'users/serach',
    views.UserSerachViewSet,
    basename='search-user'
)

app_name = 'friends'

urlpatterns = [
    path('', include(router.urls))
]
