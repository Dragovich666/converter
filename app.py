"""
API Crawler para buscar passagens aéreas mais baratas
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random
import uuid

app = Flask(__name__)
CORS(app)

# Banco de dados em memória
database = {}


class FlightDatabase:
    """Classe para gerenciar o banco de dados em memória"""
    
    def __init__(self):
        self.searches = {}
        self.results = {}
    
    def save_search(self, search_data):
        """Salva uma busca no banco de dados"""
        search_id = str(uuid.uuid4())
        self.searches[search_id] = {
            'id': search_id,
            'data': search_data,
            'timestamp': datetime.now().isoformat()
        }
        return search_id
    
    def save_results(self, search_id, results):
        """Salva os resultados de uma busca"""
        self.results[search_id] = results
    
    def get_search(self, search_id):
        """Recupera uma busca pelo ID"""
        return self.searches.get(search_id)
    
    def get_results(self, search_id):
        """Recupera os resultados de uma busca"""
        return self.results.get(search_id)
    
    def list_all_searches(self):
        """Lista todas as buscas realizadas"""
        return list(self.searches.values())


# Instância do banco de dados
db = FlightDatabase()


class FlightCrawler:
    """Crawler para simular busca de passagens aéreas"""
    
    # Lista de companhias aéreas fictícias
    AIRLINES = ['GOL', 'LATAM', 'Azul', 'Avianca', 'VoePass']
    
    # Lista de aeroportos brasileiros
    AIRPORTS = {
        'GRU': 'São Paulo - Guarulhos',
        'CGH': 'São Paulo - Congonhas',
        'GIG': 'Rio de Janeiro - Galeão',
        'SDU': 'Rio de Janeiro - Santos Dumont',
        'BSB': 'Brasília',
        'CNF': 'Belo Horizonte - Confins',
        'SSA': 'Salvador',
        'REC': 'Recife',
        'FOR': 'Fortaleza',
        'POA': 'Porto Alegre'
    }
    
    @staticmethod
    def search_flights(data_inicial, data_final, passageiros, tem_crianca=False, idade_crianca=None):
        """
        Simula a busca de voos
        
        Args:
            data_inicial: Data de início (formato: YYYY-MM-DD)
            data_final: Data de retorno (formato: YYYY-MM-DD)
            passageiros: Quantidade de passageiros
            tem_crianca: Se há crianças
            idade_crianca: Idade da(s) criança(s)
        
        Returns:
            Lista de voos encontrados
        """
        flights = []
        
        # Gera entre 5 e 10 resultados fictícios
        num_results = random.randint(5, 10)
        
        for i in range(num_results):
            # Seleciona aeroportos de origem e destino aleatórios
            origem_code = random.choice(list(FlightCrawler.AIRPORTS.keys()))
            destino_code = random.choice([k for k in FlightCrawler.AIRPORTS.keys() if k != origem_code])
            
            # Calcula desconto se houver crianças
            desconto = 0.15 if tem_crianca else 0
            
            # Preço base por passageiro
            preco_base = random.randint(200, 1500)
            
            # Calcula preço total considerando passageiros e desconto
            preco_crianca = preco_base * (1 - desconto) if tem_crianca else 0
            preco_adulto = preco_base
            
            # Preço total
            if tem_crianca and passageiros > 1:
                preco_total = (preco_adulto * (passageiros - 1)) + preco_crianca
            else:
                preco_total = preco_adulto * passageiros
            
            flight = {
                'id': str(uuid.uuid4()),
                'companhia': random.choice(FlightCrawler.AIRLINES),
                'origem': {
                    'codigo': origem_code,
                    'nome': FlightCrawler.AIRPORTS[origem_code]
                },
                'destino': {
                    'codigo': destino_code,
                    'nome': FlightCrawler.AIRPORTS[destino_code]
                },
                'data_ida': data_inicial,
                'data_volta': data_final,
                'horario_ida': f'{random.randint(0, 23):02d}:{random.choice(["00", "30"])}',
                'horario_volta': f'{random.randint(0, 23):02d}:{random.choice(["00", "30"])}',
                'passageiros': passageiros,
                'tem_crianca': tem_crianca,
                'idade_crianca': idade_crianca if tem_crianca else None,
                'preco_por_adulto': round(preco_adulto, 2),
                'preco_por_crianca': round(preco_crianca, 2) if tem_crianca else None,
                'preco_total': round(preco_total, 2),
                'moeda': 'BRL',
                'disponivel': True,
                'escalas': random.randint(0, 2),
                'duracao_estimada': f'{random.randint(1, 8)}h {random.randint(0, 59):02d}min'
            }
            
            flights.append(flight)
        
        # Ordena por preço (mais barato primeiro)
        flights.sort(key=lambda x: x['preco_total'])
        
        return flights


def validate_date(date_str):
    """Valida formato de data"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


