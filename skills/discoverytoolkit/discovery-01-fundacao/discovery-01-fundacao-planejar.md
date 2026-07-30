---
name: discovery-01-fundacao-planejar
description: Inspeciona o estado real do projeto (discovery-project.yml + pasta discovery/) e gera PLANO-DISCOVERY-YYYY-MM-DD.md com o plano em ondas, status de cada fase, alertas adaptativos e prompts prontos para executar. Aplica heurísticas sobre o que foi encontrado (volume de tabelas, SPs críticas, CFs priorizados, pendências abertas) para ajustar a sequência e emitir alertas. Use quando o usuário pedir para montar o plano de discovery, ver em que fase está, criar o roteiro de execução em ondas, ou diagnosticar o que falta no discovery.
---

# Discovery Planner — Plano em Ondas

## Responsabilidade

Inspecionar o estado real do projeto e produzir um **plano de execução em ondas** persistido em `discovery/PLANO-DISCOVERY-YYYY-MM-DD.md`.

Responde de forma rastreável: *"Em que fase estou? O que falta? Qual o próximo prompt exato?"*

**O que esta skill FAZ:**
- Lê `discovery-project.yml` para conhecer o projeto (stack, banco, paths)
- Lista os arquivos em `discovery/` e mapeia cada artefato à fase do GUIA
- Classifica cada fase como `COMPLETA`, `PARCIAL`, `PENDENTE` ou `BLOQUEADA`
- Identifica a próxima ação concreta com o prompt exato para execução
- Gera `PLANO-DISCOVERY-YYYY-MM-DD.md` — documento vivo, atualizado a cada execução
- Preserva o histórico de ondas concluídas ao re-executar (idempotente)

**O que esta skill NÃO FAZ:**
- Não executa outras skills automaticamente
- Não acessa o banco de dados
- Não altera artefatos existentes de discovery
- Não abre novos levantamentos nem cria FLUXOs ou TELAs

---

## Configuração do projeto

Ler `discovery-project.yml` antes de executar:

| Chave | Uso na skill |
|---|---|
| `project.name` | Nome do sistema — exibido no cabeçalho do plano |
| `paths.discovery` | Pasta com os artefatos de discovery |
| `paths.indices.legado` | Caminho de `arquivos-legado.txt` |
| `paths.indices.workspace` | Caminho de `arquivos-workspace.txt` |
| `database.mcp_server` | Nome do MCP — exibido no diagnóstico de Fase 0 |
| `database.schema_principal` | Schema principal — confirmação da Fase B |
| `stack.backend.framework` | Stack do backend — contextualiza análise de Fase C/E |

---

## Passo 1 — Diagnóstico do projeto

### 1.1 — Leitura do yml

Ler `discovery-project.yml` e extrair:
- Nome do projeto, sistema, stack backend, banco/schema, MCP server
- Paths de discovery, legado e índices

### 1.1.1 — Geração automática dos índices

Se algum dos arquivos de índice (`arquivos-legado.txt` ou `arquivos-workspace.txt`) não existir, gere automaticamente usando:

No Windows:
```
tree /f > caminho/do/arquivo.txt
```
Exemplo:
```
tree /f > discovery/arquivos-legado.txt
```
No Linux/Mac:
```
find . -type f > caminho/do/arquivo.txt
```
Adapte o caminho conforme o índice desejado. Isso garante que as skills sempre terão um inventário mínimo dos arquivos do projeto.

### 1.2 — Inventário de artefatos

Listar todos os arquivos em `{paths.discovery}/` (sem subpastas de evidência).

Para cada arquivo encontrado, registrar:
- Nome do arquivo
- Tamanho aproximado (em KB, ou "vazio" se < 1 KB)
- Fase à qual pertence (tabela de mapeamento abaixo)

**Tabela de mapeamento artefato → fase:**

