# Flight Crawler API v2.0 - Documentação

## 🚀 Arquitetura Profissional com Dados Reais

Esta aplicação foi completamente refatorada seguindo **princípios SOLID** e **padrões de projeto de alto nível**, integrando com APIs reais de companhias aéreas e agregadores de voos.

## 📋 Princípios SOLID Aplicados

### 1. **Single Responsibility Principle (SRP)**
- `config.py`: Responsável apenas por configurações
- `interfaces.py`: Define contratos e modelos de domínio
- `repository.py`: Gerencia apenas persistência de dados
- `flight_service.py`: Orquestra buscas entre provedores
- Cada provedor (`provider_*.py`): Integração específica com uma API

### 2. **Open/Closed Principle (OCP)**
- Sistema aberto para extensão: novos provedores podem ser adicionados sem modificar código existente
- Fechado para modificação: a lógica core não precisa ser alterada

### 3. **Liskov Substitution Principle (LSP)**
- Todos os provedores implementam `IFlightProvider`
- Qualquer provedor pode substituir outro sem quebrar o sistema

### 4. **Interface Segregation Principle (ISP)**
- Interface `IFlightProvider` contém apenas métodos essenciais
- Clientes não dependem de métodos que não utilizam

### 5. **Dependency Inversion Principle (DIP)**
- `FlightSearchService` depende de abstrações (`IFlightProvider`), não de implementações concretas
- Inversão de controle através de injeção de dependências

## 🎨 Padrões de Projeto Implementados

### 1. **Strategy Pattern**
- Cada provedor de voos é uma estratégia diferente
- Provedores são intercambiáveis em runtime

### 2. **Facade Pattern**
- `FlightSearchService` fornece interface simplificada para busca em múltiplos provedores

### 3. **Repository Pattern**
- `SearchRepository` abstrai a camada de persistência
- Facilita migração para banco de dados real no futuro

### 4. **Dependency Injection**
- Serviços recebem dependências via construtor
- Facilita testes e manutenção

## 🌐 Provedores de Dados Reais

### 1. **Kiwi.com (Tequila API)** ✅ Recomendado
- **Status**: API gratuita com dados reais
- **Registro**: https://tequila.kiwi.com/portal/login
- **Cobertura**: Mundial, múltiplas companhias
- **Prioridade**: Alta (Priority 1)

### 2. **Amadeus API** ✅ Profissional
- **Status**: Plano gratuito disponível (teste)
- **Registro**: https://developers.amadeus.com/
- **Cobertura**: Global, dados oficiais
- **Prioridade**: Média (Priority 2)

## 📁 Estrutura do Projeto

```
converter/
├── app.py                   # Aplicação Flask principal
├── config.py                # Configurações centralizadas
├── interfaces.py            # Interfaces e modelos de domínio
├── provider_kiwi.py         # Provedor Kiwi.com (dados reais)
├── provider_amadeus.py      # Provedor Amadeus (dados reais)
├── flight_service.py        # Serviço orquestrador (Facade)
├── repository.py            # Repositório de dados
├── requirements.txt         # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
└── README_ARCHITECTURE.md   # Esta documentação
```

## 🔧 Configuração Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
```bash
# Copie o arquivo exemplo
copy .env.example .env

# Edite .env e adicione suas API keys
```

### 3. Obter API Keys Gratuitas

#### Kiwi.com (Recomendado - Gratuito)
1. Acesse: https://tequila.kiwi.com/portal/login
2. Crie uma conta
3. Gere sua API key gratuita
4. Adicione em `.env`: `KIWI_API_KEY=sua-chave-aqui`

#### Amadeus (Opcional - Plano Teste Gratuito)
1. Acesse: https://developers.amadeus.com/
2. Crie uma conta de desenvolvedor
3. Crie um app para obter API Key e Secret
4. Adicione em `.env`:
   - `AMADEUS_API_KEY=sua-chave-aqui`
   - `AMADEUS_API_SECRET=seu-secret-aqui`

### 4. Executar a Aplicação
```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

## 📡 Endpoints da API

### 1. **GET /** - Informações da API
```bash
curl http://localhost:5000/
```

**Resposta:**
```json
{
  "api": "Flight Crawler API",
  "version": "2.0",
  "providers_configured": ["Kiwi.com", "Amadeus"],
  "endpoints": { ... }
}
```

### 2. **POST /consulta** - Buscar Voos (DADOS REAIS)
```bash
curl -X POST http://localhost:5000/consulta \
  -H "Content-Type: application/json" \
  -d '{
    "origem": "GRU",
    "destino": "GIG",
    "data_ida": "2025-11-01",
    "data_volta": "2025-11-10",
    "passageiros": 2,
    "criancas": 0,
    "classe": "ECONOMY",
    "moeda": "BRL"
  }'
