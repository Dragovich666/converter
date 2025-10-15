"""
API Flight Crawler - Versão profissional com dados reais
Aplicação principal seguindo princípios SOLID e padrões de projeto
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import logging

# Importações dos módulos criados
from config import Config
from interfaces import FlightSearchParams, CabinClass
from provider_kiwi import KiwiFlightProvider
from provider_amadeus import AmadeusFlightProvider
from flight_service import FlightSearchService
from repository import SearchRepository

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Inicialização dos provedores (Strategy Pattern)
providers = [
    KiwiFlightProvider(),
    AmadeusFlightProvider(),
]

# Inicialização dos serviços (Dependency Injection)
flight_service = FlightSearchService(providers)
search_repository = SearchRepository()


@app.route('/')
def index():
    """Página inicial com formulário de busca"""
    return render_template('index.html')


@app.route('/api')
def api_info():
    """Endpoint de informações da API"""
    available_providers = [p.get_provider_name() for p in providers if p.is_available()]

    return jsonify({
        'api': 'Flight Crawler API',
        'version': '2.0',
        'description': 'API profissional com integração real de provedores de voos',
        'architecture': 'SOLID principles + Design Patterns',
        'providers_configured': available_providers,
        'total_providers': len(providers),
        'endpoints': {
            'GET /': 'Página inicial com formulário',
            'GET /api': 'Informações da API',
            'POST /consulta': 'Buscar voos com dados reais',
            'GET /consulta/<search_id>': 'Recuperar busca anterior',
            'GET /consulta/<search_id>/view': 'Ver resultados em HTML',
            'GET /historico': 'Listar histórico de buscas',
            'GET /stats': 'Estatísticas de buscas',
            'GET /health': 'Status da API'
        },
        'example_request': {
            'origem': 'GRU',
            'destino': 'GIG',
            'data_ida': '2025-02-01',
            'data_volta': '2025-02-10',
            'passageiros': 2,
            'criancas': 0,
            'classe': 'ECONOMY',
            'moeda': 'BRL'
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    available_providers = [
        {
            'name': p.get_provider_name(),
            'available': p.is_available(),
            'priority': p.get_priority()
        }
        for p in providers
    ]

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'providers': available_providers,
        'database': 'connected'
    }), 200


@app.route('/consulta', methods=['POST'])
def consulta():
    """
    Endpoint para buscar passagens aéreas com dados reais

    Body JSON:
    {
        "origem": "GRU",
        "destino": "GIG",
        "data_ida": "2025-02-01",
        "data_volta": "2025-02-10",
        "passageiros": 2,
        "criancas": 0,
        "classe": "ECONOMY",
        "moeda": "BRL"
    }

    Query Params:
    ?format=html - Retorna página HTML ao invés de JSON
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'erro': 'Dados não fornecidos',
                'mensagem': 'É necessário enviar um JSON no corpo da requisição'
            }), 400

        # Validação de campos obrigatórios
        campos_obrigatorios = ['origem', 'destino', 'data_ida', 'passageiros']
        campos_faltando = [campo for campo in campos_obrigatorios if campo not in data]

        if campos_faltando:
            return jsonify({
                'erro': 'Campos obrigatórios faltando',
                'campos_faltando': campos_faltando
            }), 400

        # Extrai e valida parâmetros
        origem = data['origem'].upper()
        destino = data['destino'].upper()
        data_ida_str = data['data_ida']
        data_volta_str = data.get('data_volta')
        passageiros = data.get('passageiros', 1)
        criancas = data.get('criancas', 0)
        classe = data.get('classe', 'ECONOMY').upper()
        moeda = data.get('moeda', 'BRL').upper()

        # Validação de códigos de aeroporto
        if len(origem) != 3 or len(destino) != 3:
            return jsonify({
                'erro': 'Códigos de aeroporto inválidos',
                'mensagem': 'Use códigos IATA de 3 letras (ex: GRU, GIG)'
            }), 400

        # Validação de datas
        try:
            data_ida = datetime.strptime(data_ida_str, '%Y-%m-%d')
            data_volta = datetime.strptime(data_volta_str, '%Y-%m-%d') if data_volta_str else None
        except ValueError:
            return jsonify({
                'erro': 'Formato de data inválido',
                'mensagem': 'Use o formato YYYY-MM-DD'
            }), 400

        # Validação de classe
        try:
            cabin_class = CabinClass[classe]
        except KeyError:
            return jsonify({
                'erro': 'Classe de cabine inválida',
                'mensagem': 'Use: ECONOMY, PREMIUM_ECONOMY, BUSINESS ou FIRST'
            }), 400

        # Cria parâmetros de busca
        try:
            params = FlightSearchParams(
                origin=origem,
                destination=destino,
                departure_date=data_ida,
                return_date=data_volta,
                adults=passageiros,
                children=criancas,
                cabin_class=cabin_class,
                currency=moeda
            )
        except ValueError as e:
            return jsonify({
                'erro': 'Erro de validação',
                'mensagem': str(e)
            }), 400

        logger.info(f"Iniciando busca: {origem} -> {destino} em {data_ida_str}")

        # Busca voos usando o serviço
        flights = flight_service.search_flights(params)

        # Salva a busca no repositório
        search_id = search_repository.save_search(data)
        flights_dict = [flight.to_dict() for flight in flights]
        search_repository.save_results(search_id, flights_dict)

        # Verifica se deve retornar HTML
        if request.args.get('format') == 'html':
            return render_template('results.html',
                search_id=search_id,
                timestamp=datetime.now().isoformat(),
                parametros={
                    'origem': origem,
                    'destino': destino,
                    'data_ida': data_ida_str,
                    'data_volta': data_volta_str,
                    'passageiros': passageiros,
                    'criancas': criancas,
                    'classe': classe,
                    'moeda': moeda
                },
                total_resultados=len(flights),
                voos=flights_dict
            )

        return jsonify({
            'sucesso': True,
            'search_id': search_id,
            'timestamp': datetime.now().isoformat(),
            'parametros': {
                'origem': origem,
                'destino': destino,
                'data_ida': data_ida_str,
                'data_volta': data_volta_str,
                'passageiros': passageiros,
                'criancas': criancas,
                'classe': classe,
                'moeda': moeda
            },
            'total_resultados': len(flights),
            'voos': flights_dict
        }), 200

    except Exception as e:
        logger.error(f"Erro na consulta: {str(e)}", exc_info=True)
        return jsonify({
            'erro': 'Erro interno do servidor',
            'mensagem': str(e)
        }), 500


