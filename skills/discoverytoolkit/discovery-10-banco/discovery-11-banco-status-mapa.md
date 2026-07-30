---
name: discovery-11-banco-status-mapa
description: Mapeia status, transições e enums do schema principal do projeto ativo (engine e schema lidos de discovery-project.yml) e gera ou atualiza DADOS-06 e DADOS-09 em discovery/. Use quando o usuário pedir para mapear status de solicitação, transições de estado, enums do banco, ciclo de vida de atendimentos, ou quando precisar entender quais valores de status existem no schema principal.
---

# Discovery DB Status Map

> **Antes de qualquer ação:** ler `discovery-project.yml` e extrair `database.engine`, `database.schema_principal` e `database.mcp_server`.
> Executar **apenas** o bloco SQL correspondente ao `database.engine` configurado.
> Schema a usar em todas as queries: valor de `database.schema_principal` (ex.: `public` para PostgreSQL, `dbo` para SQL Server).
> MCP a usar: valor de `database.mcp_server` em `discovery-project.yml`.

## Responsabilidade

Mapear com evidência do banco (`schema dbo`, SQL Server):

- Valores de status armazenados em tabelas e colunas
- Transições permitidas (se registradas no DDL, triggers ou tabelas de configuração)
- Enums, lookups e tabelas de domínio relacionados a estados

## Rótulos obrigatórios

| Rótulo | Quando usar |
|---|---|
| `` | Valor extraído diretamente via query ou DDL do schema principal (conforme `database.schema_principal` no yml) |
| `` | Enum ou constante extraída do código legado (`paths.legado` no yml) |
| `` | Conclusão sobre significado de status a partir de nomes/comentários — sem confirmação direta |
| `[PEN]` | Status sem descrição clara ou transição sem evidência — sempre incluir "como confirmar" |

**Se precisar inferir, sempre declarar explicitamente com `` e justificativa.**

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `discovery/DADOS-06-STATUS-E-TRANSICOES.md` | Mapa completo de status por entidade/tabela |
| `discovery/DADOS-09-MAPA-FLUXO-TABELAS.md` | Relacionamento entre fluxos e tabelas de status |

Atualizar `DADOS-06` para adições/correções de status. Atualizar `DADOS-09` quando houver correlação com fluxos documentados em `FLUXO-*`.

## Fontes de extração (em ordem de prioridade)

1. **Queries ao banco** (engine e schema configurados em `discovery-project.yml`): colunas de status, tabelas de lookup, comentários de coluna/tabela
2. **DDL e scripts SQL** no legado (localizar via `discovery/arquivos-legado.txt`)
3. **Código legado** (`paths.legado` de `discovery-project.yml`): enums, constantes e lógica de transição — ler o caminho do arquivo de configuração, nunca hardcodar

## Fluxo de trabalho

1. **Identificar entidade-alvo**: perguntar ao usuário qual entidade/módulo (ex.: processo, requerimento, benefício).
2. **Localizar coluna de status**: buscar por `status`, `situacao`, `cod_situacao`, `tp_situacao` na tabela.
3. **Extrair valores distintos**: via query `SELECT DISTINCT status FROM tabela` ou leitura de DDL/enum.
4. **Mapear significados**: usar comentários do banco; se ausentes, buscar no código legado.
5. **Identificar transições**: verificar triggers, procedures ou tabelas de histórico/log de transição.
6. **Rotular cada elemento** com nível de confiança.
7. **Registrar pendências**: status sem descrição → `[PEN]` com query sugerida.
8. **Gravar em `DADOS-06`** (e `DADOS-09` se houver correlação de fluxo).

## Formato de saída (por entidade)

```markdown
### Entidade: `nome_tabela` — Coluna: `coluna_status`

| Valor | Descrição | Nível de confiança | Transições conhecidas |
|---|---|---|---|
| `PENDENTE` | Aguardando análise | | → `EM_ANALISE` |
| `APROVADO` | Processo deferido | | — |
| `XX` | Significado desconhecido | [PEN] — executar: `SELECT * FROM tabela WHERE status = 'XX'` | — |
```

## Restrições

- Foco exclusivo em evidência do banco (schema configurado em `database.schema_principal`) e legado.
- Não documentar status da API nova ou endpoints do novo stack.
- Não alterar `DISC-*` ou `FLUXO-*` neste passo; registrar somente em `DADOS-06` e `DADOS-09`.
- Não remover `[PEN]` sem evidência concreta substituindo-a.

---

## Execução no Cursor (MCP)

**Pré-requisito:** MCP configurado em `database.mcp_server` (de `discovery-project.yml`) ativo.

**Prompt padrão:**
```
Mapeie os status e transições do schema principal do projeto
```

O agente lê esta SKILL.md, consulta o banco via MCP e grava os artefatos em `discovery/`.

**Regras de execução:**
- Sempre ler `discovery-project.yml` antes de qualquer query
- Executar apenas o bloco SQL correspondente ao engine (`database.engine`)
- Artefatos gerados em `paths.discovery`; estado vive em `DADOS-06` e `DADOS-09`

---

## Referências adicionais

- Para contexto dos DADOS e FLUXO já documentados, ver [references/REFERENCE.md](references/REFERENCE.md)

---

## Passo final — Atualizar o plano

Ao concluir a geração dos artefatos desta skill, **executar obrigatoriamente** a atualização do plano de discovery:

`
Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto
`

O plano re-inspeciona o estado real da pasta discovery/ e reflete os artefatos recém-gerados, desbloqueando automaticamente a próxima onda de execução.


