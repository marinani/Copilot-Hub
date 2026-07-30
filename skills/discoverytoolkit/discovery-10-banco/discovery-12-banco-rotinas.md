---
name: discovery-12-banco-rotinas
description: Documenta stored procedures, functions, triggers e jobs do sistema com fichas em linguagem natural. Filtra obrigatoriamente pelo Passo 0c — documenta SOMENTE SPs confirmadas no código legado (Grupo A); SPs não usadas entram apenas na tabela-resumo (Grupo B). Para cada SP do Grupo A gera ficha com dois níveis: (1) "O que representa para o negócio" — interpretação orientada ao usuário que alimenta diretamente a Seção 1 e 8.1 da documentação de telas; (2) "Regras de negócio identificadas" — cada validação/IF/RAISERROR extraída como regra em linguagem natural com ID sugerido RN-SP-*. A ficha é a fonte de verdade que o Passo 2-B de discovery - 30 - telas - documentar-tela consome sem precisar reler a SP. Gera DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md com fichas completas, referências cruzadas a telas e fluxos, e SNAP-DADOS-10-VALIDACAO.md. Use quando o usuário pedir para mapear rotinas do banco, documentar SPs, gerar fichas de procedures em linguagem natural, ou regenerar DADOS-10.
---

# Discovery DB Rotinas

> **Antes de qualquer ação:** ler `discovery-project.yml` e extrair `database.engine`, `database.schema_principal` e `database.mcp_server`.
> Executar **apenas** o bloco SQL correspondente ao `database.engine` configurado (`postgresql` ou `sqlserver`).
> **Jobs agendados:** verificar se usa Hangfire, Quartz ou SQL Server Agent conforme `discovery-project.yml`.

## Responsabilidade

Documentar com fichas em linguagem natural todas as rotinas do sistema:

- **Stored Procedures e Functions** — corpo extraído de pasta local (`.sql`) ou do banco via MCP
- **Triggers** — via banco (sys.triggers)
- **Jobs agendados** — Hangfire, Quartz ou SQL Server Agent, conforme configuração

**Filtro obrigatório:** documentar apenas rotinas **efetivamente usadas pelo sistema** — confirmadas por chamada no código legado (`.cs`, `.vb`, `.java`). Rotinas de outros sistemas no mesmo banco compartilhado devem ser identificadas e excluídas da documentação principal.

**Princípio central:** cada SP ou Function deve ter uma ficha de documentação em linguagem natural, legível por um analista de negócio, descrevendo o que a rotina faz, quais dados manipula, e em quais telas e fluxos ela é invocada.

**Princípio de negócio:** a ficha de cada SP deve conter uma interpretação de negócio — o que esta SP representa para o usuário do sistema, não apenas o que ela faz tecnicamente. Esta interpretação é a fonte que a documentação de telas (`discovery - 30 - telas - documentar-tela`, Passo 2-B) consumirá para enriquecer o Objetivo, as Regras de negócio e os Critérios de aceitação de cada tela. Quanto mais rica a ficha da SP, mais precisa e completa será a documentação da tela correspondente.

---

## Fontes de extração (em ordem de prioridade)

1. **Pasta local de SPs** (`paths.sps_local` em `discovery-project.yml`, ou informada pelo usuário) — arquivos `.sql` lidos diretamente; **preferencial quando disponível**
2. **Banco via MCP** (`sys.objects` + `sys.sql_modules`) — usado quando pasta local não existe ou SP não tem arquivo correspondente
3. **Código legado** (`paths.legado`) — confirmar quais SPs são efetivamente chamadas e em qual contexto

---

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | Catálogo completo com fichas em linguagem natural de functions, procedures, triggers e jobs |
| `discovery/SNAP-DADOS-10-VALIDACAO.md` | Snapshot de validação: totais, divergências, itens [PEN] |

Criar `SNAP-*` apenas quando o usuário solicitar validação formal ou regeneração completa.

---

## Fluxo de trabalho

### Passo 0 — Ler a configuração do projeto (OBRIGATÓRIO)

Ler o arquivo `discovery-project.yml` e extrair:

| Campo | Chave no arquivo | Usado em |
|---|---|---|
| Engine do banco | `database.engine` | Selecionar bloco SQL correto (`postgresql` ou `sqlserver`) |
| Schema principal | `database.schema_principal` | Todas as queries SQL |
| Servidor MCP | `database.mcp_server` | Identificar qual MCP usar para executar SQL |
| Caminho do legado | `paths.legado` | Busca de chamadas no código com `rg` |
| Pasta local de SPs | `paths.sps_local` | Fonte alternativa ao banco — arquivos `.sql` locais |