@app.route('/consulta/<search_id>/view', methods=['GET'])
def view_consulta(search_id):
    """Renderiza os resultados de uma busca em HTML"""
    search = search_repository.get_search(search_id)

    if not search:
        return render_template('error.html',
            erro='Busca não encontrada',
            mensagem=f'Nenhuma busca encontrada com o ID {search_id}'
        ), 404

    results = search_repository.get_results(search_id)

    return render_template('results.html',
        search_id=search_id,
        timestamp=search['timestamp'],
        parametros=search['data'],
        total_resultados=len(results) if results else 0,
        voos=results
    )


@app.route('/consulta/<search_id>', methods=['GET'])
def get_consulta(search_id):
    """Recupera uma busca anterior pelo ID"""
    search = search_repository.get_search(search_id)

    if not search:
        return jsonify({
            'erro': 'Busca não encontrada',
            'mensagem': f'Nenhuma busca encontrada com o ID {search_id}'
        }), 404

    results = search_repository.get_results(search_id)

    return jsonify({
        'sucesso': True,
        'search_id': search_id,
        'timestamp': search['timestamp'],
        'status': search['status'],
        'parametros': search['data'],
        'total_resultados': len(results) if results else 0,
        'voos': results
    }), 200


@app.route('/historico', methods=['GET'])
def historico():
    """Lista todas as buscas realizadas"""
    searches = search_repository.list_all_searches()

    # Ordena por timestamp (mais recentes primeiro)
    searches.sort(key=lambda x: x['timestamp'], reverse=True)

    return jsonify({
        'sucesso': True,
        'total_buscas': len(searches),
        'buscas': searches
    }), 200


@app.route('/stats', methods=['GET'])
def stats():
    """Retorna estatísticas da API"""
    stats = search_repository.get_search_stats()

    return jsonify({
        'sucesso': True,
        'estatisticas': stats
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handler para rotas não encontradas"""
    return jsonify({
        'erro': 'Rota não encontrada',
        'mensagem': 'O endpoint solicitado não existe'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({
        'erro': 'Erro interno do servidor',
        'mensagem': 'Ocorreu um erro inesperado'
    }), 500


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Iniciando Flight Crawler API v2.0")
    logger.info("Arquitetura: SOLID + Design Patterns")
    logger.info(f"Provedores configurados: {len([p for p in providers if p.is_available()])}/{len(providers)}")
    logger.info(f"Acesse http://{Config.HOST}:{Config.PORT}")
    logger.info("=" * 60)

    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
