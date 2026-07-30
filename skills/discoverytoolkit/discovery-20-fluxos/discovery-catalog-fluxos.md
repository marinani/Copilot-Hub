---
name: discovery-catalog-fluxos
description: [LEGACY] Skill mantida apenas como referência histórica. Use discovery-20-fluxos-catalago no lugar, que adiciona checkpoint obrigatório no chat para incluir fluxos importantes não mapeados automaticamente.
---


# Discovery Catalog Fluxos — Skill Legada

> **Legado:** para uso operacional atual, preferir `discovery-20-fluxos-catalago`.

> **Contexto:** Esta skill é genérica e deve ser usada em qualquer projeto discovery. Todas as configurações (engine, schema, banco, MCP, paths) são lidas do discovery-project.yml. Nunca usar valores fixos de projeto.
> Leia o arquivo de metodologia do projeto antes de executar (ex: DISC-99-METODOLOGIA-E-ARQUITETURA-DO-DISCOVERY.md).
> Sempre use queries compatíveis com o engine e schema definidos em database.engine e database.schema_principal.

## Responsabilidade

Gerar o **catálogo mestre de fluxos candidatos** do sistema Atendimento 156 com base **exclusivamente em consultas ao SQL Server** (schema `dbo`, banco `central`). Este passo é a **ponte entre a extração estrutural (Fase A/B) e a produção iterativa de FLUXOs (Fase D)**.

> **Regra fundamental:** A geração é **banco-driven**. Os CFs são construídos a partir de consultas SQL Server (inventário de tabelas, colunas de status, volume, comentários via extended properties). O código .NET pode ser referenciado apenas para indicar "onde confirmar" em itens `[PEN]`.

**O que este passo FAZ:**
- Consulta o banco (schema `dbo`) via SQL Server: inventário de tabelas, volume (`sys.partitions`), comentários (`sys.extended_properties`), colunas de status/situação/estado, tabelas de log/evento
- Agrupa tabelas por domínio (prefixo do nome, comentários) e monta CF-001..CF-NNN
- Para cada CF: tabelas principais (3–10), colunas status detectadas, volume estimado, 1–3 SQLs diagnósticas, rótulo de confiança
- Produz fila de produção priorizada (top 30) por impacto (volume/status)
- Nunca retorna zero CFs: se o banco não estiver acessível, gera CF-001 "Inventário indisponível" `[PEN]`
- DADOS-05, DADOS-06, DADOS-09, DADOS-10 são **referência opcional** para enriquecimento, não dependência obrigatória

**O que este passo NÃO FAZ:**
- Não cria `FLUXO-Fxx-*.md` — apenas o catálogo e a fila
- Não depende do parsing de DADOS-09 em Markdown (estrutura markdown varia; geração é banco-only)
- Não usa o código legado como fonte de regras de negócio
- Não menciona o novo stack

---

## Rótulos obrigatórios

| Rótulo | Quando usar |
|---|---|
| `` | Dado derivado de consultas SQL ao schema `prev` (estrutura, colunas, comentários, volume) |
| `` | Agrupamento heurístico (ex.: por prefixo de tabela, nome) a partir dos resultados do banco |
| `[PEN]` | Depende de regra de negócio/código ou banco indisponível — sempre incluir "como confirmar" |

**Nunca omitir o rótulo. `[PEN]` sempre acompanha instrução de confirmação.**

---

## Configuração do projeto

Ler `discovery-project.yml` antes de qualquer análise:

| Chave | Uso na skill |
|---|---|
| `paths.discovery` | Onde estão os DADOS-* de entrada e onde gravar os artefatos de saída |
| `database.schema_principal` | Schema de referência para as SQLs diagnósticas geradas |
| `rotulos.*` | Textos oficiais dos rótulos de confiabilidade |

---

## Fontes de entrada

**Fonte primária (obrigatória para CFs > 0):** consultas SQL ao PostgreSQL (schema `prev`) via MCP `project-0-156-project-1-api156-sqlserver`.

**Referências opcionais (enriquecimento):**

