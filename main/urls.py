
from django.urls import path, include
from . import views

urlpatterns = [
    path('cadastro/',views.cadastro),#chama as urls do app auth
    path('',views.auth)
]
