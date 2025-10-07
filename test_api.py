"""
Testes básicos para a Flight Crawler API
"""
import sys
import requests
import json


def test_api():
    """Executa testes básicos na API"""
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("EXECUTANDO TESTES DA API")
    print("=" * 60)
    
    # Teste 1: Verificar se API está online
    print("\n[Teste 1] Verificando se a API está online...")
    try:
        response = requests.get(base_url)
        assert response.status_code == 200, "API não está respondendo"
        data = response.json()
        assert data['api'] == 'Flight Crawler API', "Resposta inesperada da API"
        print("✓ API está online e respondendo corretamente")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    # Teste 2: Busca simples sem crianças
    print("\n[Teste 2] Testando busca sem crianças...")
    try:
        payload = {
            "data_inicial": "2024-03-01",
            "data_final": "2024-03-10",
            "passageiros": 1,
            "tem_crianca": False
        }
        response = requests.post(f"{base_url}/consulta", json=payload)
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data['sucesso'] == True, "Busca não teve sucesso"
        assert 'search_id' in data, "search_id não retornado"
        assert data['total_resultados'] > 0, "Nenhum resultado encontrado"
        assert len(data['voos']) > 0, "Lista de voos vazia"
        search_id = data['search_id']
        print(f"✓ Busca realizada com sucesso (ID: {search_id[:8]}...)")
        print(f"  Total de resultados: {data['total_resultados']}")
        print(f"  Voo mais barato: R$ {data['voos'][0]['preco_total']}")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    # Teste 3: Busca com crianças
    print("\n[Teste 3] Testando busca com crianças...")
    try:
        payload = {
            "data_inicial": "2024-06-15",
            "data_final": "2024-06-25",
            "passageiros": 2,
            "tem_crianca": True,
            "idade_crianca": 7
        }
        response = requests.post(f"{base_url}/consulta", json=payload)
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data['sucesso'] == True, "Busca não teve sucesso"
        voo = data['voos'][0]
        assert voo['tem_crianca'] == True, "Criança não registrada"
        assert voo['idade_crianca'] == 7, "Idade incorreta"
        assert voo['preco_por_crianca'] is not None, "Preço de criança não calculado"
        print(f"✓ Busca com criança realizada com sucesso")
        print(f"  Preço por adulto: R$ {voo['preco_por_adulto']}")
        print(f"  Preço por criança: R$ {voo['preco_por_crianca']} (desconto aplicado)")
        print(f"  Preço total: R$ {voo['preco_total']}")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    # Teste 4: Recuperar busca por ID
    print("\n[Teste 4] Testando recuperação de busca por ID...")
    try:
        response = requests.get(f"{base_url}/consulta/{search_id}")
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data['search_id'] == search_id, "ID não corresponde"
        assert 'timestamp' in data, "Timestamp não presente"
        print(f"✓ Busca recuperada com sucesso")
        print(f"  Timestamp: {data['timestamp']}")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    # Teste 5: Histórico
    print("\n[Teste 5] Testando histórico de buscas...")
    try:
        response = requests.get(f"{base_url}/historico")
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data['sucesso'] == True, "Requisição falhou"
        assert data['total_buscas'] >= 2, "Histórico não contém buscas"
        print(f"✓ Histórico recuperado com sucesso")
        print(f"  Total de buscas: {data['total_buscas']}")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    # Teste 6: Validação de erros
    print("\n[Teste 6] Testando validação de erros...")
    try:
        # Campos faltando
        response = requests.post(f"{base_url}/consulta", json={"passageiros": 1})
        assert response.status_code == 400, "Deveria retornar erro 400"
        
        # Data inválida
        response = requests.post(f"{base_url}/consulta", json={
            "data_inicial": "01/01/2024",
            "data_final": "2024-01-10",
            "passageiros": 1
        })
        assert response.status_code == 400, "Deveria retornar erro 400"
        
        # Passageiros inválido
        response = requests.post(f"{base_url}/consulta", json={
            "data_inicial": "2024-01-01",
            "data_final": "2024-01-10",
            "passageiros": 0
        })
        assert response.status_code == 400, "Deveria retornar erro 400"
        
        print("✓ Validações de erro funcionando corretamente")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    # Teste 7: Ordenação por preço
    print("\n[Teste 7] Testando ordenação por preço...")
    try:
        payload = {
            "data_inicial": "2024-08-01",
            "data_final": "2024-08-10",
            "passageiros": 1,
            "tem_crianca": False
        }
        response = requests.post(f"{base_url}/consulta", json=payload)
        data = response.json()
        voos = data['voos']
        precos = [voo['preco_total'] for voo in voos]
        assert precos == sorted(precos), "Voos não estão ordenados por preço"
        print("✓ Voos ordenados corretamente (do mais barato ao mais caro)")
        print(f"  Preço mais barato: R$ {precos[0]}")
        print(f"  Preço mais caro: R$ {precos[-1]}")
    except Exception as e:
        print(f"✗ Falhou: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("TODOS OS TESTES PASSARAM COM SUCESSO! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    print("Certifique-se de que a API está rodando em http://localhost:5000")
    print("Execute: python app.py")
    print()
    input("Pressione ENTER para continuar com os testes...")
    
    try:
        success = test_api()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTestes interrompidos pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro inesperado: {e}")
        sys.exit(1)
