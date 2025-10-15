"""
Configurações da aplicação - Centraliza todas as configurações (Single Responsibility)
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações centralizadas da aplicação"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # API Keys para provedores de voos
    AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY', 'pqBks5Uh2T41rQRRl3QwoVXMkQGhUAum')
    AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET', 'LzAsRUC8TEpOEtrt')

    KIWI_API_KEY = os.getenv('KIWI_API_KEY', '')

    AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY', '')

    # URLs das APIs
    # AMADEUS_BASE_URL = 'https://api.amadeus.com'
    AMADEUS_BASE_URL = 'https://test.api.amadeus.com'  # Ambiente de teste
    KIWI_BASE_URL = 'https://api.tequila.kiwi.com'
    AVIATIONSTACK_BASE_URL = 'http://api.aviationstack.com/v1'

    # Configurações de requisições
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    CACHE_TTL = 3600  # 1 hora em segundos

    # Configurações de busca
    MAX_RESULTS_PER_PROVIDER = 50
    DEFAULT_CURRENCY = 'BRL'

