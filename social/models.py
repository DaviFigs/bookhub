from django.db import models
from usuario.models import Usuario
from livro.models import Livro, Autor
from django.core.validators import MinValueValidator, MaxValueValidator


class Avaliacao(models.Model):
    TIPO_CHOICES = [
        (1, 'Livro'),
        (2, 'Autor')
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes')
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES)
    id_alvo = models.PositiveIntegerField()  # ID do Livro ou Autor
    nota = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    conteudo = models.TextField(blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    visibilidade = models.BooleanField(default=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Avaliação de {self.usuario} - {self.nota}/5"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ['-data_publicacao']
        unique_together = ('usuario', 'tipo', 'id_alvo')


class AvaliacaoVote(models.Model):
    VOTO_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacao_votes')
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='votes')
    voto = models.SmallIntegerField(choices=VOTO_CHOICES)
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'avaliacao'], name='unique_vote')
        ]
        verbose_name = "Voto em Avaliação"
        verbose_name_plural = "Votos em Avaliações"


class Comentario(models.Model):
    TIPO_CHOICES = [
        (1, 'Livro'),
        (2, 'Autor'),
        (3, 'Comentário'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES)
    id_alvo = models.PositiveIntegerField()  # ID do Livro, Autor ou Comentário
    pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respostas')
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Comentário de {self.usuario}"

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        


class ComentarioLike(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentario_likes')
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='likes')
    data_like = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'comentario')
        verbose_name = "Like em Comentário"
        verbose_name_plural = "Likes em Comentários"


class Seguidor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguidores')
    seguindo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarios_seguindo')
    data_seguindo = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'seguindo')
        verbose_name = "Seguidor"
        verbose_name_plural = "Seguidores"
        


class SeguidorAutor(models.Model):
    """Modelo para rastrear seguidores de autores"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='autores_seguindo')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='seguidores_usuarios')
    data_seguindo = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'autor')
        verbose_name = "Seguidor de Autor"
        verbose_name_plural = "Seguidores de Autores"


class StatusLeitura(models.Model):
    """Rastreia o status de leitura de um livro por um usuário"""
    STATUS_CHOICES = [
        ('nao_iniciado', 'Não Iniciado'),
        ('lendo', 'Lendo'),
        ('lido', 'Lido'),
        ('abandonado', 'Abandonado'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='leituras')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='leituras')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_iniciado')
    data_inicio = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    numero_paginas_lidas = models.PositiveIntegerField(default=0)
    favorito = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario} - {self.livro} ({self.status})"

    class Meta:
        unique_together = ('usuario', 'livro')
        verbose_name = "Status de Leitura"
        verbose_name_plural = "Status de Leituras"
