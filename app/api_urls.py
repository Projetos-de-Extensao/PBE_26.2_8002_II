# app/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api import SalaViewSet

router = DefaultRouter()
router.register(r'sala', SalaViewSet, basename='sala')

urlpatterns = [
    path('', include(router.urls)),
]
