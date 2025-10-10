#!/usr/bin/env python3
"""
Exemplo de uso do Tradutor de Artigos Técnicos
Demonstra como usar a API programaticamente
"""

import os
from dotenv import load_dotenv
from translator_service import TechnicalTranslator

def exemplo_basico():
    """Exemplo básico de tradução"""
    print("🔤 Exemplo Básico de Tradução")
    print("-" * 40)
    
    # Carrega configurações
    load_dotenv()
    
    # Inicializa o tradutor
    translator = TechnicalTranslator()
    
    # Texto de exemplo
    texto_exemplo = """
    # Machine Learning with Python
    
    Machine learning is a subset of artificial intelligence that focuses on 
    algorithms that can learn from data. Python provides excellent libraries 
    like scikit-learn, TensorFlow, and PyTorch for implementing ML models.
    
    ```python
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    ```
    
    The key concepts include:
    - Supervised learning
    - Unsupervised learning  
    - Deep learning
    - Neural networks
    """
    
    print("📝 Texto original:")
    print(texto_exemplo)
    print("\n🔄 Traduzindo...")
    
    # Traduz o texto
    resultado = translator.translate_article(
        text=texto_exemplo,
        source_language="en",
        target_language="pt",
        preserve_formatting=True
    )
    
    print("✅ Tradução concluída!")
    print(f"⏱️  Tempo: {resultado['translation_time']}s")
    print("\n📖 Texto traduzido:")
    print(resultado['translated_text'])

def exemplo_multiplos_idiomas():
    """Exemplo traduzindo para múltiplos idiomas"""
    print("\n🌍 Exemplo - Múltiplos Idiomas")
    print("-" * 40)
    
    load_dotenv()
    translator = TechnicalTranslator()
    
    texto = "Artificial Intelligence is revolutionizing software development."
    idiomas = ["pt", "es", "fr", "de"]
    
    print(f"📝 Texto original: {texto}")
    print("\n🔄 Traduzindo para múltiplos idiomas...")
    
    for idioma in idiomas:
        resultado = translator.translate_article(
            text=texto,
            source_language="en",
            target_language=idioma,
            preserve_formatting=False
        )
        
        nome_idioma = translator.get_supported_languages().get(idioma, idioma)
        print(f"🇧🇷 {nome_idioma}: {resultado['translated_text']}")

def exemplo_termos_tecnicos():
    """Exemplo demonstrando preservação de termos técnicos"""
    print("\n🔧 Exemplo - Preservação de Termos Técnicos")
    print("-" * 40)
    
    load_dotenv()
    translator = TechnicalTranslator()
    
    texto_tecnico = """
    The API uses REST endpoints to communicate with the database. 
    We implement microservices architecture with Docker containers 
    running on Kubernetes. The authentication uses JWT tokens with 
    OAuth 2.0 protocol.
    """
    
    print("📝 Texto técnico original:")
    print(texto_tecnico)
    
    # Traduz preservando termos técnicos
    resultado = translator.translate_article(
        text=texto_tecnico,
        source_language="en", 
        target_language="pt",
        preserve_formatting=True
    )
    
    print("\n✅ Tradução com preservação de termos:")
    print(resultado['translated_text'])

def exemplo_artigo_completo():
    """Exemplo com um artigo técnico mais completo"""
    print("\n📚 Exemplo - Artigo Técnico Completo")
    print("-" * 40)
    
    load_dotenv()
    translator = TechnicalTranslator()
    
    artigo_completo = """
    # Building Scalable Web Applications with Python

    ## Introduction
    
    Building scalable web applications requires careful consideration of 
    architecture, performance, and maintainability. Python offers several 
    frameworks that make this process easier.

    ## Key Frameworks

    ### Django
    Django is a high-level web framework that encourages rapid development 
    and clean, pragmatic design. It includes:
    
    - ORM (Object-Relational Mapping)
    - Admin interface
    - Authentication system
    - URL routing

    ### Flask
    Flask is a lightweight WSGI web application framework. It's designed 
    to make getting started quick and easy.

    ## Database Considerations

    For scalable applications, consider:

    ```python
    # Example database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'myapp',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

    ## Performance Optimization

    - Use caching strategies (Redis, Memcached)
    - Implement database indexing
    - Optimize queries
    - Use CDN for static assets

    ## Conclusion

    Building scalable web applications is a complex task that requires 
    understanding of multiple technologies and best practices.
    """
    
    print("📄 Artigo técnico completo")
    print(f"📊 Tamanho: {len(artigo_completo)} caracteres")
    
    # Traduz o artigo completo
    resultado = translator.translate_article(
        text=artigo_completo,
        source_language="en",
        target_language="pt", 
        preserve_formatting=True
    )
    
    print(f"✅ Tradução concluída em {resultado['translation_time']}s")
    print("\n📖 Primeira parte da tradução:")
    print(resultado['translated_text'][:500] + "...")

def main():
    """Função principal com menu de exemplos"""
    print("🚀 Tradutor de Artigos Técnicos - Exemplos de Uso")
    print("=" * 60)
    
    # Verifica se as configurações estão OK
    try:
        load_dotenv()
        if not all([
            os.getenv('AZURE_TRANSLATOR_KEY'),
            os.getenv('AZURE_TRANSLATOR_ENDPOINT'),
            os.getenv('AZURE_TRANSLATOR_REGION')
        ]):
            print("❌ Configuração do Azure não encontrada!")
            print("📝 Configure o arquivo .env com suas credenciais do Azure")
            return
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return
    
    # Menu de exemplos
    exemplos = [
        ("Básico", exemplo_basico),
        ("Múltiplos Idiomas", exemplo_multiplos_idiomas), 
        ("Termos Técnicos", exemplo_termos_tecnicos),
        ("Artigo Completo", exemplo_artigo_completo)
    ]
    
    while True:
        print("\n📋 Escolha um exemplo para executar:")
        for i, (nome, _) in enumerate(exemplos, 1):
            print(f"  {i}. {nome}")
        print("  0. Sair")
        
        try:
            escolha = int(input("\n👉 Digite sua escolha: "))
            
            if escolha == 0:
                print("👋 Até logo!")
                break
            elif 1 <= escolha <= len(exemplos):
                nome, funcao = exemplos[escolha - 1]
                print(f"\n🎯 Executando: {nome}")
                print("=" * 60)
                funcao()
            else:
                print("❌ Escolha inválida!")
                
        except ValueError:
            print("❌ Digite um número válido!")
        except KeyboardInterrupt:
            print("\n👋 Execução interrompida pelo usuário!")
            break
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")

if __name__ == "__main__":
    main()
