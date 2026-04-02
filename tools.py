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