**Nunca usar valores hardcoded de schema ou engine.** Sempre ler do `discovery-project.yml`.

Se o arquivo não existir: interromper e avisar o usuário que `discovery-project.yml` precisa ser criado antes de executar a skill.

---

### Passo 0b — Detectar fonte das definições de SP (OBRIGATÓRIO)

Determinar qual fonte será usada para obter o **corpo (definição)** das SPs:

#### Caso A — Pasta local fornecida

A pasta local existe quando **qualquer uma** das condições abaixo for verdadeira:

- `paths.sps_local` está preenchida em `discovery-project.yml` E o caminho existe no filesystem
- O usuário informou explicitamente um caminho de pasta nesta sessão (ex.: "use a pasta C:\sps")

**Procedimento quando pasta local está disponível:**

1. Listar todos os arquivos `.sql` na pasta (incluindo subpastas):
   ```
   Get-ChildItem -Path "<paths.sps_local>" -Recurse -Filter "*.sql" | Select-Object Name, FullName
   ```
2. Extrair o nome de cada SP a partir do nome do arquivo (convenção: `USP_CO_NomeDaSP.sql` → `USP_CO_NomeDaSP`) ou do conteúdo (`CREATE PROCEDURE`/`CREATE OR ALTER PROCEDURE`).
3. **Não executar as queries do Passo 1 e Passo 5** (sys.objects / sys.sql_modules) — o corpo já está nos arquivos locais.

#### Caso B — Sem pasta local

Usar banco via MCP normalmente (Passos 1, 2, 5).

#### Regra de fusão (quando ambas as fontes existem)

Se pasta local existe mas uma SP não tem arquivo correspondente (foi removida do filesystem mas ainda existe no banco): buscar no banco via Passo 5.

---

### Passo 0c — Filtrar SPs usadas pelo sistema (OBRIGATÓRIO)

**Independente da fonte** (pasta local ou banco), aplicar o filtro de uso antes de documentar:

1. Obter a lista de nomes de SPs disponíveis (do filesystem ou do banco).
2. Para cada SP, buscar no código legado:
   ```
   rg "<nome_da_SP>" <paths.legado> --type cs -l
   ```
   Ou para múltiplas SPs de uma vez (mais eficiente):
   ```
   rg "USP_CO_|USP_CONC_|UFN_" <paths.legado> --type cs -o --no-filename | sort -u
   ```
3. Construir dois grupos:
   - **Grupo A — Usadas pelo sistema:** ao menos 1 resultado no código legado → documentar com ficha completa em linguagem natural
   - **Grupo B — Não usadas / sistemas externos:** nenhum resultado no código legado → listar apenas na tabela-resumo com nota "Não utilizada pelo sistema" ou "Sistema externo"

3b. **⚠️ Regra obrigatória — verificar se funções Grupo B são chamadas por triggers:**

   Após classificar as funções em Grupo A/B pelo código legado, cruzar obrigatoriamente com o resultado do **Passo 3 (Triggers)**. Uma função que não é chamada diretamente pelo código C# **pode ser invocada indiretamente via trigger** — e triggers disparam em INSERT/UPDATE/DELETE nas tabelas, ou seja, **são acionados pela tela que grava dados**. Se ignorada, a função impacta silenciosamente o comportamento da tela sem aparecer no código da aplicação.

   **Procedimento:**
   1. Para cada função do Grupo B, verificar se ela aparece na coluna `funcao_trigger` do resultado do Passo 3.
   2. Se aparecer: **reclassificar para Grupo A** — a função é chamada indiretamente pela tela que executa o DML na tabela do trigger.
   3. Preencher na ficha da função a seção "Telas que usam" com: `[via trigger <nome_trigger> na tabela <nome_tabela> — acionado pela tela que grava dados nesta tabela]`.
   4. Preencher a seção "O que representa para o negócio" explicitando que a função é invocada automaticamente pelo banco quando a tela persiste o registro, sem que o código da aplicação precise chamá-la explicitamente.

   **Exemplo de preenchimento:**
   ```
   Telas que usam:
   | — | [via trigger trg_calcular_status na tabela Inscricao — disparado automaticamente pelo banco
         em qualquer INSERT/UPDATE executado pelo código da aplicação nesta tabela]
   ```

   **Impacto:** a função reclassificada deve receber ficha completa em linguagem natural (Passo 7) porque seu comportamento afeta o resultado visível ao usuário após cada gravação.

