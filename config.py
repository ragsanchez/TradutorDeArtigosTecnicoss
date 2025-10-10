import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure AI Translator Configuration
    AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')
    AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    AZURE_TRANSLATOR_REGION = os.getenv('AZURE_TRANSLATOR_REGION')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Translation Settings
    DEFAULT_SOURCE_LANGUAGE = os.getenv('DEFAULT_SOURCE_LANGUAGE', 'en')
    DEFAULT_TARGET_LANGUAGE = os.getenv('DEFAULT_TARGET_LANGUAGE', 'pt')
    
    # Technical terminology preservation
    TECHNICAL_TERMS_FILE = 'data/technical_terms.json'
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present"""
        required_vars = [
            'AZURE_TRANSLATOR_KEY',
            'AZURE_TRANSLATOR_ENDPOINT',
            'AZURE_TRANSLATOR_REGION'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(Config, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
