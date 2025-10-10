# 🛠️ Comandos Úteis - Tradutor de Artigos Técnicos

## 🚀 Comandos de Inicialização

### Desenvolvimento
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação (modo desenvolvimento)
python run.py

# Ou executar diretamente
python app.py

# Executar exemplos
python exemplo_uso.py
```

### Produção
```bash
# Com Gunicorn
gunicorn -c gunicorn.conf.py app:app

# Comando simples
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Com logs
gunicorn -w 4 -b 0.0.0.0:5000 app:app --access-logfile - --error-logfile -
```

## 🔧 Comandos de Manutenção

### Verificar Status
```bash
# Health check
curl http://localhost:5000/health

# Verificar idiomas suportados
curl http://localhost:5000/languages

# Verificar termos técnicos
curl http://localhost:5000/technical-terms
```

### Testes
```bash
# Teste básico de tradução
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello World","source_language":"en","target_language":"pt"}'
```

### Logs e Debug
```bash
# Ver logs em tempo real
tail -f logs/app.log

# Debug com logs detalhados
FLASK_DEBUG=1 python app.py

# Logs do Gunicorn
gunicorn --log-level debug app:app
```

## 📦 Comandos de Deploy

### Azure App Service
```bash
# Build e deploy
az webapp up --sku F1 --name tradutor-artigos-tecnicos

# Configurar variáveis de ambiente
az webapp config appsettings set --resource-group myResourceGroup --name tradutor-artigos-tecnicos --settings AZURE_TRANSLATOR_KEY="sua_chave"

# Ver logs
az webapp log tail --resource-group myResourceGroup --name tradutor-artigos-tecnicos
```

### Docker
```bash
# Build da imagem
docker build -t tradutor-artigos-tecnicos .

# Executar container
docker run -p 5000:5000 --env-file .env tradutor-artigos-tecnicos

# Executar com volumes
docker run -p 5000:5000 -v $(pwd)/data:/app/data tradutor-artigos-tecnicos
```

### Heroku
```bash
# Login
heroku login

# Criar app
heroku create tradutor-artigos-tecnicos

# Configurar variáveis
heroku config:set AZURE_TRANSLATOR_KEY="sua_chave"
heroku config:set AZURE_TRANSLATOR_ENDPOINT="seu_endpoint"
heroku config:set AZURE_TRANSLATOR_REGION="sua_regiao"

# Deploy
git push heroku main

# Ver logs
heroku logs --tail
```

## 🔍 Comandos de Diagnóstico

### Verificar Configuração
```bash
# Verificar variáveis de ambiente
python -c "from config import Config; Config.validate_config(); print('✅ Config OK')"

# Testar conexão Azure
python -c "from translator_service import TechnicalTranslator; t=TechnicalTranslator(); print('✅ Azure OK')"

# Verificar estrutura
python -c "import os; print('✅ Estrutura:', [d for d in os.listdir('.')])"
```

### Performance
```bash
# Teste de carga simples
for i in {1..10}; do
  curl -X POST http://localhost:5000/translate \
    -H "Content-Type: application/json" \
    -d '{"text":"Test message '${i}'","source_language":"en","target_language":"pt"}' &
done
wait
```

### Backup e Restore
```bash
# Backup dos dados
cp -r data/ backup/data-$(date +%Y%m%d)/

# Backup da configuração
cp .env backup/.env-$(date +%Y%m%d)

# Restore
cp backup/data-YYYYMMDD/* data/
```

## 🧹 Comandos de Limpeza

### Limpar Cache
```bash
# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +

# Limpar arquivos temporários
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

# Limpar logs antigos
find logs/ -name "*.log" -mtime +7 -delete
```

### Reset Completo
```bash
# Parar processos
pkill -f "python.*app.py"
pkill -f "gunicorn.*app:app"

# Limpar tudo
rm -rf __pycache__/
rm -rf *.pyc
rm -rf logs/*.log

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📊 Comandos de Monitoramento

### Sistema
```bash
# Ver processos Python
ps aux | grep python

# Ver uso de memória
ps aux | grep python | awk '{sum+=$6} END {print "Memória total: " sum/1024 " MB"}'

# Ver portas em uso
netstat -tlnp | grep :5000
```

### Aplicação
```bash
# Status da aplicação
curl -s http://localhost:5000/health | jq .

# Métricas básicas
curl -s http://localhost:5000/health | jq '.timestamp, .azure_configured'

# Teste de tradução rápida
time curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Test","source_language":"en","target_language":"pt"}'
```

## 🛡️ Comandos de Segurança

### Verificar Configurações
```bash
# Verificar permissões de arquivos
ls -la .env
ls -la data/

# Verificar se .env não está no git
git check-ignore .env

# Verificar variáveis expostas
env | grep AZURE
```

### Rotacionar Chaves
```bash
# Backup da chave atual
cp .env .env.backup

# Atualizar chave no Azure Portal
# Atualizar .env com nova chave

# Testar nova chave
python -c "from translator_service import TechnicalTranslator; t=TechnicalTranslator()"
```

## 🔄 Comandos de Atualização

### Atualizar Dependências
```bash
# Verificar versões
pip list --outdated

# Atualizar requirements.txt
pip freeze > requirements.txt

# Atualizar dependências
pip install -r requirements.txt --upgrade
```

### Atualizar Código
```bash
# Pull latest
git pull origin main

# Verificar mudanças
git diff HEAD~1

# Aplicar migrações se necessário
python -c "print('✅ Nenhuma migração necessária')"
```

## 📝 Comandos de Desenvolvimento

### Criar Novo Termo Técnico
```bash
# Adicionar termo via Python
python -c "
from translator_service import TechnicalTranslator
t = TechnicalTranslator()
t.add_technical_term('en', 'kubernetes', 'pt', 'Kubernetes')
print('✅ Termo adicionado')
"
```

### Testar Tradução Específica
```bash
python -c "
from translator_service import TechnicalTranslator
t = TechnicalTranslator()
result = t.translate_article('Your text here', 'en', 'pt')
print(result['translated_text'])
"
```

### Gerar Relatório de Uso
```bash
# Contar traduções (se implementado logging)
grep "Tradução concluída" logs/app.log | wc -l

# Estatísticas de idiomas
grep "source_language" logs/app.log | cut -d'"' -f4 | sort | uniq -c
```

---

**💡 Dica**: Mantenha estes comandos salvos para facilitar a manutenção e operação do sistema!