4. Registrar o critério de filtro aplicado no cabeçalho do `DADOS-10`:
   > "SPs documentadas em linguagem natural: somente aquelas com chamadas confirmadas no código legado em `<paths.legado>`. SPs sem chamada confirmada são listadas apenas na tabela-resumo."

**Regra de exceção:** se o código legado não estiver disponível (pasta não existe), documentar todas as SPs e avisar o usuário que o filtro de uso não pôde ser aplicado.

---

### Passo 1 — Listar functions e procedures via banco (somente Caso B — sem pasta local)

**`sqlserver`** — via `sys.objects`:

```sql
-- Substituir <schema_principal> pelo valor de database.schema_principal em discovery-project.yml
SELECT
    o.name                                             AS nome,
    s.name                                             AS schema_name,
    o.type_desc                                        AS tipo_descr,
    o.modify_date                                      AS ultima_modificacao,
    ep.value                                           AS comentario
FROM sys.objects o
JOIN sys.schemas s    ON s.schema_id = o.schema_id
LEFT JOIN sys.extended_properties ep
    ON ep.major_id = o.object_id AND ep.minor_id = 0 AND ep.name = 'MS_Description'
WHERE s.name = '<schema_principal>'
  AND o.type IN ('FN', 'IF', 'TF', 'P')   -- FN=scalar, IF=inline table, TF=multi-stmt table, P=procedure
ORDER BY o.type_desc, o.name;
```

**`postgresql`** — via `pg_proc`:

```sql
-- Substituir <schema_principal> pelo valor de database.schema_principal em discovery-project.yml
SELECT
    p.proname                                          AS nome,
    n.nspname                                          AS schema_name,
    pg_get_function_identity_arguments(p.oid)          AS assinatura,
    CASE p.proisagg
        WHEN true THEN 'AGGREGATE'
        ELSE 'FUNCTION'
    END                                                AS tipo_descr,
    t.typname                                          AS tipo_retorno,
    d.description                                      AS comentario
FROM pg_proc p
JOIN pg_namespace n  ON n.oid = p.pronamespace
LEFT JOIN pg_type t  ON t.oid = p.prorettype
LEFT JOIN pg_description d
    ON d.objoid = p.oid AND d.classoid = 'pg_proc'::regclass
WHERE n.nspname = '<schema_principal>'
ORDER BY tipo_descr, p.proname;
```

---

### Passo 2 — Checagem cruzada via information_schema (somente Caso B — sem pasta local)

```sql
-- Funciona em postgresql e sqlserver — substituir <schema_principal>
SELECT
    routine_name,
    routine_type,
    data_type,
    external_language
FROM information_schema.routines
WHERE specific_schema = '<schema_principal>'
ORDER BY routine_type, routine_name;
```

**Divergência esperada (sqlserver):** `information_schema.routines` não lista triggers — esses são capturados no Passo 3.

---

### Passo 3 — Triggers

**`sqlserver`** — via `sys.triggers`:

```sql
-- Substituir <schema_principal> pelo valor de database.schema_principal em discovery-project.yml
SELECT
    t.name                                                        AS trigger_name,
    OBJECT_NAME(t.parent_id)                                      AS tabela,
    s.name                                                        AS schema_name,
    CASE WHEN t.is_instead_of_trigger = 1 THEN 'INSTEAD OF'
         ELSE 'AFTER'
    END                                                           AS timing,
    CASE WHEN OBJECTPROPERTY(t.object_id, 'ExecIsInsertTrigger') = 1 THEN 'INSERT ' ELSE '' END +
    CASE WHEN OBJECTPROPERTY(t.object_id, 'ExecIsDeleteTrigger') = 1 THEN 'DELETE ' ELSE '' END +
    CASE WHEN OBJECTPROPERTY(t.object_id, 'ExecIsUpdateTrigger') = 1 THEN 'UPDATE'  ELSE '' END AS evento,
    o.name                                                        AS funcao_trigger
FROM sys.triggers  t
JOIN sys.objects   o  ON o.object_id = t.object_id
JOIN sys.schemas   s  ON s.schema_id = o.schema_id
WHERE s.name = '<schema_principal>'
ORDER BY OBJECT_NAME(t.parent_id), t.name;
```

**`postgresql`** — via `pg_trigger`:

