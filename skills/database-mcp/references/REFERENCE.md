# Database MCP — Referências de Consulta Rápida

Este arquivo consolida referências de todos os 4 módulos originais (discovery-10, discovery-11, discovery-12, discovery-13) em um único lugar.

---

## 📋 Documento de configuração do projeto (LEITURA OBRIGATÓRIA)

Antes de executar **qualquer módulo**, ler `discovery-database.yml`.

| Chave                       | Uso                               | Exemplo                             |
| --------------------------- | --------------------------------- | ----------------------------------- |
| `database.engine`           | Selecionar bloco SQL correto      | `postgresql` \| `sqlserver`         |
| `database.schema_principal` | Schema padrão em todas as queries | `public` \| `dbo`                   |
| `database.mcp_server`       | Servidor MCP para executar SQL    | `postgres-mcp`                      |
| `database.schema_quartz`    | Schema de jobs (se Quartz usado)  | `public`                            |
| `paths.legacy`              | Caminho do código legado          | `/src/legacy`                       |
| `paths.sps_local`           | Pasta local de `.sql` das SPs     | `/database/sps`                     |
| `paths.discovery`           | Pasta de saída de artefatos       | `/discovery`                        |
| `stack.backend.framework`   | Framework para adaptar busca rg   | `spring-boot` \| `.net` \| `django` |

---

## Módulo 1 — Snapshot: Documentos para ler antes

| Arquivo                              | Quando ler                                | Buscar por             |
| ------------------------------------ | ----------------------------------------- | ---------------------- |
| `DADOS-05-MAPA-DADOS.md`             | Antes de Snapshot — verificar duplicações | Nome da tabela-alvo    |
| `SNAP-MAPA-DADOS-*.md`               | Snapshot anterior como linha de base      | Seção da tabela        |
| `DISC-98-FONTES-E-CONFIABILIDADE.md` | Confirmar quais fontes estão disponíveis  | Seção "Banco de dados" |
| `DISC-00-INDICE.md`                  | Localizar pendências abertas              | Buscar `[PEN]`         |

### Localizador rápido (Snapshot)

```powershell
# Verificar se tabela já está em DADOS-05:
Select-String -Path "discovery\DADOS-05-MAPA-DADOS.md" -Pattern "nome_tabela"

# Buscar scripts SQL do legado:
Select-String -Path "discovery\arquivos-legado.txt" -Pattern "\.sql"
```

### Saída do Snapshot

| Arquivo                                   | Atualizar quando                  |
| ----------------------------------------- | --------------------------------- |
| `discovery/DADOS-05-MAPA-DADOS.md`        | Nova tabela ou correção de coluna |
| `discovery/SNAP-MAPA-DADOS-YYYY-MM-DD.md` | Snapshot formal solicitado        |

---

## Módulo 2 — Status Map: Documentos para ler antes

| Arquivo                                   | Quando ler                                      | Buscar por                     |
| ----------------------------------------- | ----------------------------------------------- | ------------------------------ |
| `DADOS-06-STATUS-E-TRANSICOES.md`         | Sempre — verificar o que já está mapeado        | Nome da entidade/tabela-alvo   |
| `DADOS-09-MAPA-FLUXO-TABELAS.md`          | Correlacionar status com fluxos documentados    | Nome do fluxo ou tabela        |
| `SNAP-STATUS-*.md`                        | Snapshot anterior como linha de base            | Seção da entidade-alvo         |
| `FLUXO-F03-PROCESSO-TRAMITACAO-STATUS.md` | Entender ciclo de vida e referenciar transições | Seções "Status" e "Transições" |
| `DISC-00-INDICE.md`                       | Localizar pendências abertas de status          | Buscar `[PEN]` com `status`    |

### Localizador rápido (Status Map)

```powershell
# Verificar status já documentados em DADOS-06:
Select-String -Path "discovery\DADOS-06-STATUS-E-TRANSICOES.md" -Pattern "nome_status_ou_tabela"

# Localizar enums Java no legado:
Select-String -Path "discovery\arquivos-legado.txt" -Pattern "Enum|enum|Status|Situacao"

# Buscar scripts SQL com status:
Select-String -Path "discovery\arquivos-legado.txt" -Pattern "\.sql"
```

### Saída do Status Map

| Arquivo                                     | Atualizar quando                             |
| ------------------------------------------- | -------------------------------------------- |
| `discovery/DADOS-06-STATUS-E-TRANSICOES.md` | Novo status mapeado ou descrição corrigida   |
| `discovery/DADOS-09-MAPA-FLUXO-TABELAS.md`  | Correlação entre status e fluxo identificada |

