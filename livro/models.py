from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Autor(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    descricao = models.TextField()
    seguidores_count = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

class Livro(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    nome = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    data_publicacao = models.DateField()
    descricao = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

class Genero(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

class LivroGenero(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='generos')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('livro', 'genero')
        verbose_name = "Livro-Gênero"
        verbose_name_plural = "Livro-Gêneros" 

class AutorGenero(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='generos')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('autor', 'genero')
        verbose_name = "Autor-Gênero"
        verbose_name_plural = "Autor-Gêneros"