```sql
SELECT
    tg.tgname                              AS trigger_name,
    c.relname                              AS tabela,
    n.nspname                              AS schema_name,
    CASE tg.tgtype & 66
        WHEN 2  THEN 'BEFORE'
        WHEN 64 THEN 'INSTEAD OF'
        ELSE 'AFTER'
    END                                    AS timing,
    CASE WHEN tg.tgtype & 4  > 0 THEN 'INSERT ' ELSE '' END ||
    CASE WHEN tg.tgtype & 8  > 0 THEN 'DELETE ' ELSE '' END ||
    CASE WHEN tg.tgtype & 16 > 0 THEN 'UPDATE'  ELSE '' END  AS evento,
    p.proname                              AS funcao_trigger
FROM pg_trigger    tg
JOIN pg_class      c  ON c.oid  = tg.tgrelid
JOIN pg_namespace  n  ON n.oid  = c.relnamespace
JOIN pg_proc       p  ON p.oid  = tg.tgfoid
WHERE n.nspname = '<schema_principal>'
  AND NOT tg.tgisinternal
ORDER BY c.relname, tg.tgname;
```

Se resultado vazio: registrar **"Nenhum trigger encontrado"** com a consulta SQL usada como referência.

---

### Passo 4 — Jobs Hangfire

```sql
-- Lista jobs Hangfire com estado e dados de invocação
SELECT
    j.Id,
    j.StateName,
    j.CreatedAt,
    j.ExpireAt,
    j.InvocationData,
    j.Arguments
FROM hangfire.Job j
ORDER BY j.CreatedAt DESC;
```

Anotar o `InvocationData` de cada job — contém o nome da classe e método .NET invocado (JSON).

Complementar com busca no código:
```
rg "AddHangfireServer|RecurringJob|BackgroundJob" <paths.legado>
```

---

### Passo 5 — Obter definição completa (fonte para a documentação em linguagem natural)

#### Caso A — Pasta local disponível

Para cada SP do **Grupo A** (usadas pelo sistema), ler diretamente o arquivo correspondente na pasta local:

```
Read: <paths.sps_local>\<NomeDaSP>.sql
```

Se o nome do arquivo não corresponder exatamente ao nome da SP, tentar variações:
- `<NomeDaSP>.sql`
- `<NomeDaSP>.Sql`
- Subpasta com nome do grupo (ex.: `USP_CO\USP_CO_FinalizarInscricao.sql`)

Se o arquivo não for encontrado para uma SP do Grupo A: tentar buscar no banco (Caso B). Se também não encontrar no banco: **registrar como pendência de documentação** (ver Passo 5c).

#### Caso B — Banco via MCP

**`sqlserver`:**

```sql
-- Substituir <schema_principal> e <nome_da_rotina>
SELECT m.definition
FROM sys.sql_modules m
JOIN sys.objects     o ON o.object_id = m.object_id
JOIN sys.schemas     s ON s.schema_id = o.schema_id
WHERE s.name  = '<schema_principal>'
  AND o.name  = '<nome_da_rotina>';
```

**`postgresql`:**

```sql
SELECT pg_get_functiondef(p.oid)
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = '<schema_principal>'
  AND p.proname = '<nome_da_rotina>';
```

#### Regras para uso da definição completa

- **SPs críticas** (chamadas por múltiplos fluxos ou com modificação recente): sempre ler o corpo completo para gerar a narrativa em linguagem natural.
- **SPs utilitárias simples** (listas de domínio, lookups com nome autoexplicativo): pode-se inferir o comportamento pelo nome; indicar na ficha que o comportamento foi deduzido pelo nome e não verificado.
- **SPs com corpo > 100 linhas**: registrar resumo por bloco lógico na narrativa em linguagem natural; não copiar o corpo SQL integralmente para o DADOS-10.
- **SP não localizada em nenhuma fonte**: **registrar como pendência de documentação** (ver Passo 5c) e não criar ficha.

---

### Passo 5b — Extrair parâmetros formais

**`sqlserver`:**

```sql
-- Listar parâmetros de entrada e saída de uma SP ou Function
SELECT
    p.name                          AS parametro,
    TYPE_NAME(p.user_type_id)       AS tipo,
    p.max_length,
    p.is_output                     AS saida,
    p.has_default_value,
    p.default_value
FROM sys.parameters p
JOIN sys.objects o ON o.object_id = p.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE s.name = '<schema_principal>'
  AND o.name = '<nome_da_rotina>'
ORDER BY p.parameter_id;
```

---

### Passo 5c — Registrar pendências de documentação

Para cada SP do **Grupo A** (usada pelo sistema) cuja definição **não foi localizada** em nenhuma fonte (pasta local e banco consultados sem resultado):

