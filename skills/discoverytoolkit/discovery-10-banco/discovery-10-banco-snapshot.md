---
name: discovery-10-banco-snapshot
description: Extrai snapshot operacional do schema principal do projeto ativo (engine e schema lidos de discovery-project.yml) e gera ou atualiza arquivos DADOS-* e SNAP-* em discovery/. Use quando o usuário pedir para extrair estrutura do banco, documentar tabelas, gerar snapshot de schema ou mapear colunas e tipos do schema principal.
---

# Discovery DB Snapshot

> **Antes de qualquer ação:** ler `discovery-project.yml` e extrair `database.engine`, `database.schema_principal` e `database.mcp_server`.
> Executar **apenas** o bloco SQL correspondente ao `database.engine` configurado (`postgresql` ou `sqlserver`).
> MCP a usar: valor de `database.mcp_server` em `discovery-project.yml`.
> Schema a usar em todas as queries: valor de `database.schema_principal` em `discovery-project.yml` (ex.: `public` para PostgreSQL, `dbo` para SQL Server).

## Responsabilidade

Extrair e documentar a estrutura do schema principal do projeto ativo (engine e schema lidos de `discovery-project.yml`) em arquivos de evidência rastreáveis.

## Rótulos obrigatórios

| Rótulo | Quando usar |
|---|---|
| `` | Dado extraído diretamente via query ou DDL do schema principal |
| `` | Conclusão lógica a partir de nomes/comentários; sem query direta |
| `[PEN]` | Sem evidência disponível — sempre incluir "como confirmar" |

**Nunca omitir o rótulo. Nunca assumir comportamento sem evidência.**

## Fontes de extração

Prioridade de consulta:

1. **Queries diretas** ao schema principal (DDL, `information_schema`, catálogos internos do engine)
2. **Arquivos DDL/SQL** encontrados via `discovery/arquivos-legado.txt`
3. **Código legado** (`paths.legado` de `discovery-project.yml`) para confirmar mapeamentos de entidade — ler o caminho do arquivo de configuração, nunca hardcodar

> **Antes de qualquer query:** ler `discovery-project.yml` e extrair `database.engine` (`postgresql` ou `sqlserver`), `database.schema_principal` e `database.mcp_server`. Em cada passo abaixo há dois blocos SQL — executar **apenas** o bloco correspondente ao engine configurado.

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `discovery/DADOS-05-MAPA-DADOS.md` | Catálogo de tabelas e colunas principais |
| `discovery/SNAP-MAPA-DADOS-YYYY-MM-DD.md` | Snapshot pontual — criar ao extrair pela primeira vez ou após mudança relevante |
| `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | Functions, procedures e triggers (quando solicitado) |

Criar `SNAP-*` apenas quando o usuário solicitar um snapshot formal ou quando os dados mudarem substancialmente.

## Fluxo de trabalho

1. **Ler configuração**: extrair `database.engine`, `database.schema_principal` e `database.mcp_server` do `discovery-project.yml`.
2. **Identificar tabelas-alvo**: perguntar ao usuário quais tabelas ou qual escopo (módulo, fluxo).
3. **Extrair estrutura** usando o bloco SQL do engine correto (ver seção abaixo): colunas, tipos, `NOT NULL`, defaults, comentários, PKs, FKs.
4. **Rotular cada campo** com o nível de confiança adequado.
5. **Registrar pendências**: para colunas sem comentário ou com nome ambíguo, marcar `[PEN]` com consulta sugerida.
6. **Gravar no arquivo correto**: atualizar `DADOS-05` ou criar `SNAP-*` conforme orientado.

## Queries de extração por engine

### Listar tabelas do schema

**`postgresql`:**

```sql
-- Substituir <schema_principal> pelo valor de database.schema_principal
SELECT
    t.table_name,
    obj_description(('"' || t.table_schema || '"."' || t.table_name || '"')::regclass) AS comentario
FROM information_schema.tables t
WHERE t.table_schema = '<schema_principal>'
  AND t.table_type = 'BASE TABLE'
ORDER BY t.table_name;
```

**`sqlserver`:**

```sql
-- Substituir <schema_principal> pelo valor de database.schema_principal
SELECT
    t.name AS table_name,
    ep.value AS comentario
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
LEFT JOIN sys.extended_properties ep
    ON ep.major_id = t.object_id AND ep.minor_id = 0 AND ep.name = 'MS_Description'
WHERE s.name = '<schema_principal>'
ORDER BY t.name;
```

### Listar colunas de uma tabela

**`postgresql`:**

```sql
-- Substituir <schema_principal> e <tabela>
SELECT
    c.column_name,
    c.data_type,
    c.character_maximum_length,
    c.is_nullable,
    c.column_default,
    pgd.description AS comentario
FROM information_schema.columns c
LEFT JOIN pg_class       pgc ON pgc.relname = c.table_name
LEFT JOIN pg_namespace   pgn ON pgn.oid = pgc.relnamespace AND pgn.nspname = c.table_schema
LEFT JOIN pg_attribute   pga ON pga.attrelid = pgc.oid AND pga.attname = c.column_name
LEFT JOIN pg_description pgd ON pgd.objoid = pgc.oid AND pgd.objsubid = pga.attnum
WHERE c.table_schema = '<schema_principal>'
  AND c.table_name   = '<tabela>'
