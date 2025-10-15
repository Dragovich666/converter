"""
Exemplo de uso da API Flight Crawler v2.0
Demonstra como fazer requisições para buscar voos reais
"""
import requests
import json
from datetime import datetime, timedelta

# URL base da API
BASE_URL = "http://localhost:5000"


def exemplo_busca_simples():
    """Exemplo de busca simples de voos"""
    print("=" * 60)
    print("EXEMPLO 1: Busca Simples de Voos")
    print("=" * 60)

    # Dados da busca
    data_ida = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    data_volta = (datetime.now() + timedelta(days=37)).strftime('%Y-%m-%d')

    payload = {
        "origem": "GRU",  # São Paulo
        "destino": "GIG",  # Rio de Janeiro
        "data_ida": data_ida,
        "data_volta": data_volta,
        "passageiros": 2,
        "criancas": 0,
        "classe": "ECONOMY",
        "moeda": "BRL"
    }

    print(f"\nBuscando voos:")
    print(f"  Origem: {payload['origem']}")
    print(f"  Destino: {payload['destino']}")
    print(f"  Ida: {payload['data_ida']}")
    print(f"  Volta: {payload['data_volta']}")
    print(f"  Passageiros: {payload['passageiros']}")

    # Faz a requisição
    response = requests.post(f"{BASE_URL}/consulta", json=payload)

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Sucesso!")
        print(f"  Search ID: {result['search_id']}")
        print(f"  Total de voos encontrados: {result['total_resultados']}")

        # Mostra os 3 voos mais baratos
        if result['voos']:
            print(f"\n🎯 Top 3 Voos Mais Baratos:")
            for i, voo in enumerate(result['voos'][:3], 1):
                print(f"\n  {i}. {voo['airline']} - R$ {voo['price']:.2f}")
                print(f"     Provedor: {voo['provider']}")
                print(f"     Partida: {voo['departure_datetime']}")
                print(f"     Chegada: {voo['arrival_datetime']}")
                print(f"     Duração: {voo['duration_formatted']}")
                print(f"     Escalas: {voo['stops']}")
                if voo['booking_url']:
                    print(f"     Reservar: {voo['booking_url'][:50]}...")

        return result['search_id']
    else:
        print(f"\n❌ Erro: {response.status_code}")
        print(response.json())
        return None


def exemplo_recuperar_busca(search_id):
    """Exemplo de como recuperar uma busca anterior"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Recuperar Busca Anterior")
    print("=" * 60)

    if not search_id:
        print("❌ Nenhum search_id fornecido")
        return

    print(f"\nRecuperando busca: {search_id}")

    response = requests.get(f"{BASE_URL}/consulta/{search_id}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Busca recuperada!")
        print(f"  Timestamp: {result['timestamp']}")
        print(f"  Status: {result['status']}")
        print(f"  Total de resultados: {result['total_resultados']}")
    else:
        print(f"\n❌ Erro: {response.status_code}")
        print(response.json())


def exemplo_historico():
    """Exemplo de visualização do histórico"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Histórico de Buscas")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/historico")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Total de buscas: {result['total_buscas']}")

        if result['buscas']:
            print(f"\nÚltimas 5 buscas:")
            for i, busca in enumerate(result['buscas'][:5], 1):
                params = busca['data']
                print(f"\n  {i}. {params['origem']} → {params['destino']}")
                print(f"     Data: {busca['timestamp']}")
                print(f"     ID: {busca['id']}")
    else:
        print(f"\n❌ Erro: {response.status_code}")


def exemplo_health_check():
    """Exemplo de verificação de status da API"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Health Check")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/health")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Status: {result['status']}")
        print(f"  Timestamp: {result['timestamp']}")
        print(f"\nProvedores configurados:")

        for provider in result['providers']:
            status = "✅ Ativo" if provider['available'] else "❌ Inativo"
            print(f"  - {provider['name']}: {status} (Priority: {provider['priority']})")
    else:
        print(f"\n❌ Erro: {response.status_code}")


def exemplo_info_api():
    """Exemplo de obtenção de informações da API"""
    print("=" * 60)
    print("API Flight Crawler v2.0 - Demonstração")
    print("=" * 60)

    response = requests.get(BASE_URL)

    if response.status_code == 200:
        result = response.json()
        print(f"\nAPI: {result['api']}")
        print(f"Versão: {result['version']}")
        print(f"Descrição: {result['description']}")
        print(f"\nProvedores disponíveis: {', '.join(result['providers_configured'])}")
        print(f"Total de provedores: {result['total_providers']}")

        print(f"\nEndpoints disponíveis:")
        for endpoint, desc in result['endpoints'].items():
            print(f"  {endpoint}: {desc}")
    else:
        print(f"\n❌ API não está respondendo")
        print(f"Certifique-se de que o servidor está rodando em {BASE_URL}")
        return False

    return True


def exemplo_busca_internacional():
    """Exemplo de busca internacional"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Busca Internacional")
    print("=" * 60)

    data_ida = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    data_volta = (datetime.now() + timedelta(days=74)).strftime('%Y-%m-%d')

    payload = {
        "origem": "GRU",  # São Paulo
        "destino": "JFK",  # Nova York
        "data_ida": data_ida,
        "data_volta": data_volta,
        "passageiros": 1,
        "criancas": 0,
        "classe": "BUSINESS",
        "moeda": "USD"
    }

    print(f"\nBuscando voos internacionais:")
    print(f"  {payload['origem']} → {payload['destino']}")
    print(f"  Classe: {payload['classe']}")
    print(f"  Moeda: {payload['moeda']}")

    response = requests.post(f"{BASE_URL}/consulta", json=payload)

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ {result['total_resultados']} voos encontrados!")

        if result['voos']:
            voo = result['voos'][0]
            print(f"\nMelhor opção:")
            print(f"  Companhia: {voo['airline']}")
            print(f"  Preço: {voo['currency']} {voo['price']:.2f}")
            print(f"  Duração: {voo['duration_formatted']}")
    else:
        print(f"\n❌ Erro: {response.status_code}")
        print(response.json())


def main():
    """Função principal que executa todos os exemplos"""
    try:
        # Verifica se a API está rodando
        if not exemplo_info_api():
            print("\n⚠️  Inicie a API primeiro com: python app.py")
            return

        # Executa os exemplos
        search_id = exemplo_busca_simples()

        if search_id:
            exemplo_recuperar_busca(search_id)

        exemplo_historico()
        exemplo_health_check()
        exemplo_busca_internacional()

        print("\n" + "=" * 60)
        print("✅ Demonstração concluída!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API")
        print("Certifique-se de que o servidor está rodando:")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")


if __name__ == "__main__":
    main()