1. **Não criar ficha** — a ausência do corpo impede documentação confiável em linguagem natural.
2. Adicionar entrada na seção **"Pendências de documentação"** do `DADOS-10`:

```markdown
## Pendências de documentação

| SP / Function | Chamada em | Por que está pendente | Como resolver |
|---|---|---|---|
| `USP_CO_ExemplosP` | `ExemploRepositorio.cs` | Definição não encontrada na pasta local nem no banco via sys.sql_modules | Solicitar ao DBA o script de criação ou verificar se a SP foi renomeada |
```

3. Marcar na tabela-resumo a coluna "Ficha detalhada" como `— pendência` em vez de link.
4. Ao final da execução, informar ao usuário o total de pendências geradas e listar os nomes.

---

### Passo 6 — Levantar referências cruzadas (telas e fluxos)

#### 6a — Quais arquivos de código chamam a SP?

Buscar no código legado:

```
rg "<nome_da_SP>" <paths.legado> --type cs -l
```

Anotar os arquivos encontrados. Cada arquivo geralmente corresponde a um repositório ou serviço, que por sua vez é chamado por um ou mais controllers (telas da API).

#### 6b — Mapear controllers e endpoints (telas)

Para cada arquivo encontrado no passo 6a:

```
rg "class.*Controller" <paths.legado> --type cs -A 3
```

Cruzar com `TELA-CATALOGO.md` (se existir) para identificar o endpoint exato.

#### 6c — Mapear fluxos documentados

Buscar nos arquivos FLUXO-*.md em `discovery/`:

```
rg "<nome_da_SP>" discovery/ --include "FLUXO-*.md"
```

Se não encontrado, verificar se o fluxo existe mas não menciona a SP explicitamente — nesse caso registrar "fluxo não identificado" na ficha.

---

### Passo 7 — Escrever a ficha em linguagem natural de cada SP (Grupo A)

**Somente para SPs do Grupo A** (confirmadas no código legado pelo Passo 0c). SPs do Grupo B não recebem ficha.

**Sequência obrigatória para cada SP:**

1. **Ler e compreender** o corpo completo da SP (arquivo local ou banco)
2. **Perguntar antes de escrever:**
   - Qual ação do usuário dispara esta SP?
   - O que muda no sistema após a execução?
   - Quais condições o negócio impõe para que execute com sucesso?
   - O que pode dar errado e o que o sistema faz nesse caso?
3. **Escrever "O que representa para o negócio"** — campo mais importante da ficha; alimenta diretamente a Seção 1 (Objetivo) da tela que usa esta SP
4. **Extrair regras de negócio** — cada `IF`, validação, `RAISERROR` ou condição de rejeição vira uma linha na tabela "Regras de negócio identificadas"; prefixar com `[Regra]` na "Lógica principal"
5. **Executar Passo 6** (referências cruzadas — telas e fluxos) e preencher as seções "Telas que usam" e "Fluxos que usam"

**Ordem de prioridade:**
1. SPs de escrita (INSERT/UPDATE/DELETE) chamadas por controllers de formulário — maior impacto de negócio
2. SPs com múltiplas validações — maior extração de regras de negócio
3. SPs de leitura crítica (lookups de status, elegibilidade)
4. SPs utilitárias simples — nível básico (tabela-resumo + campo "O que representa" apenas)

---

## Formato de Ficha por SP/Function (linguagem natural)

> **Princípio de preenchimento:** ler e compreender a SP completamente antes de escrever qualquer campo. A ficha deve ser rica o suficiente para que a documentação de telas (`discovery - 30 - telas - documentar-tela`, Passo 2-B) consiga enriquecer o Objetivo, as Regras de negócio e os Critérios de aceitação **sem precisar reler a SP**. A ficha é a fonte de verdade de negócio para a tela que a usa.

