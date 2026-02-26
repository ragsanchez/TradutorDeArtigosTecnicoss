import re
import json
import time
import os
import logging
from typing import Dict, List, Optional, Tuple
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from config import Config

# Logger para este módulo
logger = logging.getLogger(__name__)

class TechnicalTranslator:
    """Serviço de tradução de artigos técnicos usando Azure AI"""
    
    def __init__(self):
        """Inicializa o cliente de tradução do Azure"""
        self.client = None
        self.technical_terms = {}
        self.supported_languages = {}
        self._initialize_client()
        self._load_technical_terms()
        self._load_supported_languages()
    
    def _initialize_client(self):
        """Inicializa o cliente do Azure Translator"""
        try:
            if not Config.AZURE_TRANSLATOR_KEY:
                raise ValueError("AZURE_TRANSLATOR_KEY não configurada")
            if not Config.AZURE_TRANSLATOR_ENDPOINT:
                raise ValueError("AZURE_TRANSLATOR_ENDPOINT não configurado")
            if not Config.AZURE_TRANSLATOR_REGION:
                raise ValueError("AZURE_TRANSLATOR_REGION não configurada")
            
            credential = TranslatorCredential(
                key=Config.AZURE_TRANSLATOR_KEY,
                region=Config.AZURE_TRANSLATOR_REGION
            )
            self.client = TextTranslationClient(
                endpoint=Config.AZURE_TRANSLATOR_ENDPOINT,
                credential=credential
            )
            logger.info("Cliente Azure Translator inicializado com sucesso")
        except ValueError as e:
            logger.error(f"Erro de configuração ao inicializar cliente Azure: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente Azure: {e}")
            raise
    
    def _load_technical_terms(self):
        """Carrega dicionário de termos técnicos do arquivo JSON"""
        try:
            if os.path.exists(Config.TECHNICAL_TERMS_FILE):
                with open(Config.TECHNICAL_TERMS_FILE, 'r', encoding='utf-8') as f:
                    self.technical_terms = json.load(f)
                # Conta quantos termos foram carregados
                total_terms = sum(len(terms) for terms in self.technical_terms.values())
                logger.info(f"Carregados {total_terms} termos técnicos de {len(self.technical_terms)} idiomas")
            else:
                # Termos técnicos padrão
                self.technical_terms = {
                    "en": {
                        "api": "API",
                        "database": "banco de dados",
                        "framework": "framework",
                        "algorithm": "algoritmo",
                        "machine learning": "aprendizado de máquina",
                        "artificial intelligence": "inteligência artificial",
                        "cloud computing": "computação em nuvem",
                        "microservices": "microsserviços",
                        "devops": "DevOps",
                        "kubernetes": "Kubernetes",
                        "docker": "Docker",
                        "javascript": "JavaScript",
                        "python": "Python",
                        "react": "React",
                        "node.js": "Node.js",
                        "sql": "SQL",
                        "nosql": "NoSQL",
                        "rest": "REST",
                        "json": "JSON",
                        "xml": "XML",
                        "html": "HTML",
                        "css": "CSS"
                    }
                }
                self._save_technical_terms()
                logger.info("Termos técnicos padrão criados e salvos")
        except Exception as e:
            logger.warning(f"Erro ao carregar termos técnicos: {e}. Usando dicionário vazio.")
            self.technical_terms = {}
    
    def _save_technical_terms(self):
        """Salva dicionário de termos técnicos"""
        os.makedirs(os.path.dirname(Config.TECHNICAL_TERMS_FILE), exist_ok=True)
        with open(Config.TECHNICAL_TERMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.technical_terms, f, ensure_ascii=False, indent=2)
    
    def _load_supported_languages(self):
        """Carrega lista de idiomas suportados"""
        self.supported_languages = {
            "pt": "Português",
            "en": "Inglês",
            "es": "Espanhol",
            "fr": "Francês",
            "de": "Alemão",
            "it": "Italiano",
            "ru": "Russo",
            "ja": "Japonês",
            "ko": "Coreano",
            "zh": "Chinês",
            "ar": "Árabe"
        }
    
    def _preserve_technical_terms(self, text: str, source_lang: str, target_lang: str) -> str:
        """Preserva termos técnicos durante a tradução"""
        if source_lang not in self.technical_terms or target_lang not in self.technical_terms:
            return text
        
        source_terms = self.technical_terms.get(source_lang, {})
        target_terms = self.technical_terms.get(target_lang, {})
        
        # Cria mapeamento de termos
        term_mapping = {}
        for term, translation in source_terms.items():
            if translation in target_terms:
                term_mapping[term.lower()] = target_terms[translation]
        
        # Substitui termos no texto
        result_text = text
        for term, translation in term_mapping.items():
            # Usa regex para substituir apenas palavras completas
            pattern = r'\b' + re.escape(term) + r'\b'
            result_text = re.sub(pattern, translation, result_text, flags=re.IGNORECASE)
        
        return result_text
    
    def _preserve_formatting(self, text: str) -> Dict[str, str]:
        """Preserva formatação do texto (markdown, código, etc.)"""
        # Extrai blocos de código
        code_blocks = []
        code_pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.finditer(code_pattern, text, re.DOTALL)
        
        for i, match in enumerate(matches):
            placeholder = f"__CODE_BLOCK_{i}__"
            code_blocks.append(match.group(0))
            text = text.replace(match.group(0), placeholder)
        
        # Extrai código inline
        inline_code = []
        inline_pattern = r'`([^`]+)`'
        matches = re.finditer(inline_pattern, text)
        
        for i, match in enumerate(matches):
            placeholder = f"__INLINE_CODE_{i}__"
            inline_code.append(match.group(0))
            text = text.replace(match.group(0), placeholder)
        
        return {
            'text': text,
            'code_blocks': code_blocks,
            'inline_code': inline_code
        }
    
    def _restore_formatting(self, text: str, formatting_data: Dict[str, str]) -> str:
        """Restaura formatação após tradução"""
        # Restaura blocos de código
        for i, code_block in enumerate(formatting_data['code_blocks']):
            placeholder = f"__CODE_BLOCK_{i}__"
            text = text.replace(placeholder, code_block)
        
        # Restaura código inline
        for i, inline_code in enumerate(formatting_data['inline_code']):
            placeholder = f"__INLINE_CODE_{i}__"
            text = text.replace(placeholder, inline_code)
        
        return text
    
    def translate_article(self, text: str, source_language: str, target_language: str, 
                         preserve_formatting: bool = True) -> Dict:
        """Traduz um artigo técnico completo"""
        start_time = time.time()
        
        try:
            # Validação básica
            if not text or not text.strip():
                raise ValueError("Texto vazio não pode ser traduzido")
            
            logger.debug(f"Iniciando tradução: {len(text)} caracteres, {source_language} -> {target_language}")
            
            # Preserva formatação se solicitado (código, markdown, etc.)
            if preserve_formatting:
                formatting_data = self._preserve_formatting(text)
                text_to_translate = formatting_data['text']
                logger.debug(f"Formatação preservada: {len(formatting_data.get('code_blocks', []))} blocos de código")
            else:
                formatting_data = None
                text_to_translate = text
            
            # Divide o texto em chunks para tradução (Azure tem limite de tamanho)
            chunks = self._split_text_into_chunks(text_to_translate)
            logger.debug(f"Texto dividido em {len(chunks)} chunks")
            
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    translated_chunk = self._translate_chunk(chunk, source_language, target_language)
                    translated_chunks.append(translated_chunk)
                    logger.debug(f"Chunk {i+1}/{len(chunks)} traduzido")
                else:
                    translated_chunks.append(chunk)
            
            # Reconstrói o texto traduzido
            translated_text = ''.join(translated_chunks)
            
            # Restaura formatação se foi preservada
            if preserve_formatting and formatting_data:
                translated_text = self._restore_formatting(translated_text, formatting_data)
                logger.debug("Formatação restaurada")
            
            # Preserva termos técnicos do dicionário
            translated_text = self._preserve_technical_terms(
                translated_text, source_language, target_language
            )
            
            translation_time = time.time() - start_time
            
            logger.info(f"Tradução concluída: {len(text)} -> {len(translated_text)} caracteres em {translation_time:.2f}s")
            
            return {
                'translated_text': translated_text,
                'confidence': 0.95,  # Azure não retorna confiança diretamente
                'detected_language': source_language,
                'translation_time': round(translation_time, 2)
            }
            
        except ValueError as e:
            # Erros de validação são re-levantados
            logger.error(f"Erro de validação na tradução: {e}")
            raise
        except Exception as e:
            # Outros erros são logados e re-levantados com mensagem mais clara
            logger.error(f"Erro na tradução: {e}", exc_info=True)
            raise Exception(f"Erro ao traduzir artigo: {str(e)}")
    
    def _split_text_into_chunks(self, text: str, max_chunk_size: int = 5000) -> List[str]:
        """Divide o texto em chunks menores para tradução"""
        # Divide por parágrafos primeiro
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _translate_chunk(self, text: str, source_language: str, target_language: str) -> str:
        """Traduz um chunk de texto usando Azure Translator"""
        try:
            if not text or not text.strip():
                logger.warning("Tentativa de traduzir chunk vazio")
                return text
            
            input_text_elements = [InputTextItem(text=text)]
            
            # Faz a chamada para o Azure Translator
            response = self.client.translate(
                content=input_text_elements,
                to=[target_language],
                from_parameter=source_language if source_language != 'auto' else None
            )
            
            translation = response[0] if response else None
            if translation and translation.translations:
                translated_text = translation.translations[0].text
                logger.debug(f"Chunk traduzido: {len(text)} -> {len(translated_text)} caracteres")
                return translated_text
            else:
                logger.warning("Resposta do Azure sem tradução, retornando texto original")
                return text
                
        except Exception as e:
            logger.error(f"Erro ao traduzir chunk: {e}")
            # Em caso de erro, retorna o texto original para não quebrar o fluxo
            return text
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Retorna lista de idiomas suportados"""
        return self.supported_languages
    
    def get_technical_terms(self) -> Dict[str, Dict[str, str]]:
        """Retorna dicionário de termos técnicos"""
        return self.technical_terms
    
    def add_technical_term(self, source_lang: str, term: str, target_lang: str, translation: str):
        """Adiciona um novo termo técnico"""
        if source_lang not in self.technical_terms:
            self.technical_terms[source_lang] = {}
        if target_lang not in self.technical_terms:
            self.technical_terms[target_lang] = {}
        
        self.technical_terms[source_lang][term] = translation
        self._save_technical_terms()