| Artefato | Fase | Obrigatório |
|---|---|---|
| `discovery-project.yml` (no .cursor/) | 0 | Sim |
| `arquivos-legado.txt` | A | Sim |
| `arquivos-workspace.txt` | A | Sim |
| `DISC-90-PENDENCIAS.md` | A (e contínuo) | Sim |
| `DADOS-05-MAPA-DADOS.md` | B | Sim |
| `DADOS-06-STATUS-E-TRANSICOES.md` | B | Sim |
| `DADOS-09-*.md` (qualquer) | B | Sim |
| `DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` | B | Sim |
| `DISC-04-CATALOGO-CODIGO-LEGADO.md` | C | Sim |
| `TELA-CATALOGO.md` | C | Sim |
| `DISC-03-CATALOGO-DE-FLUXOS.md` | D | Sim |
| `DISC-03A-FILA-MANUAL-FLUXOS-CORE.md` | D | Opcional (recomendado quando houver curadoria de negócio) |
| `SNAP-INVENTARIO-FLUXOS.md` | D | Sim |
| `TELA-*.md` (exceto `TELA-CATALOGO.md`) | D | Cobertura em lote das telas priorizadas |
| `FLUXO-F*.md` | E | Um por CF da fila |
| `SNAP-CONSOLIDACAO-*.md` | F | Sim |
| `DISC-06-MODERNIZACAO.md` | F | Opcional |
| `DISC-07-INDICE-DE-ROTEAMENTO-TECNICO.md` | F (pós-consolidação) | Opcional |
| `DISC-08-INDICE-REVERSO-OBJETOS-TECNICOS.md` | F (pós-consolidação) | Opcional |
| `PLANO-DISCOVERY-*.md` | Meta | Gerado por esta skill |

> Artefatos com tamanho < 1 KB são tratados como "presentes mas vazios" — não contam como completos.

---

## Passo 2 — Classificação por fase

Para cada fase, determinar o status:

| Status | Critério |
|---|---|
| `COMPLETA` | Todos os artefatos obrigatórios da fase existem e têm tamanho > 1 KB |
| `PARCIAL` | Alguns artefatos obrigatórios existem; outros faltam ou estão vazios |
| `PENDENTE` | Nenhum artefato da fase existe |
| `BLOQUEADA` | Fase anterior está PENDENTE ou PARCIAL (pré-requisito não cumprido) |

**Regras de bloqueio por fase:**

| Fase | Bloqueada se |
|---|---|
| A | Fase 0 não tem `discovery-project.yml` preenchido |
| B | Fase A PENDENTE (sem índices) |
| C | Fase A PENDENTE (sem `arquivos-legado.txt`) |
| D | Fase B PENDENTE, ou Fase C PARCIAL/PENDENTE |
| E | Fase D PARCIAL/PENDENTE (sem catálogo de fluxos DISC-03, inventário básico e lote de TELAs detalhadas) |
| F | Fase E sem nenhum `FLUXO-F*.md` |

### Avaliação especial da Fase E

A Fase E é iterativa. Para cada CF na fila do `DISC-03`, verificar:
- Existe `FLUXO-F*.md` correspondente com tamanho > 5 KB?

Produzir uma tabela de cobertura da Fase E com **todos os CFs** da fila (não truncar):
```
CF-001 → FLUXO-F001 [COMPLETO]
CF-002 → FLUXO-F002 [COMPLETO]
CF-003 → [PENDENTE]
CF-004 → [PENDENTE]
... (um por linha para cada CF do DISC-03)
```

> Esta tabela alimenta diretamente as ondas expandidas no Passo 3 — cada linha aqui corresponde a uma onda no documento.

---

## Passo 2-B — Adaptações inteligentes do plano

> Este passo é executado **depois** da classificação por fase e **antes** de gerar o documento.
> Aplica heurísticas sobre o que foi encontrado para ajustar a sequência e emitir alertas.
> Nunca especula — só adapta com base em evidências reais dos artefatos já existentes.

### Heurísticas por artefato disponível

#### Após DADOS-05 (snapshot do banco) estar disponível

Contar tabelas documentadas no arquivo. Aplicar:

| Condição | Adaptação |
|---|---|
| Banco com 100+ tabelas | Inserir alerta na Onda 1: "Volume alto — executar B.3 (rotinas) em contexto próprio antes de C.1" |
| Banco com schemas adicionais além do principal (ex.: hangfire, dashboard) | Registrar nota: "Schemas adicionais detectados no yml — verificar se precisam de documentação separada" |

#### Após DADOS-10 (rotinas) estar disponível

Contar SPs, functions e triggers no arquivo. Aplicar:

| Condição | Adaptação |
|---|---|
| Mais de 20 SPs | Inserir recomendação nas Ondas 2..N: "Priorizar E.3 (deep-dive) antes de E.4 (TELA) para fluxos com SPs críticas" |
| Triggers presentes | Inserir alerta: "Triggers identificadas — verificar se impactam status das tabelas do DISC-06" |
| SPs com nível `Resumida` ou `[PEN]` | Listar nominalmente na onda correspondente: "Deep-dive pendente antes de documentar TELAs que as chamam" |