---

## Módulo 3 — Rotinas: Documentos para ler antes

| Arquivo                                    | Quando ler                              | Buscar por                            |
| ------------------------------------------ | --------------------------------------- | ------------------------------------- |
| `DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | Versão anterior — verificar duplicações | Seção "Resumo" ou nome da SP          |
| `SNAP-DADOS-10-VALIDACAO.md`               | Snapshot anterior — linha de base       | Seções "Divergências" e "Itens [PEN]" |
| `DADOS-05-MAPA-DADOS.md`                   | Correlacionar tabelas afetadas          | Nome da tabela                        |
| `DISC-98-FONTES-E-CONFIABILIDADE.md`       | Confirmar fontes disponíveis            | Seções "Banco" e "Jobs Quartz"        |
| `DISC-00-INDICE.md`                        | Localizar pendências de rotinas         | Buscar `[PEN]` e `D10-*`              |

### Localizador rápido (Rotinas)

```powershell
# Verificar SPs já documentadas em DADOS-10:
Select-String -Path "discovery\DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md" -Pattern "nome_sp_ou_function"

# Buscar chamadas de SP no código legado (ajustar por framework):
# .NET:
rg "EXEC\s+|ExecuteCommand\(|sp_executesql" --type cs "<paths.legado>"

# Java:
rg "\.call\(|execute\(|\bCallableStatement" --type java "<paths.legado>"

# Python:
rg "cursor\.callproc|execute\(|call " --type py "<paths.legado>"

# Listar arquivos .sql no legado:
Get-ChildItem -Path "<paths.legado>" -Recurse -Filter "*.sql"
```

### Saída do Rotinas

| Arquivo                                              | Atualizar quando                         |
| ---------------------------------------------------- | ---------------------------------------- |
| `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | Adição, correção ou regeneração completa |
| `discovery/SNAP-DADOS-10-VALIDACAO.md`               | Snapshot formal solicitado               |

---

## Módulo 4 — SP Deep Dive: Documentos para ler antes

Mesmo que Módulo 3, mais:

| Arquivo               | Quando ler                 | Buscar por                         |
| --------------------- | -------------------------- | ---------------------------------- |
| Qualquer `FLUXO-*.md` | Se SP é crítica para fluxo | Seções "Dados" e "Rastreabilidade" |
| Qualquer `TELA-*.md`  | Se SP é usada na tela      | Seção "Regras de negócio"          |

### Saída do Deep Dive

| Arquivo                                              | Atualizar quando                              |
| ---------------------------------------------------- | --------------------------------------------- |
| `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | Ficha da SP enriquecida com regras e diagrama |

---

## Queries de referência rápida

### PostgreSQL — Listagens básicas

```sql
-- Listar tabelas do schema
SELECT table_name FROM information_schema.tables
WHERE table_schema = '<schema_principal>' AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Listar colunas de uma tabela
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = '<schema_principal>' AND table_name = '<tabela>'
ORDER BY ordinal_position;

-- Listar functions
SELECT proname, pg_get_function_identity_arguments(oid)
FROM pg_proc
WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = '<schema_principal>')
ORDER BY proname;

-- Obter definição de uma function
SELECT pg_get_functiondef(oid)
FROM pg_proc
WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = '<schema_principal>')
  AND proname = '<func_name>';

-- Listar triggers
SELECT tgname, relname
FROM pg_trigger t
JOIN pg_class c ON c.oid = t.tgrelid
WHERE c.relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = '<schema_principal>')
ORDER BY tgname;

-- Listar jobs Quartz
SELECT job_name, job_class_name, trigger_state
FROM public.qrtz_job_details jd
LEFT JOIN public.qrtz_triggers t ON t.job_name = jd.job_name;
```

### SQL Server — Listagens básicas

```sql
-- Listar tabelas do schema
SELECT name FROM sys.tables
WHERE schema_id = SCHEMA_ID('<schema_principal>')
ORDER BY name;

-- Listar colunas de uma tabela
SELECT c.name, t.name, c.is_nullable
FROM sys.columns c
JOIN sys.tables tb ON tb.object_id = c.object_id
JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE tb.schema_id = SCHEMA_ID('<schema_principal>') AND tb.name = '<tabela>'
ORDER BY c.column_id;

-- Listar SPs, functions, triggers
SELECT name, type FROM sys.objects
WHERE schema_id = SCHEMA_ID('<schema_principal>')
  AND type IN ('P', 'FN', 'TR')
ORDER BY name;

