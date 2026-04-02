from django.urls import path, include
from . import views
urlpatterns = [
    path('comentario/<int:id>/', views.comentario, name='comentario'),
    path('avaliacao/<int:id>/', views.avaliacao, name='avaliacao'),
    
]