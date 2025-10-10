#!/usr/bin/env python3
"""
Script de inicialização para o Tradutor de Artigos Técnicos com Azure AI
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("🔍 Verificando configuração do ambiente...")
    
    required_vars = [
        'AZURE_TRANSLATOR_KEY',
        'AZURE_TRANSLATOR_ENDPOINT', 
        'AZURE_TRANSLATOR_REGION'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Variáveis de ambiente faltando:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Configure essas variáveis no arquivo .env:")
        print("   AZURE_TRANSLATOR_KEY=sua_chave_aqui")
        print("   AZURE_TRANSLATOR_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/")
        print("   AZURE_TRANSLATOR_REGION=sua_regiao_aqui")
        return False
    
    print("✅ Todas as variáveis de ambiente estão configuradas!")
    return True

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    try:
        import flask
        import azure
        import dotenv
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def create_directories():
    """Cria diretórios necessários se não existirem"""
    print("📁 Verificando estrutura de diretórios...")
    
    directories = ['templates', 'static/css', 'static/js', 'data']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Estrutura de diretórios verificada!")

def main():
    """Função principal"""
    print("🚀 Iniciando Tradutor de Artigos Técnicos com Azure AI")
    print("=" * 60)
    
    # Carrega variáveis de ambiente
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("📋 Arquivo .env carregado!")
    except:
        print("⚠️  Arquivo .env não encontrado, usando variáveis do sistema")
    
    # Verifica dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Cria diretórios
    create_directories()
    
    # Verifica configuração
    if not check_environment():
        print("\n🛠️  Para configurar o Azure Translator:")
        print("1. Acesse https://portal.azure.com")
        print("2. Crie um recurso 'Translator'")
        print("3. Copie as credenciais para o arquivo .env")
        sys.exit(1)
    
    print("\n🎉 Tudo pronto! Iniciando aplicação...")
    print("🌐 Acesse: http://localhost:5000")
    print("=" * 60)
    
    # Inicia a aplicação
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
