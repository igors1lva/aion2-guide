import os
import sys

# Adiciona o diretório raiz ao sys.path para carregar os módulos locais do projeto
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app
