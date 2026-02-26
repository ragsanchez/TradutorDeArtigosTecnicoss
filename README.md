# 🌐 Tradutor de Artigos Técnicos com Azure AI

> **Projeto desenvolvido para o desafio de certificação AI-102 da DIO**

Uma aplicação web moderna e robusta para tradução automática de artigos técnicos, utilizando os serviços de IA do Azure. Desenvolvida com foco em garantir precisão terminológica e preservação do contexto específico do domínio técnico, facilitando o acesso a conteúdos especializados em diferentes idiomas.

## 🎯 Objetivo

Este projeto foi desenvolvido como parte do desafio de certificação AI-102, com o objetivo de criar uma solução completa de tradução automática que:

- ✅ Mantém a precisão de termos técnicos durante a tradução
- ✅ Preserva formatação original (Markdown, código, estrutura)
- ✅ Oferece interface intuitiva e responsiva
- ✅ Suporta múltiplos idiomas
- ✅ Facilita o acesso a conteúdos técnicos em diferentes idiomas

## ✨ Funcionalidades Principais

### 🔄 Tradução Inteligente
- **Tradução com Azure AI Translator**: Utiliza os serviços de tradução da Microsoft Azure
- **Preservação de Terminologia Técnica**: Mantém termos técnicos corretos através de dicionário customizado
- **Preservação de Formatação**: Mantém Markdown, blocos de código, e estrutura original
- **Detecção Automática de Idioma**: Identifica automaticamente o idioma de origem

### 🎨 Interface Moderna
- **Design Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Interface Intuitiva**: Layout limpo e fácil de usar
- **Feedback Visual**: Indicadores de progresso e status em tempo real
- **Atalhos de Teclado**: Produtividade aumentada com atalhos

### 📊 Recursos Adicionais
- **Estatísticas em Tempo Real**: Contagem de palavras, caracteres e tempo de tradução
- **Upload de Arquivos**: Suporte para arquivos `.txt` e `.md`
- **Exportação**: Download das traduções em formato texto
- **Múltiplos Idiomas**: Suporte para 11+ idiomas principais

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Conta Azure com serviço Translator configurado
- Chave de API do Azure Translator

### Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd TradutorDeArtigosTecnicoss
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   
   Copie o arquivo de exemplo e configure suas credenciais:
   ```bash
   # Windows
   copy env.example .env
   
   # Linux/Mac
   cp env.example .env
   ```
   
   Abra o arquivo `.env` e preencha com suas credenciais do Azure:
   ```env
   AZURE_TRANSLATOR_KEY=sua_chave_aqui
   AZURE_TRANSLATOR_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
   AZURE_TRANSLATOR_REGION=sua_regiao_aqui
   ```
   
   💡 **Dica**: O arquivo `env.example` contém instruções detalhadas e exemplos!

4. **Execute a aplicação**
   ```bash
   python run.py
   ```
   
   Ou diretamente:
   ```bash
   python app.py
   ```

5. **Acesse a aplicação**
   
   Abra seu navegador em: `http://localhost:5000`

### Uso Básico

1. **Cole ou digite** o texto técnico no campo "Texto Original"
2. **Selecione** os idiomas de origem e destino
3. **Clique em "Traduzir"** ou use o atalho `Ctrl+Enter`
4. **Visualize** a tradução no campo "Texto Traduzido"
5. **Copie ou baixe** o resultado traduzido

### Atalhos de Teclado

- `Ctrl+Enter`: Traduzir texto
- `Ctrl+K`: Limpar todos os campos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+
- **Framework Web**: Flask 2.3.3
- **Serviço de Tradução**: Azure AI Translator (azure-ai-translation-text)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.1.3
- **Ícones**: Font Awesome 6.0.0

## 📁 Estrutura do Projeto

```
TradutorDeArtigosTecnicoss/
├── app.py                 # Aplicação Flask principal
├── translator_service.py  # Serviço de tradução
├── config.py             # Configurações
├── run.py                # Script de inicialização
├── exemplo_uso.py        # Exemplos de uso programático
├── requirements.txt      # Dependências Python
├── templates/
│   └── index.html        # Interface web
├── static/
│   ├── css/
│   │   └── style.css     # Estilos customizados
│   └── js/
│       └── app.js        # Lógica JavaScript
└── data/
    └── technical_terms.json  # Dicionário de termos técnicos
```

## 🔧 Configuração do Azure

Para configurar o serviço Azure Translator:

1. Acesse o [Portal do Azure](https://portal.azure.com)
2. Crie um novo recurso "Translator"
3. Copie a chave de API e o endpoint
4. Configure a região do serviço
5. Adicione essas informações no arquivo `.env`

## 📝 Exemplos de Uso

### Uso Programático

```python
from translator_service import TechnicalTranslator

translator = TechnicalTranslator()

resultado = translator.translate_article(
    text="Machine learning is revolutionizing software development.",
    source_language="en",
    target_language="pt",
    preserve_formatting=True
)

print(resultado['translated_text'])
```

Execute `python exemplo_uso.py` para ver mais exemplos.

## 🌍 Idiomas Suportados

- Português (pt)
- Inglês (en)
- Espanhol (es)
- Francês (fr)
- Alemão (de)
- Italiano (it)
- Russo (ru)
- Japonês (ja)
- Coreano (ko)
- Chinês (zh)
- Árabe (ar)

## 📚 Documentação Adicional

- [Comandos Úteis](comandos_uteis.md) - Guia de comandos para desenvolvimento e deploy
- [Análise e Melhorias](ANALISE_E_MELHORIAS.md) - Documentação de análise do projeto

## 🤝 Contribuindo

Este é um projeto de aprendizado desenvolvido para o desafio AI-102. Sinta-se à vontade para:

- Reportar bugs
- Sugerir melhorias
- Adicionar novos recursos
- Melhorar a documentação

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como parte do desafio de projeto do curso de certificação AI-102 da DIO.

## 🙏 Agradecimentos

- DIO (Digital Innovation One) pelo curso e desafio
- Microsoft Azure pelos serviços de IA
- Comunidade open source pelas ferramentas utilizadas

---

**💡 Dica**: Para melhor experiência, use textos técnicos com formatação Markdown e código. O tradutor preservará toda a estrutura original!