#### Após DISC-03 (catálogo de fluxos) estar disponível

Ler a fila de CFs com prioridade. Aplicar:

| Condição | Adaptação |
|---|---|
| CFs com prioridade ALTA | Posicionar primeiro nas Ondas 2..N |
| CF com 5+ tabelas ou SPs críticas | Marcar como "complexo — reservar contexto limpo" |
| CF sem nenhuma tabela identificada | Marcar como "simples — pode ser feito junto com o anterior se for pequeno" |
| Mais de 10 CFs na fila | Inserir recomendação: "Priorize os N CFs ALTA antes de avançar para MÉDIA" |

#### Após DISC-03A (fila manual de fluxos core) estar disponível

Ler `DISC-03A-FILA-MANUAL-FLUXOS-CORE.md` e aplicar:

| Condição | Adaptação |
|---|---|
| Itens manuais com prioridade ALTA | Inserir no topo da próxima onda de FLUXO com marcação `Origem: usuário` |
| Item manual sem evidência mínima (tela/tabela/SP/log/perfil) | Inserir alerta: "Curadoria sem evidência mínima — validar antes de gerar FLUXO" |
| Item manual já coberto por CF do DISC-03 | Marcar como "sobreposição" e evitar duplicidade de onda |

#### Após DISC-90 (pendências) estar disponível

Contar pendências abertas por severidade. Aplicar:

| Condição | Adaptação |
|---|---|
| Pendências CRITICA abertas | Inserir bloco de alerta no início do plano: "X pendências CRÍTICAS abertas — resolver antes de avançar para próxima onda" |
| Pendências acumuladas > 20 abertas | Recomendar executar `discovery - 50 - consolidacao - pendencias` antes de iniciar nova onda |
| Pendências concentradas em uma tabela ou SP | Associar à onda correspondente do CF que usa esse artefato |

#### Após FLUXOs (FLUXO-F*.md) estarem disponíveis

Para cada FLUXO existente, verificar tamanho e seções. Aplicar:

| Condição | Adaptação |
|---|---|
| FLUXO com menos de 5 KB | Marcar como "raso — considerar refinamento antes de documentar TELAs" |
| FLUXO sem `SNAP-REVALIDACAO` | Marcar E.2 como pendente antes de avançar para E.4 |
| FLUXO sem nenhuma `TELA-[0-9]*.md` associada | Marcar E.4 como pendente para aquele CF |
| SP mencionada em 3+ FLUXOs | Inserir sugestão: "SP {nome} é transversal — deep-dive beneficia múltiplos fluxos; priorizar" |

### Formato dos alertas no plano

Os alertas gerados por esta etapa são inseridos em três locais do documento:

1. **Bloco `## Alertas e recomendações`** — no topo do plano, logo após a tabela de status geral
2. **Dentro da onda afetada** — como `> ⚠️ Adaptação: {motivo}` antes do critério de conclusão
3. **Na referência rápida** — ordem dos prompts ajustada conforme as adaptações

### Proibições desta etapa

- **NUNCA reordenar** fases obrigatórias (A → B → C → D é sempre essa ordem)
- **NUNCA omitir** uma onda por julgá-la desnecessária — apenas marcar como "simples" ou "complexa"
- **NUNCA inventar** CFs, SPs ou tabelas que não estejam nos artefatos lidos
- **NUNCA atrasar** a Onda Final por conta de CFs de prioridade BAIXA ainda pendentes — registrar como gap, não bloqueio

---

## Passo 3 — Gerar o plano em ondas

### Estrutura do documento de saída

Arquivo: `{paths.discovery}/PLANO-DISCOVERY-YYYY-MM-DD.md`