```markdown
### `<schema>.<nome_da_SP>` · <tipo>

**Fonte da definição:** arquivo local `<NomeDaSP>.sql` | banco via sys.sql_modules
**Chamada por:** `NomeRepositorio.cs` / `NomeService.cs`

#### O que representa para o negócio

<Interpretação em linguagem de negócio — o que esta SP significa para o USUÁRIO DO SISTEMA,
não para o desenvolvedor. Responder: qual ação do usuário dispara esta SP? O que muda no
sistema após sua execução? O que o usuário vê ou sente como resultado?

Exemplos:
- "Representa o momento em que o candidato confirma e envia definitivamente sua inscrição.
   Após a execução, a inscrição fica registrada como concluída e passa a aparecer para os
   operadores na fila de análise."
- "Realiza o cancelamento de uma inscrição mediante solicitação do candidato. O sistema
   verifica se o prazo de cancelamento ainda está vigente antes de executar."
- "Calcula e consolida o tempo de serviço acumulado do servidor considerando todos os
   vínculos funcionais, utilizado para validação de elegibilidade em concursos.">

#### O que faz (técnico)

<Narrativa técnica em linguagem natural: o que a SP executa internamente. 2–6 linhas.>

#### Regras de negócio identificadas

> Regras que a SP verifica ou impõe — incluindo **qualquer filtro ou condição SQL que restrinja
> os dados retornados ou processados**. Filtros SQL são frequentemente regras de negócio
> invisíveis: `WHERE ativo = 1` significa "somente registros ativos são considerados" — isso
> é uma regra de negócio, não um detalhe técnico.
>
> **Fontes obrigatórias de regras a inspecionar:**
> - `IF` / `CASE` / `RAISERROR` / `THROW` — validações explícitas e rejeições
> - `WHERE <coluna> = <valor>` — restrições de escopo (ex.: só ativos, só do tipo X)
> - `WHERE <coluna> IS NULL / IS NOT NULL` — restrições de estado (ex.: só sem data de encerramento)
> - `WHERE <coluna> >= GETDATE()` — restrições temporais (ex.: só vigentes, só futuros)
> - `TOP 1` / `ORDER BY <coluna> DESC` — regra de seleção do registro mais recente/prioritário
> - `JOIN ... ON ... AND <condição extra>` — condição de vínculo com restrição de negócio
> - `HAVING` — regra de agregação com filtro de negócio
>
> **Regra de escrita:** nunca registrar o filtro SQL como descrição — sempre traduzir para
> o que o negócio impõe. Exemplos:
>
> | ❌ Técnico (proibido) | ✅ Negócio (obrigatório) |
> |---|---|
> | `WHERE ativo = 1` | Somente linhas de ônibus marcadas como ativas são retornadas. Linhas inativas ou suspensas são excluídas automaticamente. |
> | `WHERE data_fim IS NULL` | Somente vínculos funcionais ainda em vigor são considerados no cálculo. Vínculos encerrados são ignorados. |
> | `WHERE tipo = 'P' AND status = 'A'` | Somente inscrições do tipo Principal com status Ativo participam do processo. |
> | `TOP 1 ORDER BY data DESC` | O sistema considera apenas o registro mais recente, ignorando histórico anterior. |

| ID sugerido | Enunciado em linguagem de negócio | Origem na SP | Efeito / impacto |
|---|---|---|---|
| RN-SP-<NomeSP>-01 | <enunciado sem código — o que o negócio restringe ou impõe> | <tipo: filtro WHERE / validação IF / rejeição RAISERROR> | <o que muda para o usuário ou para os dados> |

> Se a SP é de leitura e não tem nenhum filtro restritivo: registrar "Sem restrições de negócio identificadas — retorna todos os registros do escopo informado."

#### Parâmetros de entrada

| Parâmetro | Tipo | Obrigatório | Significado de negócio |
|---|---|---|---|
| @NomeParam | tipo | Sim/Não | o que este parâmetro representa para o usuário |

#### O que retorna

| Campo / ResultSet | Tipo | Significado de negócio |
|---|---|---|
| campo ou resultado | tipo | o que representa para quem chamou |

> Se a SP não retorna nada (apenas efeito colateral): registrar "Sem retorno — apenas efeito no banco."

#### Tabelas envolvidas

| Tabela | Operação | O que faz nessa tabela |
|---|---|---|
| NOME_TABELA | SELECT / INSERT / UPDATE / DELETE | o que lê ou modifica em linguagem de negócio |

#### Lógica principal (resumo por bloco)

> Usar quando o corpo tiver > 20 linhas. Descrever os blocos sequencialmente em linguagem natural.
> Destacar as validações de negócio com prefixo **[Regra]** para facilitar extração.
>
> Exemplo:
> 1. **[Regra]** Verifica se a inscrição ainda está dentro do prazo de cancelamento — se não, rejeita.
> 2. Localiza a inscrição do candidato pelo identificador informado.
> 3. Atualiza o status da inscrição para "Cancelada".
> 4. Registra o histórico de cancelamento com data e motivo.
> 5. Retorna confirmação da operação.

#### Telas que usam

| Código | Tela / Controller | Rota / Endpoint | Contexto de uso |
|---|---|---|---|
| T001 | `InscricaoController` | `POST /inscricoes/cancelar` | Acionada quando o candidato solicita cancelamento |

#### Fluxos que usam

| Fluxo | Arquivo | Passo onde é usada |
|---|---|---|
| Cancelamento de Inscrição | `FLUXO-F003-cancelamento-inscricao.md` | Passo 4 — efetivação do cancelamento |
```

