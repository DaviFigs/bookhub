import tools
import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render


#melhorar tempo de requisição
def buscar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        query = tools.normalizar_texto(query)

        url_livros = f'https://openlibrary.org/search.json?q={query}'
        url_autores = f'https://openlibrary.org/search.json?author={query}'

        response_livros = requests.get(url_livros)
        response_autores = requests.get(url_autores)

        livros = []
        autores = []

        # livros
        if response_livros.status_code == 200:
            try:
                livros = response_livros.json().get('docs', [])
            except:
                print("Erro ao converter livros")

        # autores
        if response_autores.status_code == 200:
            try:
                autores = response_autores.json().get('docs', [])
            except:
                print("Erro ao converter autores")

        context = {
            'livros': tools.organizar_livros(livros),
            'autores': tools.organizar_autores(autores)
        }

        return render(request, 'index.html', context)


def livro(request, id):
    pass

def autor(request, id):
    pass

