from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import logging
from datetime import datetime
from translator_service import TechnicalTranslator
from config import Config

# Configuração de logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Validação de configuração na inicialização
try:
    Config.validate_config()
    logger.info("✅ Configuração validada com sucesso")
except ValueError as e:
    logger.error(f"❌ Erro de configuração: {e}")
    logger.warning("Verifique o arquivo .env e certifique-se de que todas as variáveis estão configuradas")

# Inicializa o tradutor (pode falhar se Azure não estiver configurado)
translator = None
try:
    translator = TechnicalTranslator()
    logger.info("✅ Tradutor inicializado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao inicializar tradutor: {e}")

@app.route('/')
def index():
    """Main page with translation interface"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_article():
    """Translate technical article"""
    try:
        # Verifica se o tradutor está inicializado
        if translator is None:
            logger.error("Tradutor não inicializado - Azure não configurado")
            return jsonify({
                'error': 'Serviço de tradução não disponível. Verifique a configuração do Azure.',
                'error_code': 'SERVICE_UNAVAILABLE'
            }), 503
        
        data = request.get_json()
        
        # Validação básica de entrada
        if not data:
            logger.warning("Requisição sem dados JSON")
            return jsonify({'error': 'Dados não fornecidos', 'error_code': 'NO_DATA'}), 400
        
        if 'text' not in data:
            logger.warning("Requisição sem campo 'text'")
            return jsonify({'error': 'Campo "text" não fornecido', 'error_code': 'NO_TEXT'}), 400
        
        text = data['text'].strip()
        
        # Validação de texto vazio
        if not text:
            logger.warning("Tentativa de traduzir texto vazio")
            return jsonify({'error': 'Texto vazio não pode ser traduzido', 'error_code': 'EMPTY_TEXT'}), 400
        
        # Validação de tamanho máximo (limite do Azure é ~50k caracteres)
        MAX_TEXT_LENGTH = 50000
        if len(text) > MAX_TEXT_LENGTH:
            logger.warning(f"Texto muito longo: {len(text)} caracteres (máximo: {MAX_TEXT_LENGTH})")
            return jsonify({
                'error': f'Texto muito longo. Máximo permitido: {MAX_TEXT_LENGTH} caracteres',
                'error_code': 'TEXT_TOO_LONG',
                'max_length': MAX_TEXT_LENGTH,
                'received_length': len(text)
            }), 400
        
        source_lang = data.get('source_language', Config.DEFAULT_SOURCE_LANGUAGE)
        target_lang = data.get('target_language', Config.DEFAULT_TARGET_LANGUAGE)
        preserve_formatting = data.get('preserve_formatting', True)
        
        # Validação de idiomas suportados
        supported_langs = translator.get_supported_languages()
        if source_lang != 'auto' and source_lang not in supported_langs:
            logger.warning(f"Idioma de origem não suportado: {source_lang}")
            return jsonify({
                'error': f'Idioma de origem não suportado: {source_lang}',
                'error_code': 'INVALID_SOURCE_LANGUAGE',
                'supported_languages': list(supported_langs.keys())
            }), 400
        
        if target_lang not in supported_langs:
            logger.warning(f"Idioma de destino não suportado: {target_lang}")
            return jsonify({
                'error': f'Idioma de destino não suportado: {target_lang}',
                'error_code': 'INVALID_TARGET_LANGUAGE',
                'supported_languages': list(supported_langs.keys())
            }), 400
        
        # Log da requisição (sem o texto completo para privacidade)
        logger.info(f"Tradução solicitada: {source_lang} -> {target_lang}, tamanho: {len(text)} caracteres")
        
        # Realiza a tradução
        result = translator.translate_article(
            text=text,
            source_language=source_lang,
            target_language=target_lang,
            preserve_formatting=preserve_formatting
        )
        
        logger.info(f"Tradução concluída em {result.get('translation_time', 0)}s")
        
        return jsonify({
            'translated_text': result['translated_text'],
            'confidence': result.get('confidence', 0),
            'detected_language': result.get('detected_language', source_lang),
            'translation_time': result.get('translation_time', 0)
        })
        
    except ValueError as e:
        # Erros de validação
        logger.error(f"Erro de validação: {e}")
        return jsonify({
            'error': str(e),
            'error_code': 'VALIDATION_ERROR'
        }), 400
        
    except Exception as e:
        # Erros inesperados
        logger.error(f"Erro inesperado na tradução: {e}", exc_info=True)
        return jsonify({
            'error': 'Erro interno ao processar tradução. Tente novamente.',
            'error_code': 'INTERNAL_ERROR',
            'message': str(e) if app.config.get('FLASK_ENV') == 'development' else None
        }), 500

@app.route('/languages')
def get_supported_languages():
    """Get list of supported languages"""
    return jsonify(translator.get_supported_languages())

@app.route('/technical-terms')
def get_technical_terms():
    """Get technical terms dictionary"""
    return jsonify(translator.get_technical_terms())

@app.route('/health')
def health_check():
    """Health check endpoint"""
    azure_configured = bool(Config.AZURE_TRANSLATOR_KEY and 
                           Config.AZURE_TRANSLATOR_ENDPOINT and 
                           Config.AZURE_TRANSLATOR_REGION)
    translator_ready = translator is not None
    
    status = 'healthy' if (azure_configured and translator_ready) else 'degraded'
    
    return jsonify({
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'azure_configured': azure_configured,
        'translator_ready': translator_ready,
        'supported_languages_count': len(translator.get_supported_languages()) if translator else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