ORDER BY c.ordinal_position;
```

**`sqlserver`:**

```sql
-- Substituir <schema_principal> e <tabela>
SELECT
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.IS_NULLABLE,
    c.COLUMN_DEFAULT,
    ep.value AS comentario
FROM INFORMATION_SCHEMA.COLUMNS c
LEFT JOIN sys.extended_properties ep
    ON ep.major_id  = OBJECT_ID(c.TABLE_SCHEMA + '.' + c.TABLE_NAME)
   AND ep.minor_id  = c.ORDINAL_POSITION
   AND ep.name      = 'MS_Description'
WHERE c.TABLE_SCHEMA = '<schema_principal>'
  AND c.TABLE_NAME   = '<tabela>'
ORDER BY c.ORDINAL_POSITION;
```

### Listar PKs e FKs

**`postgresql`:**

```sql
-- PKs — substituir <schema_principal> e <tabela>
SELECT kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON kcu.constraint_name = tc.constraint_name AND kcu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'PRIMARY KEY'
  AND tc.table_schema = '<schema_principal>'
  AND tc.table_name   = '<tabela>';

-- FKs — substituir <schema_principal> e <tabela>
SELECT
    kcu.column_name,
    ccu.table_schema AS tabela_referenciada_schema,
    ccu.table_name   AS tabela_referenciada,
    ccu.column_name  AS coluna_referenciada
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON kcu.constraint_name = tc.constraint_name AND kcu.table_schema = tc.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = '<schema_principal>'
  AND tc.table_name   = '<tabela>';
```

**`sqlserver`:**

```sql
-- PKs — substituir <schema_principal> e <tabela>
SELECT col.name AS column_name
FROM sys.indexes        idx
JOIN sys.index_columns  ic  ON ic.object_id = idx.object_id AND ic.index_id = idx.index_id
JOIN sys.columns        col ON col.object_id = idx.object_id AND col.column_id = ic.column_id
JOIN sys.tables         t   ON t.object_id = idx.object_id
JOIN sys.schemas        s   ON s.schema_id = t.schema_id
WHERE idx.is_primary_key = 1
  AND s.name = '<schema_principal>'
  AND t.name = '<tabela>';

-- FKs — substituir <schema_principal> e <tabela>
SELECT
    col.name                              AS column_name,
    SCHEMA_NAME(rt.schema_id)             AS tabela_referenciada_schema,
    rt.name                               AS tabela_referenciada,
    rcol.name                             AS coluna_referenciada
FROM sys.foreign_key_columns fkc
JOIN sys.foreign_keys        fk   ON fk.object_id = fkc.constraint_object_id
JOIN sys.tables              t    ON t.object_id  = fkc.parent_object_id
JOIN sys.schemas             s    ON s.schema_id  = t.schema_id
JOIN sys.columns             col  ON col.object_id = fkc.parent_object_id AND col.column_id = fkc.parent_column_id
JOIN sys.tables              rt   ON rt.object_id  = fkc.referenced_object_id
JOIN sys.columns             rcol ON rcol.object_id = fkc.referenced_object_id AND rcol.column_id = fkc.referenced_column_id
WHERE s.name = '<schema_principal>'
  AND t.name = '<tabela>';
```

## Formato de saída (por tabela)

```markdown
### `nome_da_tabela`

> Comentário da tabela (se existir no DDL)

| Coluna | Tipo | Nulo | Default | Descrição |
|---|---|---|---|---|
| id | bigint | NÃO | — | PK |
| status | varchar(30) | NÃO | — | Situação atual |
| obs | text | SIM | — | Observação livre [A confirmar — verificar uso no legado] |
```

## Restrições

- Não mencionar stack novo (API nova, microserviços) — este documento descreve apenas o legado.
- Não inferir regras de negócio a partir de nomes de coluna sem evidência; usar `` com justificativa.
- Não alterar `DISC-*` neste passo; registrar apenas em `DADOS-*` e `SNAP-*`.
- Nunca misturar SQL de engines diferentes. Ler `database.engine` do `discovery-project.yml` antes de qualquer query.
- Registrar no cabeçalho do documento gerado qual engine foi utilizado.

---

## Execução no Cursor (MCP)

**Pré-requisito:** MCP configurado em `database.mcp_server` (de `discovery-project.yml`) ativo.

**Prompt padrão:**
```
Extraia o snapshot de tabelas e colunas do schema principal
```

O agente lê esta SKILL.md, consulta o banco via MCP e grava os artefatos em `discovery/`.

**Regras de execução:**
- Sempre ler `discovery-project.yml` antes de qualquer query
- Executar apenas o bloco SQL correspondente ao engine (`database.engine`)
- Artefatos gerados em `paths.discovery`; estado vive em `DADOS-05` e `SNAP-MAPA-DADOS-YYYY-MM-DD`

---

## Referências adicionais

- Para contexto dos DADOS já documentados, ver [references/REFERENCE.md](references/REFERENCE.md)

---

## Passo final — Atualizar o plano

Ao concluir a geração dos artefatos desta skill, **executar obrigatoriamente** a atualização do plano de discovery:

`
Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto
`

O plano re-inspeciona o estado real da pasta discovery/ e reflete os artefatos recém-gerados, desbloqueando automaticamente a próxima onda de execução.


