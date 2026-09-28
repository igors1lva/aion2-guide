#!/usr/bin/env python3
"""
run.py - Script de execução simplificado para a aplicação Aion 2 Guides.
Execute no terminal:
    python run.py
"""

import sys
from app import app
from database import init_db

if __name__ == '__main__':
    print("=" * 65)
    print("   AION 2 GUIDES GLOBAL - PORTAL DA COMUNIDADE BRASILEIRA")
    print("=" * 65)
    print("[+] Inicializando banco de dados local SQLite (aion2_guides.db)...")
    init_db()
    print("[+] Banco de dados pronto!")
    print("[+] Servidor Flask ativo!")
    print("[+] Acesse pelo navegador: http://127.0.0.1:5000")
    print("=" * 65)
    print("Pressione CTRL + C no terminal para encerrar o servidor a qualquer momento.\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
