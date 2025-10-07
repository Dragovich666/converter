# Flight Crawler API

API RESTful para buscar passagens aéreas mais baratas com base em critérios de pesquisa.

## Descrição

Esta API simula um crawler que busca passagens aéreas com base em:
- Data inicial (ida)
- Data final (volta)
- Quantidade de passageiros
- Se há crianças
- Idade das crianças

Os dados são retornados em formato JSON e armazenados temporariamente em um banco de dados em memória.

## Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip

### Configuração

1. Clone o repositório:
```bash
git clone https://github.com/Dragovich666/converter.git
cd converter
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints

### 1. GET `/`
Retorna informações sobre a API e seus endpoints disponíveis.

**Resposta:**
```json
{
  "api": "Flight Crawler API",
  "versao": "1.0",
  "endpoints": { ... }
}
```

### 2. POST `/consulta`
Realiza uma busca de passagens aéreas.

**Corpo da requisição (JSON):**
```json
{
  "data_inicial": "2024-01-15",
  "data_final": "2024-01-22",
  "passageiros": 2,
  "tem_crianca": true,
  "idade_crianca": 8
}
```

**Parâmetros:**
- `data_inicial` (obrigatório): Data de ida no formato YYYY-MM-DD
- `data_final` (obrigatório): Data de volta no formato YYYY-MM-DD
- `passageiros` (obrigatório): Quantidade de passageiros (número inteiro > 0)
- `tem_crianca` (opcional): Se há crianças na viagem (boolean, padrão: false)
- `idade_crianca` (opcional): Idade da criança (número inteiro entre 0 e 12)

**Resposta de sucesso (200):**
```json
{
  "sucesso": true,
  "search_id": "uuid-da-busca",
  "parametros": {
    "data_inicial": "2024-01-15",
    "data_final": "2024-01-22",
    "passageiros": 2,
    "tem_crianca": true,
    "idade_crianca": 8
  },
  "total_resultados": 7,
  "voos": [
    {
      "id": "uuid-do-voo",
      "companhia": "GOL",
      "origem": {
        "codigo": "GRU",
        "nome": "São Paulo - Guarulhos"
      },
      "destino": {
        "codigo": "SSA",
        "nome": "Salvador"
      },
      "data_ida": "2024-01-15",
      "data_volta": "2024-01-22",
      "horario_ida": "08:30",
      "horario_volta": "17:00",
      "passageiros": 2,
      "tem_crianca": true,
      "idade_crianca": 8,
      "preco_por_adulto": 450.00,
      "preco_por_crianca": 382.50,
      "preco_total": 832.50,
      "moeda": "BRL",
      "disponivel": true,
      "escalas": 0,
      "duracao_estimada": "2h 30min"
    }
  ]
}
```

### 3. GET `/consulta/<search_id>`
Recupera os resultados de uma busca anterior usando o ID.

**Resposta (200):**
```json
{
  "sucesso": true,
  "search_id": "uuid-da-busca",
  "timestamp": "2024-01-10T10:30:00",
  "parametros": { ... },
  "total_resultados": 7,
  "voos": [ ... ]
}
```

### 4. GET `/historico`
Lista todas as buscas realizadas.

**Resposta (200):**
```json
{
  "sucesso": true,
  "total_buscas": 3,
  "buscas": [
    {
      "id": "uuid-1",
      "data": { ... },
      "timestamp": "2024-01-10T10:30:00"
    }
  ]
}
```

## Exemplos de Uso

### Usando cURL

**Buscar passagens sem crianças:**
```bash
curl -X POST http://localhost:5000/consulta \
  -H "Content-Type: application/json" \
  -d '{
    "data_inicial": "2024-02-01",
    "data_final": "2024-02-10",
    "passageiros": 1,
    "tem_crianca": false
  }'
```

**Buscar passagens com criança:**
```bash
curl -X POST http://localhost:5000/consulta \
  -H "Content-Type: application/json" \
  -d '{
    "data_inicial": "2024-02-01",
    "data_final": "2024-02-10",
    "passageiros": 2,
    "tem_crianca": true,
    "idade_crianca": 5
  }'
```

**Recuperar busca anterior:**
```bash
curl http://localhost:5000/consulta/<search_id>
```

**Ver histórico:**
```bash
curl http://localhost:5000/historico
```

### Usando Python

```python
import requests
import json

# Fazer uma busca
url = "http://localhost:5000/consulta"
dados = {
    "data_inicial": "2024-03-01",
    "data_final": "2024-03-10",
    "passageiros": 2,
    "tem_crianca": True,
    "idade_crianca": 7
}

response = requests.post(url, json=dados)
resultado = response.json()

print(f"Total de voos encontrados: {resultado['total_resultados']}")
print(f"Voo mais barato: R$ {resultado['voos'][0]['preco_total']}")
```

## Características

- ✅ API RESTful com Flask
- ✅ Formato de resposta JSON
- ✅ Validação de parâmetros
- ✅ Banco de dados em memória
- ✅ Ordenação por preço (mais barato primeiro)
- ✅ Desconto para crianças (15%)
- ✅ Simulação de múltiplas companhias aéreas
- ✅ Histórico de buscas
- ✅ Recuperação de buscas anteriores
- ✅ CORS habilitado

## Estrutura do Projeto

```
converter/
├── app.py              # Aplicação principal da API
├── requirements.txt    # Dependências do projeto
└── README.md          # Documentação
```

## Tecnologias Utilizadas

- **Flask**: Framework web para Python
- **Flask-CORS**: Suporte a CORS (Cross-Origin Resource Sharing)

## Observações

- Esta é uma implementação de demonstração que gera dados fictícios
- Os dados são armazenados em memória e serão perdidos ao reiniciar a aplicação
- Para produção, seria necessário integrar com APIs reais de companhias aéreas
- Para produção, utilize um banco de dados persistente (PostgreSQL, MongoDB, etc.)

## Licença

Este projeto é de código aberto e está disponível para uso educacional.