```

**Resposta:**
```json
{
  "sucesso": true,
  "search_id": "uuid-da-busca",
  "total_resultados": 15,
  "voos": [
    {
      "id": "flight-id",
      "provider": "Kiwi.com",
      "airline": "GOL",
      "origin": {
        "code": "GRU",
        "name": "São Paulo",
        "city": "São Paulo",
        "country": "Brazil"
      },
      "destination": {
        "code": "GIG",
        "name": "Rio de Janeiro",
        "city": "Rio de Janeiro",
        "country": "Brazil"
      },
      "departure_datetime": "2025-11-01T08:00:00",
      "arrival_datetime": "2025-11-01T09:15:00",
      "price": 450.00,
      "currency": "BRL",
      "stops": 0,
      "duration_minutes": 75,
      "duration_formatted": "1h 15min",
      "available_seats": 9,
      "booking_url": "https://...",
      "cabin_class": "ECONOMY"
    }
  ]
}
```

### 3. **GET /consulta/<search_id>** - Recuperar Busca
```bash
curl http://localhost:5000/consulta/uuid-da-busca
```

### 4. **GET /historico** - Histórico de Buscas
```bash
curl http://localhost:5000/historico
```

### 5. **GET /stats** - Estatísticas
```bash
curl http://localhost:5000/stats
```

### 6. **GET /health** - Health Check
```bash
curl http://localhost:5000/health
```

## 🎯 Funcionalidades Implementadas

### ✅ Busca em Múltiplos Provedores
- Busca paralela em todos os provedores configurados
- Agregação automática de resultados
- Remoção de duplicatas

### ✅ Dados Reais
- Integração com APIs reais (Kiwi.com, Amadeus)
- Preços atualizados
- Disponibilidade real de assentos
- Links diretos para reserva

### ✅ Validações Robustas
- Validação de códigos IATA
- Validação de datas
- Validação de classes de cabine
- Mensagens de erro claras

### ✅ Performance
- Buscas paralelas usando ThreadPoolExecutor
- Timeout configurável
- Retry automático

### ✅ Logging Profissional
- Logs estruturados
- Rastreamento de requisições
- Detecção de erros

## 🔄 Exemplo de Fluxo

```
1. Cliente → POST /consulta
2. App valida parâmetros
3. FlightSearchService busca em paralelo:
   ├── KiwiProvider → API Kiwi.com
   └── AmadeusProvider → API Amadeus
4. Resultados são agregados e ordenados
5. SearchRepository salva busca e resultados
6. Resposta JSON é retornada ao cliente
```

## 🚀 Próximos Passos (Extensões Possíveis)

### Adicionar Novos Provedores
```python
# Criar novo arquivo: provider_skyscanner.py
class SkyscannerProvider(IFlightProvider):
    def search_flights(self, params):
        # Implementação...
        pass
    
    def get_provider_name(self):
        return 'Skyscanner'
    
    # ... outros métodos

# Em app.py, adicionar:
providers.append(SkyscannerProvider())
```

### Adicionar Cache Redis
```python
# Instalar: pip install redis
from redis import Redis

class CachedFlightService:
    def __init__(self, flight_service, redis_client):
        self.flight_service = flight_service
        self.redis = redis_client
    
    def search_flights(self, params):
        cache_key = self._generate_cache_key(params)
        cached = self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        results = self.flight_service.search_flights(params)
        self.redis.setex(cache_key, 3600, json.dumps(results))
        return results
```

### Adicionar Banco de Dados
```python
# Instalar: pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Substituir SearchRepository por versão SQL
class SQLSearchRepository(SearchRepository):
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        # ... implementação
```

## 📊 Diferenças vs Versão Anterior

| Aspecto | Versão Antiga | Versão Nova |
|---------|---------------|-------------|
| Dados | Fictícios/Mock | APIs Reais |
| Arquitetura | Monolítica | SOLID + Patterns |
| Extensibilidade | Difícil | Fácil (plug & play) |
| Testabilidade | Baixa | Alta (interfaces) |
| Performance | Sequencial | Paralela |
| Manutenção | Complexa | Simples (separação) |
| Provedores | 0 | 2+ (extensível) |

## 🎓 Conceitos Aplicados

- ✅ **SOLID Principles**
- ✅ **Design Patterns** (Strategy, Facade, Repository, DI)
- ✅ **Clean Architecture**
- ✅ **RESTful API Design**
- ✅ **Error Handling**
- ✅ **Logging**
- ✅ **Async/Parallel Processing**
- ✅ **Data Validation**
- ✅ **API Integration**
- ✅ **Configuration Management**

## 📝 Licença

MIT License - Sinta-se livre para usar e modificar.