-- Obter parâmetros de uma SP
SELECT name, type_name FROM sys.parameters
WHERE object_id = OBJECT_ID('<schema_principal>.<sp_nome>')
ORDER BY parameter_id;

-- Obter definição de uma SP
SELECT OBJECT_DEFINITION(OBJECT_ID('<schema_principal>.<sp_nome>'));

-- Listar comentários estendidos (descrições)
SELECT major_id, minor_id, name, value
FROM sys.extended_properties
WHERE class = 1 AND parent_class = 1
ORDER BY major_id;
```

---

## Totais conhecidos (última execução: 2026-02-19)

| Tipo                          | Quantidade | Observação                                |
| ----------------------------- | ---------- | ----------------------------------------- |
| Tabelas (schema principal)    | ?          | A confirmar por Snapshot                  |
| Functions (schema principal)  | 3          | Todas dashboard — somente leitura         |
| Procedures (schema principal) | 0          | Nenhuma encontrada                        |
| Triggers (schema principal)   | 0          | Nenhum encontrado                         |
| Jobs Quartz (schema public)   | 1          | `EnvioNotificacao` — cron `0 */1 * * * ?` |

---

## Padrões de nomenclatura

### SQL Server — Prefixos convencionais

| Prefixo               | Tipo                   |
| --------------------- | ---------------------- |
| `USP_`, `SP_`, `usp_` | User Stored Procedures |
| `fn_`, `FN_`          | Scalar functions       |
| `tvf_`, `TVF_`        | Table-valued functions |
| `tr_`, `TR_`          | Triggers               |

### PostgreSQL — Padrão

Functions em PostgreSQL normalmente não têm prefixo; nomes descritivos são preferidos.

---

## Árvore de pastas típica (discovery)

```
discovery/
├── DADOS-05-MAPA-DADOS.md                       # Snapshot (Módulo 1)
├── SNAP-MAPA-DADOS-2026-02-18.md               # Snapshot pontual
├── DADOS-06-STATUS-E-TRANSICOES.md             # Status Map (Módulo 2)
├── DADOS-09-MAPA-FLUXO-TABELAS.md              # Correlação status-fluxo
├── DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md    # Rotinas (Módulo 3 + Deep Dive)
├── SNAP-DADOS-10-VALIDACAO.md                  # Snapshot validação
├── DISC-00-INDICE.md                           # Índice geral (pendências)
├── DISC-98-FONTES-E-CONFIABILIDADE.md          # Fontes disponíveis
├── arquivos-legado.txt                         # Índice de arquivos SQL/código
├── FLUXO-*.md                                  # Fluxos documentados
├── TELA-*.md                                   # Telas documentadas
└── references/
    └── REFERENCE.md                             # Este arquivo
```

---

## Como confirmar pendências ([PEN])

Ao encontrar um item marcado `[PEN]`, sempre incluir a query sugerida. Exemplos:

### Status sem descrição

```
Status: `XX` — Significado desconhecido [PEN]
Confirmar: SELECT COUNT(*) FROM tabela WHERE status = 'XX';
           Buscar exemplos de registros neste status.
```

### Campo sem comentário

```
Coluna: `campo_misterioso` — Tipo, propósito desconhecido [PEN]
Confirmar: SELECT DISTINCT campo_misterioso FROM tabela WHERE campo_misterioso IS NOT NULL LIMIT 10;
           Buscar no código legado: rg "campo_misterioso"
```

### SP não confirmada como usada

```
SP: `USP_ANTIGA` — Encontrada no banco, mas não confirmada em chamadas [PEN]
Confirmar: rg "USP_ANTIGA" --type cs "<paths.legado>";
           Se nenhum resultado: SP pode ser obsoleta — considerar remover.
```

---

## Dicas de eficiência

- **Antes de executar qualquer query:** confirmar schema em `discovery-database.yml` — não hardcodar
- **Usar tabelas-resumo (Grupo B):** listá-las em DADOS-10 mas não criar fichas para SPs não usadas
- **Reutilizar Deep Dive:** se uma SP tem árvore complexa, executar Deep Dive apenas uma vez; reutilizar em provas de telas/fluxos
- **Validar pendências em lote:** ao final de um módulo, executar as queries de `[PEN]` todas de uma vez
- **Manter [PEN] até confirmar:** nunca remover `[PEN]` sem evidência substituindo-o

---

## Histórico de consolidação

- **2026-02-19:** Consolidação de discovery-10, discovery-11, discovery-12, discovery-13 em skill unificada `database-mcp`
  - Mantida toda a informação dos 4 módulos originais
  - Reorganizada em seções por responsabilidade
  - Criado REFERENCE.md consolidado
