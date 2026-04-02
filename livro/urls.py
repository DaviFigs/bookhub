from django.urls import path, include
from . import views
urlpatterns = [
    path('buscar/', views.buscar, name='buscar'),
    path('livro/<int:id>/', views.livro, name='livro'),
    path('autor/<int:id>/', views.autor, name='autor'),
    ]