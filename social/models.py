from django.db import models
from usuario.models import Usuario
from django.core.validators import MinValueValidator, MaxValueValidator

class Avaliacao(models.Model):
    TIPO_CHOICES = [
        (1, 'Livro'),
        (2, 'Autor')
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes')
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES)
    id_alvo = models.IntegerField()
    nota = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    data_publicacao = models.DateTimeField(auto_now_add=True)
    visibilidade = models.BooleanField(default=True)

    def __str__(self):
        return f"Avaliação de {self.usuario} - {self.nota}/5"

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

class Comentario(models.Model):
    TIPO_CHOICES = [
        (1, 'Livro'),
        (2, 'Autor'),
        (3, 'Comentário'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES)
    id_alvo = models.IntegerField()
    pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respostas')
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Comentário de {self.usuario}"

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-data_publicacao']

class ComentarioLike(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='likes')
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
