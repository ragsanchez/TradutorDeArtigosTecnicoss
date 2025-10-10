# Configuração do Gunicorn para produção

import os

# Configurações básicas
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = int(os.getenv('WEB_CONCURRENCY', '4'))
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Configurações de logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Configurações de processo
preload_app = True
max_requests = 1000
max_requests_jitter = 50

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configurações de performance
worker_tmp_dir = '/dev/shm' if os.path.exists('/dev/shm') else None

# Configurações específicas para Azure
if os.getenv('AZURE_ENVIRONMENT'):
    # Configurações otimizadas para Azure App Service
    workers = 2
    timeout = 120
    keepalive = 5