| Arquivo | Uso |
|---|---|
| `discovery/DADOS-09-MAPA-FLUXO-TABELAS.md` | Referência opcional; domínios são derivados do banco (prefixos/comentários), não do parsing deste arquivo |
| `discovery/DADOS-06-STATUS-E-TRANSICOES.md` | Referência opcional; colunas de status são detectadas via `information_schema` |
| `discovery/DADOS-05-MAPA-DADOS.md` | Referência opcional; volume vem de `pg_class.reltuples` |
| `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | Referência opcional para eventos observáveis |

Se o banco não estiver acessível via MCP, a skill gera um único CF-001 "Inventário indisponível" `[PEN]` e indica como confirmar o acesso.

---

## Arquivos gerados

| Arquivo | Tipo | Comportamento |
|---|---|---|
| `discovery/DISC-03-CATALOGO-DE-FLUXOS.md` | DISC — mantido atualizado | Substituído a cada re-execução |
| `discovery/SNAP-CATALOGO-FLUXOS-VALIDACAO.md` | SNAP — imutável após criação | Criado com data; novas execuções criam novo SNAP |

---

## Fluxo de trabalho

### Passo 0 — Ler configuração (OBRIGATÓRIO)

Ler `discovery-project.yml` e extrair:
- `paths.discovery` → diretório base para gravação dos artefatos
- `database.schema_principal` → schema para todas as SQLs (`dbo` neste projeto)
- `database.mcp_server` → `project-0-156-project-1-api156-sqlserver`
- `rotulos.*` → rótulos oficiais do projeto

### Passo 1 — Validar discovery

Garantir que o diretório `discovery` existe. DADOS-05/06/09/10 são opcionais; se existirem, podem ser lidos para referência, mas não bloqueiam a geração.

### Passo 2A — Banco: inventário de tabelas e volume (SQL Server)

```sql
-- Inventário de tabelas com volume estimado (SQL Server — schema dbo)
SELECT
    t.name                                AS table_name,
    SUM(p.rows)                           AS volume_estimado,
    ep.value                              AS comentario
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
LEFT JOIN sys.partitions p
    ON p.object_id = t.object_id AND p.index_id IN (0, 1)
LEFT JOIN sys.extended_properties ep
    ON ep.major_id = t.object_id AND ep.minor_id = 0 AND ep.name = 'MS_Description'
WHERE s.name = 'dbo'
GROUP BY t.name, ep.value
ORDER BY volume_estimado DESC;
```

### Passo 2B — Banco: detectar colunas de status/situação (SQL Server)

```sql
-- Detectar colunas de status (SQL Server — schema dbo)
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND (LOWER(COLUMN_NAME) LIKE '%status%'
    OR LOWER(COLUMN_NAME) LIKE '%situacao%'
    OR LOWER(COLUMN_NAME) LIKE '%estado%'
    OR LOWER(COLUMN_NAME) LIKE '%tipo%'
    OR LOWER(COLUMN_NAME) LIKE '%flag%'
    OR LOWER(COLUMN_NAME) LIKE '%situac%')
ORDER BY TABLE_NAME, COLUMN_NAME;
```

### Passo 2C — Banco: detectar tabelas de log/evento (SQL Server)

```sql
-- Detectar tabelas de log/evento (SQL Server — schema dbo)
SELECT name AS table_name
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE s.name = 'dbo'
  AND (LOWER(t.name) LIKE '%hist%'
    OR LOWER(t.name) LIKE '%log%'
    OR LOWER(t.name) LIKE '%event%'
    OR LOWER(t.name) LIKE '%audit%'
    OR LOWER(t.name) LIKE '%atend%'
    OR LOWER(t.name) LIKE '%consulta%')
ORDER BY t.name;
```

### Passo 3 — Construir CFs por domínio

- Agrupar tabelas por **prefixo** (primeiro segmento do nome, ex.: `SOLICITACAO_*` → domínio "Solicitação")
- Usar comentários de `sys.extended_properties` (MS_Description) para nome operacional do domínio
- Domínios esperados neste sistema: Solicitação, Assunto, Pessoa/Cidadão, Localização, Histórico, URBS, Hangfire
- Para cada domínio: 3–10 tabelas principais, colunas status (2B), volume (2A), rótulo:
  - `` quando há estrutura/colunas/comentários/volume do banco
  - `` quando agrupamento é apenas heurístico (prefixo)
  - `[PEN]` quando depender de regra de negócio/código ou banco indisponível
- Gerar 1–3 SQLs diagnósticas por CF (volumetria, distribuição de status, amostra)
- **Nunca retornar zero CFs:** se o banco falhar ou não estiver acessível via MCP, gerar CF-001 "Inventário indisponível" `[PEN]` com instrução de como confirmar o acesso

### Passo 4 — Prioridade e lacunas

- Ordenar CFs por impacto (volume, presença de status)
- Top 30 na fila de produção; top 15 no SNAP
- Registrar lacunas `[PEN]` (ex.: sem coluna de status detectada) com "como confirmar"

### Passo 5 — Gravar artefatos

1. Gravar `DISC-03-CATALOGO-DE-FLUXOS.md` com critério banco-only, lista de CFs (tabelas, status, volume, SQLs, rótulo) e fila top 30.
2. Gravar `SNAP-CATALOGO-FLUXOS-VALIDACAO.md` com total CFs, top 15, heurísticas aplicadas, lacunas.

---

## Formato do DISC-03-CATALOGO-DE-FLUXOS.md

O documento deve conter:

- **Criterio de geracao (banco-only):** descrição de que os CFs vêm de consultas SQL (Passo 2A/2B/2C), agrupamento por prefixo/comentários; DADOS-09 opcional.
- **Lista de CFs**, cada um com:
  - Nome operacional
  - Tabelas principais (3–10) e volume estimado
  - Colunas status/situação detectadas
  - 1–3 SQLs diagnósticas (somente SQL)
  - Rótulo de confiança: ``, ``, `[PEN]`
- **Fila de produção** — Top 30 por impacto

Exemplo de cabeçalho e regras:

```markdown
# DISC-03-CATALOGO-DE-FLUXOS

