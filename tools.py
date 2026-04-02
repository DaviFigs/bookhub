import unicodedata
import re

def normalizar_texto(texto):
    # minúsculo
    texto = texto.lower()
    
    # remover acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    
    # remover caracteres especiais (mantém letras, números e espaço)
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    
    # substituir espaços por +
    texto = re.sub(r'\s+', '+', texto.strip())
    
    return texto

'''
    {'author_key': ['OL1608382A', 'OL6876487A'],
    'author_name': ['James Lamar Roberts', 'Roberts, James L.'],
    'cover_edition_key': 'OL23122188M',
    'cover_i': 10040573,
    'ebook_access': 'borrowable',
    'edition_count': 8,
    'first_publish_year': 1963,
    'has_fulltext': True,
    'ia': ['crimepunishmentn00robe', 'cliffsnotescrime00robe', 'cliffsnotesondos00dost'],
    'ia_collection': ['americana', 'delawarecountydistrictlibrary', 'inlibrary', 'internetarchivebooks', 'printdisabled'],
    'key': '/works/OL6224648W',
    'language': ['eng'],
    'lending_edition_s': 'OL24204374M',
    'lending_identifier_s': 'crimepunishmentn00robe',
    'public_scan_b': False,
    'title': 'Crime and Punishment Notes'}
'''

def organizar_livros(livros):
    livros_organizados = []

    for livro in livros:
        autores = livro.get('author_name', [])
        autor = autores[0] if autores else None

        livro_organizado = {
            'titulo': livro.get('title'),
            'autor': autor,
            'ano': livro.get('first_publish_year'),
        }

        livros_organizados.append(livro_organizado)

    return livros_organizados  
def organizar_autores(autores):
    autores_organizados = []

    for autor in autores:
        nome = autor.get('author_name', [])
        nome = nome[0] if nome else None

        autor_organizado = {
            'nome': nome,
            'principal_obra': autor.get('top_work'),
            'primeira_publicacao': autor.get('first_publish_year'),
            'quantidade_obras': autor.get('work_count'),
        }

        autores_organizados.append(autor_organizado)

    return autores_organizados
    