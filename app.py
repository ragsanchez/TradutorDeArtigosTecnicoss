from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
from translator_service import TechnicalTranslator
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

try:
    Config.validate_config()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set.")

translator = TechnicalTranslator()

@app.route('/')
def index():
    """Main page with translation interface"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_article():
    """Translate technical article"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        source_lang = data.get('source_language', Config.DEFAULT_SOURCE_LANGUAGE)
        target_lang = data.get('target_language', Config.DEFAULT_TARGET_LANGUAGE)
        preserve_formatting = data.get('preserve_formatting', True)
        
        result = translator.translate_article(
            text=text,
            source_language=source_lang,
            target_language=target_lang,
            preserve_formatting=preserve_formatting
        )
        
        return jsonify({
            'translated_text': result['translated_text'],
            'confidence': result.get('confidence', 0),
            'detected_language': result.get('detected_language', source_lang),
            'translation_time': result.get('translation_time', 0)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'azure_configured': bool(Config.AZURE_TRANSLATOR_KEY)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
