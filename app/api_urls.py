# app/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api import SalaViewSet, AlunoViewSet

router = DefaultRouter()
router.register(r'sala', SalaViewSet, basename='sala')
router.register(r'alunos', AlunoViewSet, basename='aluno')

urlpatterns = [
    path('', include(router.urls)),
]