Tipo: Documento Operacional — Catálogo de Fluxos Candidatos
Código: DISC-03
Nome: Catálogo de Fluxos Candidatos — GPrev (banco-only)
Escopo: Schema prev do banco `central` — evidência exclusivamente do banco; sem referências ao novo stack
Relacionados: DADOS-05/06/09/10 (opcionais); consultas diretas ao schema prev
Última atualização: YYYY-MM-DD
Palavras-chave do domínio: fluxo candidato, CF, catálogo, fila de produção, banco-only, priorização, domínio funcional

---

## Criterio de geracao (banco-only)
...
## Regras deste documento

1. **Fonte exclusiva:** banco de dados (schema `prev`) via DADOS-05, DADOS-06, DADOS-09, DADOS-10.
2. **Rótulos obrigatórios:** ``, ``, `[PEN]`.
3. **Proibido:** mencionar o novo stack (API nova, frontends Angular, microsserviços).
4. **Este documento NÃO é um FLUXO:** não contém caminho feliz, variações ou exceções completas.
5. **Uso:** serve como fila de trabalho para a Fase D (produção iterativa de FLUXOs).

---

## Fluxos Candidatos

### CF-001 — <Nome operacional>

**Domínio de origem:** BLOCO N do DADOS-09  
**Rótulo de confiança:**

**Tabelas principais:**
| Tabela | Papel | Volume |
|---|---|---|
| `prev.tabela_a` | Entidade central | N registros |
| `prev.tabela_b` | Controle de status | N registros |

**Status/situação relevantes:**
| Coluna | Tabela | Valores mapeados |
|---|---|---|
| `situacao` | `tabela_a` | ATIVO, INATIVO, PENDENTE |

**Eventos observáveis no banco:**
- Mudança de `situacao` em `tabela_a` (INSERT + UPDATE)
- Inserção em `log_acoes` após operação principal
- Function `prev.fn_xyz` opera sobre `tabela_a`

**SQLs diagnósticas:**
```sql
-- Volumetria
SELECT COUNT(*) FROM prev.tabela_a;

-- Distribuição de status
SELECT situacao, COUNT(*) FROM prev.tabela_a GROUP BY 1 ORDER BY 2 DESC;
```

---

## Fila de Produção — Top 30 por Impacto

| # | CF | Nome operacional | Tabelas escritas | Status mapeados | Rotinas | Justificativa |
|---|---|---|---|---|---|---|
| 1 | CF-001 | ... | N | S | N | ... |

---
```

---

## Formato do SNAP-CATALOGO-FLUXOS-VALIDACAO.md

O SNAP deve conter:

- **Sumário da execução:** total CFs, CFs por rótulo, banco disponível (sim/não), data.
- **Top 15 CFs por impacto (volume/status).**
- **Heurísticas aplicadas:** lista das regras usadas (agrupamento por prefixo, comentários, etc.).
- **Lacunas [PEN]:** tabela CF | Lacuna | Como confirmar.

Exemplo:

```markdown
# SNAP-CATALOGO-FLUXOS-VALIDACAO
...
## Sumário da execução
| Item | Valor |
| Total de CFs gerados | N |
| Banco disponivel | sim/nao |
...

## Top 15 CFs por impacto (volume/status)
## Heuristicas aplicadas
## Lacunas [PEN]
```

---

## Regras de qualidade

- Cada CF deve ter **entre 3 e 10 tabelas** (nem muito vago, nem muito granular).
- SQLs diagnósticas devem ser **apenas SQL** — sem resultado esperado, sem comentário de negócio.
- `[PEN]` exige instrução concreta de confirmação (query SQL ou busca com `rg` no legado).
- O documento DISC-03 **não é um FLUXO** — não deve conter "caminho feliz", "variações" ou "exceções".
- SNAP imutável após criação — nova execução cria novo SNAP com data atualizada.
- DISC-03 é substituído a cada re-execução (idempotente).

---

## Execução no Cursor (MCP)

**Pré-requisito:** MCP `project-0-156-project-1-api156-sqlserver` ativo e `discovery-project.yml` presente.

**Prompt padrão:**
```
Execute o Passo 6 do ritual — gere o catálogo de fluxos candidatos a partir do banco
```

O agente lê esta SKILL.md, consulta o banco via MCP e grava os artefatos em `discovery/`.

**Regras de execução:**
- Sempre ler `discovery-project.yml` antes de qualquer query
- Todas as queries usam o schema definido em `database.schema_principal`
- Artefatos gerados gravados em `paths.discovery` (padrão: `discovery/`)
- Estado da execução vive nos arquivos `DISC-03` e `SNAP-CATALOGO-FLUXOS-VALIDACAO`

Ver [references/REFERENCE.md](references/REFERENCE.md) para contexto adicional.