---

## Formato de Ficha para Jobs Hangfire (linguagem natural)

```markdown
### Job: `<nome_ou_classe>` · Hangfire

#### O que faz

<Narrativa descrevendo o que o job executa, quando é acionado e qual seu efeito no sistema.>

#### Agendamento

| Campo | Valor |
|---|---|
| Expressão cron | `0 */5 * * * ?` (a cada 5 minutos) |
| Fuso horário | `America/Sao_Paulo` |
| Estado atual | `WAITING` / `PROCESSING` / `FAILED` |
| Classe .NET | `NomeDoNamespace.NomeClasse` |

#### Fluxos que acionam ou dependem deste job

| Fluxo | Contexto |
|---|---|
| — | — |
```

---

## Tabela-resumo obrigatória no DADOS-10

O documento `DADOS-10` deve sempre conter uma tabela-resumo logo após o cabeçalho:

```markdown
| # | Objeto | Schema | Tipo | Descrição resumida | Ficha detalhada | Usada pelo sistema | Nível de documentação |
|---|---|---|---|---|---|---|---|
| 1 | USP_CO_FinalizarInscricao | dbo | PROCEDURE | Finaliza a inscrição gravando o candidato definitivamente | [ver seção 2.1](#usp_co_finalizarinscricao) | Sim | Completa |
| 2 | USP_CO_ExemploSP | dbo | PROCEDURE | — | — pendência | Sim (definição não localizada) | [PEN] |
| 3 | USP_SAFE_Relatorio | dbo | PROCEDURE | Sistema SAFE — fora do escopo | — | Não (sistema externo) | — |
```

A coluna **"Descrição resumida"** deve ter no mínimo uma frase completa em linguagem natural descrevendo o que a rotina faz — nunca deixar em branco nem usar só o nome da SP como descrição.

A coluna **"Nível de documentação"** indica o grau de completude da ficha e orienta qual skill usar em seguida:

| Valor | Significado | Como chegar lá |
|---|---|---|
| `Deep-dive` | Ficha completa com regras extraídas sistematicamente, árvore de chamadas e diagrama Mermaid | Executar `discovery - 13 - banco - sp-aprofundar` para esta SP |
| `Completa` | Ficha em linguagem natural com "O que representa" e "Regras de negócio identificadas" preenchidos | Esta skill (`discovery - 12 - banco - rotinas`) com corpo lido |
| `Resumida` | Apenas parâmetros e papel inferido pelo nome — corpo não lido ou não disponível | Esta skill sem acesso ao corpo |
| `[PEN]` | Ficha não gerada — SP usada pelo sistema mas definição não localizada | Obter o script e re-executar esta skill ou `discovery - 13 - banco - sp-aprofundar` |

> **Integração com `discovery - 30 - telas - documentar-tela`:** ao documentar uma TELA com SP de escrita crítica (INSERT/UPDATE em entidade principal), a skill de TELA verifica o nível de documentação. Se for `Resumida` ou `[PEN]`, sugere executar `discovery - 13 - banco - sp-aprofundar` antes de continuar. Fichas com nível `Completa` ou `Deep-dive` permitem gerar a Seção 8 (Regras de negócio) da TELA diretamente do DADOS-10.

---

## Regras de escrita em linguagem natural (obrigatórias)

1. **Sujeito ativo:** escrever "Esta procedure recebe X e retorna Y", não "Recebe X, retorna Y".
2. **Sem jargão técnico desnecessário:** preferir "grava o endereço do candidato" a "executa INSERT na tabela STD_ADDRESS".
3. **Mencionar o efeito no negócio:** além da operação técnica, descrever o impacto no processo. Ex.: "Ao ser chamada, marca a inscrição como concluída, tornando-a visível para os operadores."
4. **Incerteza explícita:** quando o corpo não estiver disponível, iniciar com "Com base no nome e na assinatura, presume-se que esta procedure..." e indicar ao final da seção "O que faz" que o comportamento não foi verificado diretamente."
5. **Não repetir o nome da SP:** a narrativa deve fluir como texto de documentação, não como eco do nome.
6. **Limite de tamanho:** a narrativa da seção "O que faz" deve ter entre 2 e 8 linhas. Se for maior, mover o excesso para "Lógica principal (resumo por bloco)".

