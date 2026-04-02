
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('livro/', include('livro.urls')),
    path('usuario/', include('usuario.urls')),
    path('social/', include('social.urls')),
]