@app.route('/')
def index():
    """Rota principal com informações da API"""
    return jsonify({
        'api': 'Flight Crawler API',
        'versao': '1.0',
        'endpoints': {
            '/consulta': {
                'metodo': 'POST',
                'descricao': 'Busca passagens aéreas',
                'parametros': {
                    'data_inicial': 'Data de início (YYYY-MM-DD) - obrigatório',
                    'data_final': 'Data de retorno (YYYY-MM-DD) - obrigatório',
                    'passageiros': 'Quantidade de passageiros (int) - obrigatório',
                    'tem_crianca': 'Se há crianças (boolean) - opcional, padrão: false',
                    'idade_crianca': 'Idade da criança (int) - opcional'
                }
            },
            '/consulta/<search_id>': {
                'metodo': 'GET',
                'descricao': 'Recupera resultados de uma busca anterior'
            },
            '/historico': {
                'metodo': 'GET',
                'descricao': 'Lista todas as buscas realizadas'
            }
        }
    })


@app.route('/consulta', methods=['POST'])
def consulta():
    """
    Endpoint para consultar passagens aéreas
    
    Espera JSON com:
    {
        "data_inicial": "2024-01-01",
        "data_final": "2024-01-10",
        "passageiros": 2,
        "tem_crianca": false,
        "idade_crianca": null
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'erro': 'Dados não fornecidos',
                'mensagem': 'É necessário enviar um JSON no corpo da requisição'
            }), 400
        
        # Validação dos campos obrigatórios
        campos_obrigatorios = ['data_inicial', 'data_final', 'passageiros']
        campos_faltando = [campo for campo in campos_obrigatorios if campo not in data]
        
        if campos_faltando:
            return jsonify({
                'erro': 'Campos obrigatórios faltando',
                'campos_faltando': campos_faltando
            }), 400
        
        # Extrai os parâmetros
        data_inicial = data.get('data_inicial')
        data_final = data.get('data_final')
        passageiros = data.get('passageiros')
        tem_crianca = data.get('tem_crianca', False)
        idade_crianca = data.get('idade_crianca')
        
        # Validações
        if not validate_date(data_inicial):
            return jsonify({
                'erro': 'Data inicial inválida',
                'mensagem': 'Use o formato YYYY-MM-DD'
            }), 400
        
        if not validate_date(data_final):
            return jsonify({
                'erro': 'Data final inválida',
                'mensagem': 'Use o formato YYYY-MM-DD'
            }), 400
        
        if not isinstance(passageiros, int) or passageiros < 1:
            return jsonify({
                'erro': 'Quantidade de passageiros inválida',
                'mensagem': 'Deve ser um número inteiro maior que 0'
            }), 400
        
        # Verifica se data inicial é anterior à data final
        if datetime.strptime(data_inicial, '%Y-%m-%d') >= datetime.strptime(data_final, '%Y-%m-%d'):
            return jsonify({
                'erro': 'Datas inválidas',
                'mensagem': 'A data inicial deve ser anterior à data final'
            }), 400
        
        if tem_crianca and idade_crianca is not None:
            if not isinstance(idade_crianca, int) or idade_crianca < 0 or idade_crianca > 12:
                return jsonify({
                    'erro': 'Idade da criança inválida',
                    'mensagem': 'Deve ser um número inteiro entre 0 e 12'
                }), 400
        
        # Salva a busca no banco de dados
        search_id = db.save_search(data)
        
        # Realiza a busca
        resultados = FlightCrawler.search_flights(
            data_inicial, 
            data_final, 
            passageiros, 
            tem_crianca, 
            idade_crianca
        )
        
        # Salva os resultados
        db.save_results(search_id, resultados)
        
        # Retorna a resposta
        return jsonify({
            'sucesso': True,
            'search_id': search_id,
            'parametros': {
                'data_inicial': data_inicial,
                'data_final': data_final,
                'passageiros': passageiros,
                'tem_crianca': tem_crianca,
                'idade_crianca': idade_crianca
            },
            'total_resultados': len(resultados),
            'voos': resultados
        }), 200
    
    except Exception as e:
        return jsonify({
            'erro': 'Erro interno do servidor',
            'mensagem': str(e)
        }), 500


@app.route('/consulta/<search_id>', methods=['GET'])
def get_consulta(search_id):
    """Recupera uma busca específica pelo ID"""
    search = db.get_search(search_id)
    
    if not search:
        return jsonify({
            'erro': 'Busca não encontrada',
            'mensagem': f'Nenhuma busca encontrada com o ID {search_id}'
        }), 404
    
    results = db.get_results(search_id)
    
    return jsonify({
        'sucesso': True,
        'search_id': search_id,
        'timestamp': search['timestamp'],
        'parametros': search['data'],
        'total_resultados': len(results) if results else 0,
        'voos': results
    }), 200


@app.route('/historico', methods=['GET'])
def historico():
    """Lista todas as buscas realizadas"""
    searches = db.list_all_searches()
    
    return jsonify({
        'sucesso': True,
        'total_buscas': len(searches),
        'buscas': searches
    }), 200


if __name__ == '__main__':
    print("Iniciando Flight Crawler API...")
    print("Acesse http://localhost:5000 para ver os endpoints disponíveis")
    app.run(debug=True, host='0.0.0.0', port=5000)
