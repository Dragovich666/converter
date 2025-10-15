# 🚀 Flight Crawler API v2.0 - Guia de Início Rápido

## ✅ O que foi implementado

A aplicação foi **completamente refatorada** seguindo **padrões de mercado de alto nível**:

### 📐 Princípios SOLID Aplicados
- ✅ **S** - Single Responsibility: Cada classe tem uma única responsabilidade
- ✅ **O** - Open/Closed: Aberto para extensão, fechado para modificação
- ✅ **L** - Liskov Substitution: Provedores são intercambiáveis
- ✅ **I** - Interface Segregation: Interfaces enxutas e específicas
- ✅ **D** - Dependency Inversion: Dependências de abstrações, não implementações

### 🎨 Padrões de Projeto
- ✅ **Strategy Pattern**: Provedores como estratégias intercambiáveis
- ✅ **Facade Pattern**: Interface simplificada para busca complexa
- ✅ **Repository Pattern**: Abstração da camada de dados
- ✅ **Dependency Injection**: Inversão de controle

### 🌐 Integração com APIs Reais
- ✅ **Kiwi.com (Tequila API)**: API gratuita com dados reais de voos
- ✅ **Amadeus API**: API profissional com dados oficiais
- ✅ Busca paralela em múltiplos provedores
- ✅ Agregação e deduplicação de resultados

## 🚦 Como Usar

### 1️⃣ Obter API Key Gratuita (Kiwi.com)

**RECOMENDADO**: Use a API Kiwi.com que é totalmente gratuita e sem limites rigorosos.

1. Acesse: https://tequila.kiwi.com/portal/login
2. Crie uma conta gratuita
3. Acesse o dashboard e copie sua API key
4. Edite o arquivo `.env` e cole sua chave:

```env
KIWI_API_KEY=sua-api-key-aqui
```

### 2️⃣ Iniciar a Aplicação

```bash
python app.py
```

Você verá:
```
============================================================
Iniciando Flight Crawler API v2.0
Arquitetura: SOLID + Design Patterns
Provedores configurados: 1/2
Acesse http://0.0.0.0:5000
============================================================
```

### 3️⃣ Testar a API

**Verificar status:**
```bash
curl http://localhost:5000/health
```

**Buscar voos (DADOS REAIS):**
```bash
curl -X POST http://localhost:5000/consulta ^
  -H "Content-Type: application/json" ^
  -d "{\"origem\":\"GRU\",\"destino\":\"GIG\",\"data_ida\":\"2025-11-15\",\"data_volta\":\"2025-11-22\",\"passageiros\":2,\"classe\":\"ECONOMY\",\"moeda\":\"BRL\"}"
```

### 4️⃣ Usar o Script de Exemplo

Execute o script de demonstração:
```bash
python exemplo_uso.py
```

Este script demonstra todos os endpoints e funcionalidades.

## 📂 Arquitetura do Projeto

```
converter/
├── app.py                    # Aplicação Flask (Controller)
├── config.py                 # Configurações centralizadas
├── interfaces.py             # Contratos e modelos de domínio
├── provider_kiwi.py          # Provedor Kiwi.com (dados reais)
├── provider_amadeus.py       # Provedor Amadeus (dados reais)
├── flight_service.py         # Orquestrador de buscas (Service)
├── repository.py             # Camada de persistência (Repository)
├── .env                      # Variáveis de ambiente (configure aqui)
├── requirements.txt          # Dependências Python
└── exemplo_uso.py            # Script de demonstração
```

## 🎯 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Status e provedores disponíveis |
| POST | `/consulta` | **Buscar voos reais** |
| GET | `/consulta/<id>` | Recuperar busca anterior |
| GET | `/historico` | Listar todas as buscas |
| GET | `/stats` | Estatísticas de uso |

## 💡 Exemplo de Resposta Real

```json
{
  "sucesso": true,
  "search_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "total_resultados": 15,
  "voos": [
    {
      "id": "real-flight-id",
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
      "departure_datetime": "2025-11-15T08:00:00",
      "arrival_datetime": "2025-11-15T09:15:00",
      "price": 450.00,
      "currency": "BRL",
      "stops": 0,
      "duration_formatted": "1h 15min",
      "available_seats": 9,
      "booking_url": "https://kiwi.com/booking/...",
      "cabin_class": "ECONOMY",
      "baggage_included": true
    }
  ]
}
```

## 🔧 Adicionar Mais Provedores

Para adicionar um novo provedor, crie um arquivo `provider_novo.py`:

```python
from interfaces import IFlightProvider, FlightSearchParams, Flight

class NovoProvider(IFlightProvider):
    def search_flights(self, params: FlightSearchParams):
        # Implementar integração com API
        pass
    
    def get_provider_name(self):
        return "Novo Provider"
    
    def is_available(self):
        return True
    
    def get_priority(self):
        return 3

# Em app.py, adicione:
providers.append(NovoProvider())
```

## 📊 Comparação: Antes vs Depois

| Característica | Versão Antiga | Nova Versão |
|----------------|---------------|-------------|
| Dados | 🔴 Fictícios | ✅ APIs Reais |
| Arquitetura | 🔴 Monolítica | ✅ SOLID + Patterns |
| Provedores | 🔴 Nenhum | ✅ 2 (extensível) |
| Busca | 🔴 Sequencial | ✅ Paralela |
| Manutenibilidade | 🔴 Baixa | ✅ Alta |
| Testabilidade | 🔴 Difícil | ✅ Fácil (interfaces) |
| Extensibilidade | 🔴 Complexa | ✅ Plug & Play |

## ⚠️ Importante

- **Configure a API key no arquivo `.env`** antes de usar
- Sem API key configurada, a aplicação não retornará voos reais
- A API Kiwi.com é gratuita e recomendada para testes
- A API Amadeus tem plano teste gratuito com limites

## 📚 Documentação Completa

Veja `README_ARCHITECTURE.md` para documentação técnica detalhada sobre a arquitetura, padrões e princípios aplicados.

## 🆘 Suporte

Se tiver problemas:
1. Verifique se o arquivo `.env` está configurado
2. Confirme que tem uma API key válida da Kiwi.com
3. Teste o endpoint `/health` para ver status dos provedores
4. Verifique os logs da aplicação para detalhes de erros

---

**Desenvolvido com princípios SOLID e padrões de projeto de alto nível** 🚀