---

## Seção "Consultas diagnósticas usadas"

Ao final do `DADOS-10`, incluir seção com as queries SQL executadas (sem referências externas):

```markdown
## N. Consultas diagnósticas usadas

### Listar functions e procedures (sys.objects)
```sql
<query aqui>
```

### Checagem cruzada (information_schema)
```sql
<query aqui>
```

### Triggers (sys.triggers)
```sql
<query aqui>
```

### Definição completa (sys.sql_modules)
```sql
<query aqui>
```

### Parâmetros (sys.parameters)
```sql
<query aqui>
```

### Jobs Hangfire
```sql
<query aqui>
```
```

---

## Restrições

- Não mencionar stack novo (API nova, microserviços) — este documento descreve apenas o legado.
- Não afirmar comportamento de SPs sem evidência (arquivo local, banco ou código legado) — indicar claramente quando a descrição é deduzida.
- Não alterar `DISC-*` neste passo; registrar apenas em `DADOS-10` e `SNAP-DADOS-10-*`.
- SPs com corpo > 100 linhas: resumir por bloco lógico na seção "Lógica principal" — nunca copiar o corpo SQL integralmente para o DADOS-10.
- Nunca misturar SQL de engines diferentes na mesma execução. Ler `database.engine` do `discovery-project.yml` e usar **apenas** o bloco correspondente.
- Registrar no documento gerado qual engine foi utilizado e qual fonte de definição foi usada (pasta local ou banco) como nota no cabeçalho.
- A coluna "Descrição resumida" da tabela-resumo é obrigatória — nunca deixar em branco.
- **Nunca criar ficha completa em linguagem natural para uma SP que não foi encontrada no código legado** — listá-la apenas na tabela-resumo como "Não utilizada pelo sistema / sistema externo".
- Se pasta local fornecida mas vazia ou inacessível: avisar o usuário e cair automaticamente para Caso B (banco via MCP).

---

## Execução no Cursor (MCP)

**Pré-requisito:** MCP configurado em `database.mcp_server` ativo e `discovery-project.yml` presente.

**Prompt — pasta local disponível:**
```
Regenere o DADOS-10 usando a pasta C:\caminho\para\sps como fonte das definições. Documente apenas as SPs usadas pelo sistema.
```

**Prompt — sem pasta local (banco via MCP):**
```
Regenere o DADOS-10 com 100% de cobertura de rotinas do schema dbo, incluindo fichas em linguagem natural para cada SP usada pelo sistema e referências cruzadas a telas e fluxos.
```

**Prompt para documentar uma SP específica:**
```
Documente a SP <nome_da_SP> em linguagem natural com ficha completa, incluindo telas e fluxos que a utilizam. O arquivo SQL está em <caminho>.
```

O agente lê esta SKILL.md, executa os passos 0 → 0b → 0c para determinar fonte e filtro, e grava os artefatos em `discovery/`.

**Regras de execução:**
- Sempre executar Passo 0 (ler `discovery-project.yml`), Passo 0b (detectar fonte) e Passo 0c (filtrar usadas) antes de qualquer leitura de definição
- Se pasta local disponível: usar Caso A (Passo 5 por arquivo); senão: Caso B (queries MCP)
- Executar apenas o bloco SQL correspondente ao engine (`database.engine`) quando usar banco
- Artefatos gerados em `paths.discovery`; estado vive em `DADOS-10` e `SNAP-DADOS-10-VALIDACAO`
- Para cada SP com ficha gerada: executar o Passo 6 (referências cruzadas) antes de finalizar a ficha

---

## Referências adicionais

- Para contexto dos documentos já gerados, ver `discovery/DISC-00-INDICE.md`
- Para catálogo de telas e endpoints, ver `discovery/TELA-CATALOGO.md` (se existir)
- Para fluxos documentados, ver arquivos `discovery/FLUXO-F*.md`
- **Queries avançadas de extração SQL Server** (árvore de dependências, referências inversas, busca textual): `.github/discoverytoolkit/references/sql/extraction-queries.md`

---

## Passo final — Atualizar o plano

Ao concluir a geração dos artefatos desta skill, **executar obrigatoriamente** a atualização do plano de discovery:

`
Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto
`

O plano re-inspeciona o estado real da pasta discovery/ e reflete os artefatos recém-gerados, desbloqueando automaticamente a próxima onda de execução.




