from django.db import models
from livro.models import Livro

class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    senha_hash = models.CharField(max_length=255)
    nome_completo = models.CharField(max_length=100)
    seguidores_count = models.IntegerField(default=0)
    seguindo_count = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    livro_favorito = models.ForeignKey(Livro, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios_favoritando')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

