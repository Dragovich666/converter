# Guia Rápido - Flight Crawler API

## Início Rápido

### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/Dragovich666/converter.git
cd converter

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

### 2. Primeiro Uso

A API estará disponível em `http://localhost:5000`

**Exemplo 1: Buscar passagens para 1 pessoa (sem crianças)**

```bash
curl -X POST http://localhost:5000/consulta \
  -H "Content-Type: application/json" \
  -d '{
    "data_inicial": "2024-12-15",
    "data_final": "2024-12-22",
    "passageiros": 1,
    "tem_crianca": false
  }'
```

**Exemplo 2: Buscar passagens para família com criança**

```bash
curl -X POST http://localhost:5000/consulta \
  -H "Content-Type: application/json" \
  -d '{
    "data_inicial": "2024-12-15",
    "data_final": "2024-12-22",
    "passageiros": 3,
    "tem_crianca": true,
    "idade_crianca": 8
  }'
```

### 3. Testando com Python

Execute o script de exemplo incluído:

```bash
pip install requests  # Se ainda não tiver instalado
python exemplo_uso.py
```

### 4. Principais Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Informações da API |
| `/consulta` | POST | Buscar passagens |
| `/consulta/<id>` | GET | Recuperar busca |
| `/historico` | GET | Ver histórico |

### 5. Estrutura da Resposta

```json
{
  "sucesso": true,
  "search_id": "uuid-da-busca",
  "total_resultados": 7,
  "voos": [
    {
      "companhia": "GOL",
      "origem": {"codigo": "GRU", "nome": "São Paulo - Guarulhos"},
      "destino": {"codigo": "SSA", "nome": "Salvador"},
      "preco_total": 450.00,
      ...
    }
  ]
}
```

### 6. Recursos

- ✅ Ordenação automática por preço (mais barato primeiro)
- ✅ Desconto de 15% para crianças
- ✅ Validação completa de dados
- ✅ Armazenamento em memória
- ✅ Histórico de buscas
- ✅ Formato JSON

## Documentação Completa

Para documentação detalhada, consulte o [README.md](README.md)
