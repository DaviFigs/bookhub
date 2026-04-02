from django.urls import path, include
from . import views
urlpatterns = [
    path('buscar/', views.buscar, name='buscar'),
]