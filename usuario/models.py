from django.db import models
from livro.models import Livro
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=100)
    seguidores_count = models.IntegerField(default=0)
    seguindo_count = models.IntegerField(default=0)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    livro_favorito = models.ForeignKey(
        Livro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_favoritando'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