```markdown
---
Tipo: Plano
Código: PLANO
Nome: Plano de Discovery em Ondas
Módulo: Meta
Criticidade: ALTA
Tags: plano, ondas, sequência, roadmap
Escopo: discovery completo
Relacionados: DISC-00-INDICE.md, DISC-03-CATALOGO-DE-FLUXOS.md
Última atualização: YYYY-MM-DD
Palavras-chave do domínio: plano, fases, ondas, sequência
---

# Plano de Discovery — {project.name}

> Gerado em: YYYY-MM-DD | Skill: discovery - 01 - fundacao - planejar
> Stack: {stack.backend.framework} | Banco: {database.engine} / schema {database.schema_principal}

## Status geral

| Fase | Artefatos esperados | Encontrados | Status |
|---|---|---|---|
| 0 — Configuração | discovery-project.yml | N | STATUS |
| A — Infraestrutura | arquivos-legado.txt, arquivos-workspace.txt, DISC-90 | N | STATUS |
| B — Banco | DADOS-05, DADOS-06, DADOS-10 | N | STATUS |
| C — Código legado | DISC-04, TELA-CATALOGO | N | STATUS |
| D — Catálogos | DISC-03, SNAP-INVENTARIO-FLUXOS | N | STATUS |
| E — FLUXOs | N CFs na fila / N FLUXOs / N TELAs | N | STATUS |
| F — Consolidação | SNAP-CONSOLIDACAO, DISC-90 final | N | STATUS |

**Fase atual:** {fase com PARCIAL mais avançada ou a primeira PENDENTE}
**Próxima ação:** {prompt exato — ver Onda correspondente abaixo}

---

## Alertas e recomendações

> Gerados automaticamente pela análise dos artefatos encontrados. Baseados apenas em evidências reais.

{lista de alertas gerados pelo Passo 2-B — vazia se nenhuma condição foi acionada}

---

## Ondas de execução

### Onda 0 — Base *(STATUS)*

**Inclui:** Fases 0 + A + B
**Objetivo:** Configurar o ambiente, indexar os arquivos e documentar o banco como âncora estrutural.

#### Artefatos
| Artefato | Status | Observação |
|---|---|---|
| discovery-project.yml | [OK / FALTA] | |
| arquivos-legado.txt | [OK / FALTA] | N linhas |
| arquivos-workspace.txt | [OK / FALTA] | N linhas |
| DADOS-05-MAPA-DADOS.md | [OK / FALTA] | N tabelas documentadas |
| DADOS-06-STATUS-E-TRANSICOES.md | [OK / FALTA] | |
| DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md | [OK / FALTA] | N rotinas |

#### Próxima ação
> Se status COMPLETA: nenhuma — avançar para Onda 1
> Se PARCIAL/PENDENTE: prompt exato do passo pendente

```
{prompt exato para o próximo passo não concluído da Onda 0}
```

#### Critério de conclusão
- [ ] Todos os artefatos acima com status OK e tamanho > 1 KB
- [ ] DISC-90 atualizado após Fase B
- [ ] **Atualizar o plano:** `Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto`

---

### Onda 1 — Estrutura *(STATUS)*

**Inclui:** Fase C
**Objetivo:** Mapear o código legado e consolidar o catálogo estrutural de telas/controllers.

#### Artefatos
| Artefato | Status | Observação |
|---|---|---|
| DISC-04-CATALOGO-CODIGO-LEGADO.md | [OK / FALTA] | N módulos / N controllers |
| TELA-CATALOGO.md | [OK / FALTA] | N artefatos de tela |

#### Próxima ação
```
{prompt exato para o próximo passo não concluído da Onda 1}
```

#### Critério de conclusão
- [ ] DISC-04 existe com mapa de módulos
- [ ] TELA-CATALOGO.md existe com lista de artefatos agrupados por módulo
- [ ] O catálogo de telas foi gerado antes de qualquer FLUXO
- [ ] DISC-90 atualizado
- [ ] **Atualizar o plano:** `Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto`

---

### Onda 2 — Telas detalhadas *(STATUS)*

**Inclui:** Fase D
**Objetivo:** Gerar catálogo de fluxos e concluir o lote de TELAs detalhadas prioritárias antes da produção de FLUXOs.

#### Artefatos
| Artefato | Status | Observação |
|---|---|---|
| DISC-03-CATALOGO-DE-FLUXOS.md | [OK / FALTA] | N CFs na fila |
| DISC-03A-FILA-MANUAL-FLUXOS-CORE.md | [OK / OPCIONAL] | N itens manuais (quando houver) |
| SNAP-INVENTARIO-FLUXOS.md | [OK / FALTA] | |
| TELA-*.md (exceto TELA-CATALOGO) | [OK / FALTA] | N telas detalhadas |

#### Próxima ação
```
{prompt exato para o próximo passo não concluído da Onda 2}
```

#### Critério de conclusão
- [ ] DISC-03 existe com fila de CFs priorizados
- [ ] SNAP-INVENTARIO-FLUXOS existe
- [ ] TELAs detalhadas prioritárias do TELA-CATALOGO foram produzidas
- [ ] DISC-90 atualizado

---

### Ondas 3..N — Fluxos *(uma onda numerada por CF da fila)*

**Inclui:** Fase E (ciclo por CF)
**Objetivo:** Documentar cada fluxo com FLUXOs industriais + TELAs associadas.

> **REGRA DE EXPANSÃO OBRIGATÓRIA:** Quando `DISC-03` estiver disponível, o plano gerado deve conter **uma seção de onda numerada para cada CF da fila**, mesmo na primeira execução. Não usar tabela resumida como substituto. Cada onda recebe número sequencial (Onda 2, Onda 3, Onda 4 …) e conteúdo completo conforme o template abaixo. CFs ainda não iniciados recebem status `🔵 PENDENTE`.

> **REGRA DE AGRUPAMENTO:** CFs classificados como "Simples" no DISC-03 podem ser agrupados em uma mesma onda (ex.: "Onda 7 — CF-005 + CF-009") quando ambos não tiverem SPs críticas pendentes de deep-dive e o FLUXO de cada um for estimado como de baixa complexidade. Registrar o motivo do agrupamento em nota.

Para cada CF na fila do DISC-03, gerar uma subseção com o template abaixo:

---

#### Onda {N} — CF-{NNN}: {nome do fluxo} *({STATUS})*

**Inclui:** Fase E — ciclo CF-{NNN}
**Prioridade:** {prioridade do CF no DISC-03}
**Complexidade estimada:** {Simples / Média / Complexa — com base no número de tabelas/SPs no DISC-03}

> ⚠️ Adaptação: {inserir nota se houver SP transversal, pendência crítica que bloqueia, ou CF dependente de onda anterior — omitir se não houver}

| Artefato | Status | Observação |
|---|---|---|
| FLUXO-F{NNN}-*.md | [✅ OK / 🔵 FALTA] | {N seções se existir; "Aguardando onda anterior" se bloqueado} |
| Pendências revalidadas (SNAP-REVALIDACAO) | [✅ OK / 🔵 FALTA] | |
| SPs com deep-dive (DADOS-10) | [✅ OK / 🔵 FALTA / N/A] | {listar SPs sem deep-dive se houver} |

**Próxima ação:**

```
{prompt exato: "Gere o FLUXO-F{NNN} em modo industrial a partir do CF-{NNN}" se pendente; ou prompt de revalidação/deep-dive se em andamento; ou "nenhuma — CF concluído" se completo}
```

**Ao concluir este CF — obrigatório:**
```
Consolide as pendências e atualize o DISC-90
```
```
Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto
```

---

### Onda Final — Consolidação *(STATUS)*

**Inclui:** F.1 + F.2 (obrigatórios) + F.3 (opcional)

| Artefato | Status | Observação |
|---|---|---|
| SNAP-CONSOLIDACAO-*.md (Passo 10) | [OK / FALTA] | |
| DISC-90-PENDENCIAS.md (final) | [OK / FALTA] | N pendências abertas |
| discovery-html/ (F.3-A — OPCIONAL) | [OK / FALTA / Não executado] | |
| Pacote NotebookLM (F.3-B — OPCIONAL) | [OK / FALTA / Não executado] | |

**Próxima ação:**
```
{prompt exato para F.1 ou F.2, conforme o que faltar}
```

#### Critério de conclusão
- [ ] SNAP-CONSOLIDACAO-*.md existe
- [ ] DISC-90 com pendências atualizadas
- [ ] F.3 é opcional — executar se necessário para compartilhamento
- [ ] **Atualizar o plano (estado final):** `Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto`

---

## Referência rápida — prompts por passo

| Passo | Prompt |
|---|---|
| A.1 Índices | `Gere os índices de arquivos do projeto` |
| B.1 Snapshot banco | `Extraia o snapshot de tabelas e colunas do schema principal` |
| B.2 Status | `Mapeie os status e transições do schema principal` |
| B.3 Rotinas | `Regenere o DADOS-10 com 100% de cobertura de rotinas do schema principal` |
| C.1 Legado | `Execute a varredura estrutural do legado e gere o catálogo DISC-04` |
| C.2 Telas | `Execute o Passo C.2 do ritual — gere o catálogo de telas/controllers do legado` |
| D.1 Fluxos candidatos | `Execute o Passo 6 do ritual — gere o catálogo de fluxos candidatos a partir do banco` |
| D.2 Inventário | `Inventarie os FLUXOs existentes e gere o SNAP-INVENTARIO-FLUXOS` |
| D.3 TELAs detalhadas | `Leia .github/skill/discoverytoolkit/discovery - 30 - telas - documentar-tela/SKILL.md e documente o artefato {NomeArquivo}` |
| E.1 FLUXO | `Gere o FLUXO-F{NNN} em modo industrial a partir do CF-{NNN}` |
| E.2 Revalidar | `Revalide as pendências do FLUXO-F{NNN}` |
| E.3 Deep-dive SP | `Faça deep-dive completo da SP {NOME_SP}` |
| [PEN] Pendências | `Consolide as pendências e atualize o DISC-90` |
| F.1 Consolidação | `Execute o Passo 10 — consolidação global do discovery` |
| F.2 Pendências finais | `Consolide as pendências e atualize o DISC-90` |
| F.3-A HTML | `Gere o site HTML do discovery` |
| F.3-B NotebookLM | `Empacote o discovery para o NotebookLM excluindo fluxos suspeitos` |
| Remontar plano | `Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto` |
```

