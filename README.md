# AquaRural

AquaRural e uma plataforma open-source para gestao de sistemas comunitarios de abastecimento de agua em areas rurais. O projeto agora inclui a fundacao de um backend FastAPI pronto para evoluir com autenticacao, regras operacionais e futuras interfaces web/mobile.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Pydantic Settings
- Uvicorn
- uv
- Docker e Docker Compose
- Pytest

## Estrutura

```text
app/
  api/
  core/
  db/
  models/
  repositories/
  schemas/
  services/
  main.py
alembic/
tests/
```

## Setup local

1. Copie `.env.example` para `.env`.
2. Ajuste as variaveis de ambiente conforme necessario.
3. Instale o `uv`.
4. Rode `uv sync --dev`.
5. Aplique as migracoes com `uv run alembic upgrade head`.
6. Inicie a API com `uv run uvicorn app.main:app --reload`.

A API ficara disponivel em `http://localhost:8000` e o health check em `http://localhost:8000/api/v1/health`.

## Docker

1. Copie `.env.example` para `.env`.
2. Rode `docker compose up --build`.
3. Em outro terminal, aplique as migracoes com `docker compose exec api uv run alembic upgrade head`.

## Testes

Execute os testes com:

```bash
uv run pytest
```

## Modelagem inicial

A fundacao cobre as entidades principais do dominio:

- customers
- locations
- consumer_units
- meters
- meter_installations
- reading_cycles
- meter_readings
- tariff_plans
- tariff_tiers
- invoices
- invoice_items
- payments
- meter_events
- users
- audit_logs

## Regras estruturais ja refletidas

- `consumer_units` e a entidade central.
- Leituras mensais sao unicas por unidade consumidora e ciclo de leitura.
- Tarifas possuem vigencia.
- Pagamentos aceitam liquidacao parcial em faturas.
- Instalacoes, eventos e logs preservam historico sem depender de sobrescrita destrutiva.

## Proximos passos recomendados

- Implementar CRUD inicial para customers, locations e consumer_units.
- Adicionar casos de uso para leitura mensal e fechamento de fatura.
- Introduzir autenticacao e autorizacao por perfis.
- Padronizar tratamento de erros e observabilidade.
- Configurar CI para testes e migracoes.
