"""
Exemplo de uso da Flight Crawler API
"""
import requests
import json

# URL base da API
BASE_URL = "http://localhost:5000"


def buscar_passagens(data_inicial, data_final, passageiros, tem_crianca=False, idade_crianca=None):
    """Busca passagens aéreas"""
    url = f"{BASE_URL}/consulta"
    
    dados = {
        "data_inicial": data_inicial,
        "data_final": data_final,
        "passageiros": passageiros,
        "tem_crianca": tem_crianca
    }
    
    if idade_crianca is not None:
        dados["idade_crianca"] = idade_crianca
    
    response = requests.post(url, json=dados)
    return response.json()


def recuperar_busca(search_id):
    """Recupera uma busca anterior"""
    url = f"{BASE_URL}/consulta/{search_id}"
    response = requests.get(url)
    return response.json()


def ver_historico():
    """Lista o histórico de buscas"""
    url = f"{BASE_URL}/historico"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    print("=" * 60)
    print("Exemplo 1: Buscar passagens sem crianças")
    print("=" * 60)
    
    resultado = buscar_passagens(
        data_inicial="2024-06-01",
        data_final="2024-06-10",
        passageiros=2
    )
    
    print(f"Total de voos encontrados: {resultado['total_resultados']}")
    print(f"Search ID: {resultado['search_id']}")
    print("\nVoo mais barato:")
    voo_barato = resultado['voos'][0]
    print(f"  Companhia: {voo_barato['companhia']}")
    print(f"  Origem: {voo_barato['origem']['nome']}")
    print(f"  Destino: {voo_barato['destino']['nome']}")
    print(f"  Preço: R$ {voo_barato['preco_total']}")
    
    search_id = resultado['search_id']
    
    print("\n" + "=" * 60)
    print("Exemplo 2: Buscar passagens com crianças")
    print("=" * 60)
    
    resultado2 = buscar_passagens(
        data_inicial="2024-07-15",
        data_final="2024-07-25",
        passageiros=3,
        tem_crianca=True,
        idade_crianca=8
    )
    
    print(f"Total de voos encontrados: {resultado2['total_resultados']}")
    print("\nTop 3 voos mais baratos:")
    for i, voo in enumerate(resultado2['voos'][:3], 1):
        print(f"\n{i}. {voo['companhia']}")
        print(f"   {voo['origem']['codigo']} → {voo['destino']['codigo']}")
        print(f"   Preço por adulto: R$ {voo['preco_por_adulto']}")
        print(f"   Preço por criança: R$ {voo['preco_por_crianca']}")
        print(f"   Preço total: R$ {voo['preco_total']}")
    
    print("\n" + "=" * 60)
    print("Exemplo 3: Recuperar busca anterior")
    print("=" * 60)
    
    recuperado = recuperar_busca(search_id)
    print(f"Busca recuperada com sucesso!")
    print(f"Timestamp: {recuperado['timestamp']}")
    print(f"Total de resultados: {recuperado['total_resultados']}")
    
    print("\n" + "=" * 60)
    print("Exemplo 4: Ver histórico de buscas")
    print("=" * 60)
    
    historico = ver_historico()
    print(f"Total de buscas no histórico: {historico['total_buscas']}")
    print("\nÚltimas buscas:")
    for busca in historico['buscas'][-3:]:
        print(f"\n  ID: {busca['id']}")
        print(f"  Data: {busca['timestamp']}")
        print(f"  Parâmetros: {busca['data']}")