---

## Passo 4 — Regras de geração do documento

### Leitura do DISC-03 para a fila de CFs

Se `DISC-03-CATALOGO-DE-FLUXOS.md` existir:
1. Identificar a lista completa de CFs (CF-001, CF-002, …) com nome, prioridade e complexidade
2. **Para cada CF, gerar uma onda numerada dedicada** no documento de saída (ver template no Passo 3) — nunca substituir por tabela resumida
3. Para cada CF, verificar se existe `FLUXO-F*.md` correspondente e preencher status real
4. Verificar se existe `SNAP-REVALIDACAO-F*.md` (pendências revalidadas)
5. Verificar TELAs associadas: buscar em `TELA-[0-9]*.md` referências ao código do CF
6. CFs simples sem dependência bloqueante podem ser agrupados em uma mesma onda — registrar motivo
7. A numeração das ondas é sequencial: Onda 0 (Base), Onda 1 (Estrutura), Onda 2..N (um CF ou par de CFs simples por onda), Onda Final (Consolidação)

**Regra de precedência obrigatória:** se `TELA-CATALOGO.md` não existir, a Onda 1 permanece PARCIAL e a Onda 2 deve ser marcada como BLOQUEADA, mesmo que `DISC-03` já exista.

Se `DISC-03` não existir: registrar Onda 2 como BLOQUEADA (aguardando Onda 1) — **não gerar ondas de fluxo sem a fila real**.

