import tools
import requests
from django.http import HttpResponse

def buscar(request):
    if(request.method == 'GET'):
        query = request.GET.get('query')
        query = tools.normalizar_texto(query)
        url_livros = f'https://openlibrary.org/search.json?title={query}'
        url_autores = f'https://openlibrary.org/search.json?author={query}'
        response_livros = requests.get(url=url_livros)
        response_autores = requests.get(url=url_autores)

        context = {
            'livros': response_livros.json().get('docs', []),
            'autores': response_autores.json().get('docs', [])
        }
    return HttpResponse(str(context))