### Leitura do DADOS-10 para status de SPs

Se `DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` existir:
1. Contar SPs com `Nível de documentação: Deep-dive` ou `Completa`
2. Contar SPs com `Nível de documentação: Resumida` ou `[PEN]`
3. Registrar nas ondas de Fase E quais TELAs têm SPs sem deep-dive

### Comportamento idempotente

Se `PLANO-DISCOVERY-*.md` já existir:
- Criar novo arquivo com data de hoje
- Na seção de cada onda já COMPLETA, manter o status e adicionar linha "Concluída em: YYYY-MM-DD"
- Não apagar nem sobrescrever o arquivo anterior — ele vira histórico em `discovery/_historico/PLANOS/` se essa pasta existir

### Proibições

- **NUNCA inventar** artefatos que não foram encontrados em `discovery/`
- **NUNCA afirmar** que uma fase está completa sem verificar tamanho de cada arquivo
- **NUNCA consultar** o banco de dados — apenas o sistema de arquivos e o yml
- **NUNCA criar** FLUXOs, TELAs ou DADOS como efeito colateral desta skill

---

## Passo 5 — Relatório final ao usuário

Após gerar o arquivo, apresentar ao usuário:

```
PLANO-DISCOVERY-YYYY-MM-DD.md criado em {paths.discovery}/

DIAGNÓSTICO ATUAL
─────────────────
Fase 0 (Configuração):  STATUS
Fase A (Infraestrutura): STATUS
Fase B (Banco):          STATUS
Fase C (Código legado):  STATUS
Fase D (Catálogos):      STATUS
Fase E (FLUXOs):         N/M CFs completos  (N TELAs criadas)
Fase F (Consolidação):   STATUS

PRÓXIMO PASSO
─────────────
{nome do passo} — copie e execute:

"{prompt exato}"

Para remontar o plano a qualquer momento:
"Leia .github/skill/discoverytoolkit/discovery - 01 - fundacao - planejar/SKILL.md e atualize o plano de discovery deste projeto"
```



