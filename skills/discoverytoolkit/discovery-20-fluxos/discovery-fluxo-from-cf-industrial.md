---
name: discovery-fluxo-from-cf-industrial
description: [LEGACY] Skill mantida como base metodológica rica. Para uso operacional atual, preferir discovery-20-fluxos-gerar, que aplica a mesma linha de documentação em pipeline catálogo -> gerar e reforça origem do fluxo, UML, plano de testes e validação humana.
---

# Discovery — Fluxo Industrial a partir de CF

> **Legado:** para novas execuções operacionais no toolkit, preferir `discovery-20-fluxos-gerar`.

## Público-alvo da documentação gerada

A documentação produzida por esta skill será consumida por:

- Analistas de Negócio e Analistas de Sistema
- Product Owners e Arquitetos
- Equipe de Modernização
- NotebookLM (indexação semântica)

**Padrão de linguagem obrigatório:** claro, objetivo, rastreável. Sem narrativa vaga, sem linguagem opinativa, sem proposta de melhoria, sem interpretação de intenção do negócio sem evidência.

---

## Parâmetros obrigatórios

| Parâmetro | Exemplo | Descrição |
|---|---|---|
| `fluxo_codigo` | `F001` | Código do fluxo de saída (Fxxx) |
| `cf_codigo` | `CF-001` | Identificador do Fluxo Candidato no DISC-03 |
| `versao_saida` | `v0.1` | Versão do documento gerado |
| `modo` | `gerar` | `gerar` · `refinar` · `gerar_e_refinar` |

Se algum parâmetro estiver ausente, solicitar ao usuário antes de prosseguir.

---

## Passo 1 — Leitura obrigatória das fontes

Ler **todos** os documentos abaixo antes de gerar qualquer conteúdo. Nenhuma seção pode ser preenchida sem esta leitura completa.

| Arquivo | Propósito |
|---|---|
| `discovery/DISC-97-PLANO-E-SEQUENCIA-DA-DESCOBERTA.md` | Contexto do plano e sequência de discovery |
| `discovery/DISC-99-METODOLOGIA-E-ARQUITETURA-DO-DISCOVERY.md` | Regras metodológicas e padrões canônicos |
| `discovery/DISC-02-PERFIS-PERMISSOES.md` | Perfis de usuário — base para preencher "Quem usa" |
| `discovery/DISC-03-CATALOGO-DE-FLUXOS.md` | Localizar o CF alvo e extrair evidências estruturais |
| `discovery/DADOS-06-STATUS-E-TRANSICOES.md` | Status e transições mapeados do schema do sistema |
| `discovery/DADOS-09-MAPA-FLUXO-TABELAS.md` | Mapa de tabelas por fluxo |
| `discovery/arquivos-legado.txt` | Índice de arquivos do código legado |

Se algum arquivo não existir, registrar como `[PEN]` no snapshot e prosseguir com o que estiver disponível. Nunca inventar conteúdo para compensar arquivo ausente.

---

## Passo 2 — Verificar existência do arquivo de saída

### 2.1 — Regra de nome do arquivo de saída

O arquivo de saída do fluxo é **sempre**:

```
discovery/FLUXO-<fluxo_codigo>-<slug>.md
```

**Proibido** gerar arquivos com sufixo de versão (`-v2`, `-v3`, etc.) na pasta `discovery/`. O arquivo corrente não carrega versão no nome — nunca.

### 2.2 — Ação conforme existência e modo

Verificar se `discovery/FLUXO-<fluxo_codigo>-<slug>.md` já existe.

**Se não existir:** prosseguir normalmente (modo `gerar`) — criar o arquivo.

**Se já existir:**

| Modo | Ação obrigatória |
|---|---|
| `gerar` | 1. Copiar o arquivo corrente para `discovery/_historico/FLUXOS/` (ver 2.3). 2. Sobrescrever `discovery/FLUXO-<fluxo_codigo>-<slug>.md` com o novo conteúdo. |
| `refinar` | 1. Copiar o arquivo corrente para `discovery/_historico/FLUXOS/` (ver 2.3). 2. Editar o arquivo corrente, preservando conteúdo anterior e adicionando/atualizando seções. |
| `gerar_e_refinar` | 1. Copiar o arquivo corrente para `discovery/_historico/FLUXOS/` (ver 2.3). 2. Sobrescrever o arquivo corrente e refinar em seguida. |

### 2.3 — Criar cópia de histórico antes de alterar

Antes de qualquer alteração no arquivo corrente existente, criar uma cópia em:

```
discovery/_historico/FLUXOS/FLUXO-<fluxo_codigo>-<slug>-<YYYY-MM-DD-HHMM>.md
```

- `<YYYY-MM-DD-HHMM>` = data e hora correntes no formato `2026-02-19-1430`.
- Se a pasta `discovery/_historico/FLUXOS/` não existir, criá-la.
- **Nunca alterar** o arquivo de histórico após criá-lo — ele é imutável.

Registrar a ação de versionamento no snapshot (nome do arquivo histórico gerado).

---

## Passo 3 — Extrair dados do CF no DISC-03

Localizar a seção `### CF-<NNN>` no DISC-03 e extrair:

| Campo | Onde encontrar |
|---|---|
| Nome do fluxo | Linha `### CF-NNN — <Nome>` |
| Domínio de origem | `**Domínio de origem:**` |
| Rótulo de confiança | `**Rótulo de confiança:**` |
| Tabelas principais | Tabela `**Tabelas principais:**` |
| Status/situação | Tabela `**Status/situação relevantes:**` |
| Eventos observáveis | Lista `**Eventos observáveis no banco:**` |
| SQLs diagnósticas | Bloco `**SQLs diagnósticas:**` |

Derivar o slug: converter o nome do CF para kebab-case minúsculo sem acentos.
Ex.: `Registro de Solicitacao do Cidadao` → `registro-de-solicitacao-do-cidadao`
Ex.: `Encaminhamento e Acompanhamento` → `encaminhamento-e-acompanhamento`

---

## Passo 3-B — Validar colunas e valores de domínio via banco (obrigatório)

**Executar após o Passo 3 (extração do CF) e antes de iniciar a geração de qualquer seção do documento.**

Para cada tabela e coluna identificada no CF (DISC-03), em DADOS-06 ou DADOS-09, confirmar via banco antes de escrever.

### 3-B.1 — Confirmar existência das colunas

Para toda referência a `<TABELA>.<COLUNA>` nos dados do CF e nos documentos base, usar MCP `project-0-Gprev-app-previdenciario → describe_table(<TABELA>)`:

- **Se a coluna existir:** usar com evidência `Banco` no documento.
- **Se a coluna NÃO existir:** NÃO escrever a referência errada em nenhuma seção. Buscar a coluna correta via `describe_table` e registrar a correção no snapshot com o formato: `CORREÇÃO: <coluna_errada> → <coluna_correta> em <TABELA>`.

### 3-B.2 — Levantar valores reais de colunas de domínio

Para toda coluna que controle status, situação, canal ou tipo no fluxo, executar via MCP `execute_query` (usando o MCP server lido de `database.mcp_server` em `discovery-project.yml`):

```sql
SELECT DISTINCT <coluna>, COUNT(*) AS total
FROM prev.<TABELA>
GROUP BY <coluna>
ORDER BY <coluna>
```

- Registrar **todos os valores confirmados** na Seção 8 (Estados envolvidos) e Seção 9 (Dados).
- Cada valor com significado de negócio vira uma `RN-Fxxx-NN` na Seção 5.2.
- Evidência: `[Confirmado por banco]` em todas as células que referenciam esses valores.

### 3-B.3 — Tabelas prioritárias a validar

Executar obrigatoriamente para as tabelas de domínio identificadas no CF corrente (DISC-03). As tabelas de domínio são aquelas que armazenam valores de status, situação, tipo ou canal usados como lookup — identificáveis pelo nome (ex.: sufixo `_SITUACAO`, `_MOTIVO`, `_TIPO`, `_STATUS`, `_SITUACAO`) ou pela coluna de controle citada nas SQLs diagnósticas do CF.

Para cada tabela de domínio do CF:
- Executar `describe_table` para confirmar colunas reais
- Executar `SELECT DISTINCT` para confirmar valores existentes
- Registrar no snapshot qualquer divergência entre os valores do CF e os valores reais do banco

**Regra de ouro:** nunca documentar um valor de status/situação como "possível" ou inferido quando a tabela de domínio existe no banco. Sempre confirmar via MCP antes de escrever. Se não for possível executar (MCP indisponível), registrar como `[PEN]` e abrir pendência 🔴 Crítico na Seção 13.

---

## Passo 4 — Gerar o arquivo FLUXO

Nome do arquivo: `discovery/FLUXO-<fluxo_codigo>-<slug>.md`

O documento deve conter **exatamente as 14 seções obrigatórias** na ordem abaixo. Ver [REFERENCE.md](REFERENCE.md) para o template completo de cada seção.

**Cabeçalho obrigatório:** usar o formato com H1 — `# FLUXO <fluxo_codigo> — <Nome>` seguido dos campos em negrito (`**Tipo:**`, `**Escopo:**`, `**Relacionados:**`, `**Última atualização:**`, `**Palavras-chave:**`). Ver template completo em [REFERENCE.md](REFERENCE.md).

### Estrutura obrigatória (14 seções + subseções obrigatórias)

| Nº | Seção | Observação |
|---|---|---|
| 1 | Objetivo | Somente texto narrativo — sem tabela |
| 2 | Quem usa | |
| 3 | Pré-condições | |
| 4 | Entradas necessárias | |
| 5 | Caminho feliz | |
| 5.1 | Diagrama de sequência | Condicional — ver regras |
| **5.2** | **Regras de negócio** | **Obrigatório — Business Rule Catalog (IIBA)** |
| 5.3 | Critérios de aceitação por regra (BDD) | **Opcional** — ver critérios de seleção abaixo |
| 6 | Variações | Formato BDD obrigatório (Dado/Quando/Então) |
| 7 | Erros e exceções | Coluna "Regra violada" obrigatória |
| 8 | Estados envolvidos | |
| 8.1 | Diagrama de estados | Obrigatório quando há status |
| 9 | Dados (tabelas e campos críticos) | |
| 10 | Pontos de atenção operacional | |
| 11 | Integrações externas | |
| 12 | Histórico de mudanças relevantes | |
| 13 | Pendências e lacunas | |
| **14** | **Mapa de rastreabilidade para modernização** | **Obrigatório — consolida fontes por aspecto** |

A ordem e os títulos das seções são fixos. Não renomear, não reordenar, não suprimir seção — mesmo que vazia (usar placeholder `[PEN]`).

---

### Seção 14 — Mapa de rastreabilidade para modernização (obrigatória)

**A Seção 14 é obrigatória em todos os fluxos.** Deve ser a última seção do documento, após a Seção 13 (Pendências), antes do bloco `## SQL Diagnóstico`.

**Propósito:** Responder a pergunta "Para reescrever ou migrar este fluxo, o que preciso ler e preservar?" sem abrir nenhum outro arquivo.

**Fontes para construção:**
- Seção 5.2 (Regras de negócio) → gera 14.1 (uma linha por RN-Fxxx-NN identificada)
- Seção 9 (Dados — tabelas de escrita) → gera 14.2 (uma linha por tabela com operação de escrita)
- Seção 11 (Integrações externas) → gera 14.3 (uma linha por sistema integrado)
- Arquivos de evidência em `EVIDENCIAS-LEGADO/ARQUIVOS/` referenciados nas seções anteriores → gera 14.4

**Estrutura obrigatória (4 subseções):**

```markdown
## 14. Mapa de rastreabilidade para modernização

> Esta seção consolida de onde vem cada informação documentada neste fluxo.
> Serve como ponto de partida para qualquer equipe que precise reescrever,
> migrar ou reimplementar esta funcionalidade em outra tecnologia ou plataforma.

### 14.1 Regras de negócio

| Regra | Artefato atual | Tipo | Caminho / Localização | O que reescrever |
|---|---|---|---|---|
| RN-Fxxx-01 | <SP / Controller / Service> | SP / Controller / Trigger | <caminho> | <lógica ou validação a reimplementar> |

### 14.2 Dados persistidos (banco de dados)

| Tabela / Objeto | Tipo | Operação neste fluxo | Colunas críticas | O que preservar na migração |
|---|---|---|---|---|
| <tabela> | Tabela / View / SP / Trigger | INSERT / UPDATE / DELETE / SELECT | <colunas de negócio> | <o que não pode ser perdido> |

### 14.3 Integrações externas a reimplementar

| Sistema / Serviço | Tipo de integração | Contrato atual | Dados trocados | Prioridade na migração |
|---|---|---|---|---|
| <sistema> | <API REST / batch / fila / OAuth> | <arquivo de evidência ou spec> | <dados trocados> | Alta / Média / Baixa |

### 14.4 Artefatos de código legado a analisar

| Artefato | Tipo | Caminho | Conteúdo relevante para modernização |
|---|---|---|---|
| <arquivo.cs / SP_X> | Controller / Service / SP / Repository | <caminho> | <o que contém — regras, lógica de estado, queries> |
```

**Regras de preenchimento:**
- **14.1:** Uma linha por regra `RN-Fxxx-NN` da Seção 5.2. Se a regra vier de SP, registrar o nome da SP. Se vier de controller, registrar o arquivo. Se não confirmada, usar `[PEN]` na coluna Caminho.
- **14.2:** Apenas tabelas com **operação de escrita** (INSERT/UPDATE/DELETE) são obrigatórias. Tabelas somente-leitura entram se forem críticas para o fluxo (ex.: lookup de status).
- **14.3:** Apenas integrações com evidência na Seção 11. Se a Seção 11 estiver com `[PEN]`, registrar `[PEN]` na linha correspondente.
- **14.4:** Todos os arquivos de evidência registrados em `EVIDENCIAS-LEGADO/ARQUIVOS/` para este fluxo. Nunca inventar caminhos — apenas os já registrados.
- Se uma subseção estiver inteiramente vazia por falta de evidência: inserir texto explicativo e abrir pendência 🟡 Funcional na Seção 13.

---

### Seção 5.2 — Regras de negócio (obrigatória)

**A Seção 5.2 é obrigatória em todos os fluxos.** Deve ser gerada após o caminho feliz (Seção 5) e antes das variações (Seção 6).

**Formato obrigatório:** Business Rule Catalog (IIBA) — cada regra recebe:
- **ID único** no padrão `RN-Fxxx-NN` (ex.: `RN-F001-01`)
- **Enunciado** em linguagem de negócio — nunca usar nome de campo ou valor técnico como enunciado
- **Dado (contexto):** estado ou contexto prévio que faz a regra ser aplicável
- **Quando (gatilho):** evento ou condição que dispara a regra
- **Então (efeito):** o que acontece quando a regra é aplicada
- **Exceção:** variação ou caso em que a regra não se aplica (ou é `—`)
- **Evidência:** coluna rastreável (banco ou legado)

**Tabela de decisão:** quando uma regra tiver múltiplas combinações de condição e resultado, inserir tabela de decisão após a linha da regra, com colunas de condições e coluna de resultado.

**Fontes para derivar as regras:**
1. Pré-condições (Seção 3): cada pré-condição de negócio geralmente é uma regra implícita
2. Passos do caminho feliz com validação ou desvio: extrair a regra que os governa
3. Campos obrigatórios (Seção 4): regra de preenchimento é uma regra de negócio
4. Valores de status e transições (DADOS-06): cada transição permitida é uma regra
5. Variações (Seção 6): cada cenário alternativo tem uma regra que o governa

**Regras de ID:** sequenciar a partir de `01` para cada fluxo. O ID deve ser reutilizado na coluna "Regra violada" da Seção 7 e referenciado nas TELA-xxx associadas.

**Se não for possível derivar nenhuma regra com evidência:** abrir pendência `PEND-Fxxx-NN` na Seção 13 (nível 🔴 Crítico) explicando que as regras de negócio precisam ser levantadas com o PO/negócio.

---

### Seção 5.3 — Critérios de aceitação por regra, BDD (opcional)

**A Seção 5.3 é opcional.** Gerar apenas quando uma ou mais RNs da Seção 5.2 se enquadrarem nos critérios abaixo. Se nenhuma se enquadrar, omitir a seção inteiramente — não criar seção vazia.

**Critérios para incluir um bloco 5.3 para uma RN:**
- A regra é crítica ou complexa (múltiplas condições, tabela de decisão)
- A regra tem histórico de incidente ou regressão conhecida
- A regra está marcada com `ADAPTAR` ou `SIMPLIFICAR` na coluna Decisão da seção 14.1
- A regra precisa de um critério verificável externamente para QA ou testes automatizados

**Diferença da Seção 6:** a Seção 6 descreve variações do *fluxo completo* (desvios do caminho feliz). A Seção 5.3 descreve o critério de aceitação de uma *regra específica* — o que confirma que ela está implementada corretamente, no cenário normal de ativação.

**Formato de cada bloco:**

```
#### RN-Fxxx-NN — <Nome resumido da regra>

**Dado que** <contexto que ativa esta regra>
**Quando** <ação ou evento que dispara a regra>
**Então** <comportamento esperado do sistema>
**E** <efeito colateral verificável, se houver>
**Critério de aceitação:** <o que QA ou teste pode verificar — dado no banco, resposta HTTP, mensagem, ausência de efeito>
```

**Limite recomendado:** 3 a 5 blocos por fluxo. Mais do que isso, é sinal de que a 5.2 precisa de refinamento ou que os cenários pertencem à Seção 6.

---

### Seção 6 — Variações em formato BDD (obrigatório)

**Cada variação deve ser escrita no formato BDD (Behavior-Driven Development):**

```
### V0N — <Nome da variação>

**Dado que** <contexto/estado inicial — pré-condição>
**Quando** <ação do usuário ou evento do sistema>
**Então** <resultado esperado no sistema>
**E** <resultado adicional, se houver>
**Critério de aceitação:** <o que QA ou analista de negócio pode verificar sem abrir código — dado no banco, mensagem exibida, redirecionamento, status alterado>
```

**Regras obrigatórias:**
- Cada cenário BDD deve referenciar a regra de negócio que o governa, usando o ID `RN-Fxxx-NN` da Seção 5.2
- O "Critério de aceitação" deve ser verificável externamente (por QA ou analista) sem acesso ao código
- Se não houver evidência suficiente para o critério de aceitação, marcar como `[PEN]` na linha do critério e abrir pendência na Seção 13
- Nunca escrever variação apenas como texto corrido — sempre em formato BDD

---

### Seção 7 — Coluna "Regra violada" (obrigatória)

A tabela de erros e exceções deve ter obrigatoriamente a coluna **"Regra violada"**:

```
| Código | Mensagem / Sintoma | Regra violada | Causa | Impacto | Ação recomendada | Evidência |
```

- **Regra violada:** preencher com o ID `RN-Fxxx-NN` da Seção 5.2 quando o erro for consequência de violação de regra de negócio
- Se o erro for puramente técnico (sem regra de negócio associada), usar `—`
- Se não for possível determinar a regra violada, usar `[PEN]` e abrir pendência na Seção 13

### Tag de pendência — `[PEN]`

A única tag de marcação usada na documentação é `[PEN]` — indica lacuna sem evidência confirmada.

**Regras de uso:**

- Usar `[PEN]` **somente em células de tabela** (coluna `Evidência` ou outra coluna de dado desconhecido) e na Seção 13 (Pendências).
- **PROIBIDO** inserir `[PEN]` no texto narrativo corrido.
- Quando a informação for confirmada (por banco ou por código legado), **remover o `[PEN]`** e preencher a célula com a fonte real.

**Regra de tratamento de incerteza no texto narrativo:**

- Se a informação **NÃO está confirmada**: não entra como afirmação no texto. Manter o texto neutro ou omitir a afirmação. Abrir pendência na Seção 13.
- Se a informação **está confirmada**: afirmar como fato no texto narrativo; registrar a fonte na coluna `Evidência` da tabela correspondente.

### Regra para evidência de código legado

Toda afirmação baseada em código legado **não cola código** no FLUXO nem na TELA. Em vez disso:

1. Criar ou atualizar o arquivo de evidência reutilizável em `discovery/EVIDENCIAS-LEGADO/ARQUIVOS/` (ver Passo 4-C).
2. Referenciar o arquivo no FLUXO/TELA com o formato:

```
> **Evidência:** [`<nome-sanitizado>.md`](../EVIDENCIAS-LEGADO/ARQUIVOS/<nome-sanitizado>.md)
> <1–2 frases resumindo o que foi identificado e como impacta este fluxo.>
```

Ver sanitização de nome, template de arquivo de evidência e template de INDEX.md em [REFERENCE.md](REFERENCE.md).

### Regras de preenchimento

- Seções 1–7 e 10–12: texto narrativo neutro (sem tags inline). Evidência vai na coluna `Evidência` das tabelas. O que não está confirmado vai para a Seção 13 como pendência.
- Seção 2 (Quem usa): cruzar com DISC-02 para identificar perfis; evidência na coluna da tabela.
- Seções 8–9: preencher com dados extraídos do CF + DADOS-06 + DADOS-09; rótulos somente na coluna `Evidência`.
- Seção 13: listar todas as lacunas no formato `PEND-<fluxo_codigo>-NN` — único local onde `[PEN]` e `` ficam como item de pendência.
- Seção 12 (Histórico): preencher apenas se houver evidência de versões anteriores no banco ou legado.

---

### Regra estrutural obrigatória — Camada descritiva + camada estruturada

**Toda seção (1–13) deve seguir a ordem:**

1. **Texto descritivo primeiro** (2–6 linhas) — explica o que a seção representa, seu papel no fluxo e dependência estrutural se houver.
2. **Tabela estruturada depois** — apresenta os dados rastreáveis com fontes de evidência.

**Nunca substituir texto por tabela. Nunca iniciar seção diretamente com tabela.**

#### Regra específica para a Seção 1 — Objetivo

A Seção 1 é **obrigatoriamente textual** — nunca contém tabela. Deve responder:

- O que este fluxo faz.
- Onde ele se encaixa no sistema GPrev.
- Qual o resultado esperado quando bem-sucedido.
- Se há dependência estrutural com outros fluxos ou módulos.

Máximo de 10 linhas. Linguagem acessível para Analista de Negócio e PO. Sem tags inline — texto neutro e afirmativo para o que é confirmado, omitindo ou remetendo a pendência o que não está.

#### Padrão de redação por frase

Sempre seguir a ordem:

1. Texto humano primeiro.
2. Campo técnico entre parênteses.
3. **Sem tag inline** — a fonte vai na coluna `Evidência` da tabela, não na frase.

**Exemplo — texto narrativo (sem tag inline):**

> Quando um documento é cancelado, o sistema mantém o registro original e cria um registro complementar de cancelamento (tabela `prev.processo_fluxo_papel_pessoa_documento_cancelado`).

**Exemplo — coluna Evidência na tabela correspondente:**

| Elemento | Descrição | Evidência |
|---|---|---|
| Registro de cancelamento | Mantém original e cria complementar de cancelamento | DDL `prev.processo_fluxo_papel_pessoa_documento_cancelado` |

---

### Diagramas PlantUML — Governança obrigatória

Os diagramas são gerados como sub-seções de 5 e 8. Aplicar as regras abaixo em cada caso.

#### Seção 5.1 — Diagrama de sequência

**Condição de geração:** gerar somente se todos os critérios mínimos estiverem satisfeitos:

| Elemento | Fonte | Condição |
|---|---|---|
| Ator (Usuário/Operador do sistema) | Sempre presente | Obrigatório |
| Banco (schema do sistema) | DDL/volumetria via MCP | Obrigatório |
| Interface de entrada (`<Tela/Controller/Endpoint>`) | Candidato identificado no Passo 4-B | Condicional — omitir se ausente |
| Serviço/Bean (`<Classe>`) | Candidato identificado no Passo 4-B | Condicional — omitir se ausente |
| Integração externa | Seção 11 com evidência | Condicional — incluir somente se confirmado |

**Se os elementos obrigatórios (Ator + Banco) estiverem presentes:** gerar o diagrama, marcando elementos sem confirmação com `note` indicando `[PEN] — candidato: <arquivo>`.

**Se não for possível satisfazer os critérios mínimos:** omitir o diagrama e abrir pendência `PEND-<fluxo_codigo>-NN` na Seção 13 (nível 🟡 Funcional) explicando o que falta.

**Notas no diagrama:**
- Elemento confirmado por código legado → `note` com referência ao arquivo de evidência.
- Elemento com candidato identificado mas não confirmado → `note` com `[PEN] — candidato: <arquivo>`.
- Interação com banco confirmada → `note` indicando a tabela/SP.
- Nunca omitir notas — todo participante carrega fonte ou indicação de lacuna.

#### Seção 8.1 — Diagrama de estados

**Condição de geração:** sempre gerar quando houver ao menos um valor de status identificado na Seção 8.

**Regras obrigatórias:**

| Elemento | Regra |
|---|---|
| Valores de estado | Usar o valor real da coluna (`1`, `2`, `'ATIVO'`) — não usar rótulo descritivo sozinho |
| Transição confirmada por legado | Linha sólida + `note on link` com referência ao arquivo de evidência |
| Transição sem confirmação | `[#gray,dashed]` + `note` com `[PEN]` |
| Estado sem transição conhecida | Incluir `note` explicativa indicando a lacuna |
| Transições inventadas | Proibido — apenas as derivadas de DADOS-06 ou candidatos do Passo 4-B |

**Nunca omitir o diagrama de estados quando houver status identificados** — a ausência de transições conhecidas não dispensa o diagrama; usar tracejado para todas as transições.

---

## Padrão obrigatório de redação

Estas regras se aplicam a **todo o conteúdo gerado** — células de tabela, parágrafos, listas e notas.

### Regra 1 — Proibir escrita técnica crua

Nunca escrever expressões como atribuição direta de campo:

| ❌ Proibido | ✅ Correto |
|---|---|
| `solicitacao.status = 1` | Quando a solicitação está na situação "Aberta" (campo `SOLICITACAO.status`, tipo integer, valor `1`) — evidência na coluna Evidência da tabela |
| `historico.tipo = 4` | Quando o histórico registra o tipo "Encaminhamento" (campo `HISTORICO.tipo`, tipo integer, valor `4`) — evidência na coluna Evidência |
| `encaminhamento.devolvido = true` | Quando o encaminhamento foi devolvido ao órgão de origem (campo `ENCAMINHAMENTO.devolvido`, tipo boolean, valor `true`) |

**Formato obrigatório para referenciar campo + valor no texto narrativo:**

```
<Descrição em linguagem natural>
(campo `<tabela>.<coluna>`, tipo <tipo>, valor `<valor>`).
```

O rótulo de evidência vai na coluna `Evidência` da tabela estruturada — nunca inline no texto.

### Regra 2 — Priorizar descrição textual do banco

Sempre que a documentação do banco (DADOS-* ou comentário DDL) contiver descrição formal da coluna, usar essa descrição **antes** do nome técnico:

```
A coluna "status" indica a situação atual da solicitação no fluxo de atendimento
(campo `SOLICITACAO.status`).
```

A fonte vai na coluna `Evidência` da tabela — não no final da frase narrativa.

Nunca apresentar apenas o nome técnico sem contexto descritivo.

### Regra 3 — Linguagem compatível com NotebookLM

- Frases completas — nunca fragmentos ou expressões isoladas.
- Preferir tabelas estruturadas a listas longas sem contexto.
- Sem siglas não explicadas — sempre expandir na primeira ocorrência.
- Nome técnico sempre entre parênteses ou em célula separada, nunca como único conteúdo.

### Regra 4 — Proibições de forma

- Não iniciar parágrafo ou célula com nome de tabela (`SOLICITACAO`, `HISTORICO`, `ENCAMINHAMENTO`…).
- Não escrever expressões SQL isoladas fora do bloco `## SQL Diagnóstico`.
- Não escrever apenas nome de campo sem contexto descritivo (`SOL_INT_COD`, `status`, `tipo`…).

### Regra 5 — Volumetria com interpretação obrigatória

Toda menção a contagens de registros (volumetria) deve estar acompanhada de interpretação de negócio. A confirmação estrutural de uma tabela **não depende** de volumetria — existência de tabela é confirmada por DDL, não por contagem.

**Volumetria é permitida apenas quando:**

| Critério | Exemplo aceitável |
|---|---|
| Demonstrar predominância | "79% dos processos seguem o caminho feliz (status `4`)" |
| Demonstrar anomalia | "Apenas 9 registros identificados — possível uso residual ou inativo" |
| Evidenciar inatividade estrutural | "Tabela com zero registros — estrutura presente mas sem uso operacional confirmado" |
| Indicar criticidade operacional | "Meio milhão de registros ativos — tabela central do fluxo operacional" |
| Explicar multiplicidade relacional | "Média de 3 vínculos por requerimento — indica estrutura de histórico por etapa" |

**É proibido gerar volumetria isolada sem interpretação.**

| ❌ Proibido | ✅ Correto |
|---|---|
| "A tabela `prev.documento` possui 540.531 registros." | Omitir o número — a existência da tabela já está confirmada por DDL. |
| "Foram encontrados 12.847 registros em `prev.processo`." | "O volume de processos (~12,8 mil) indica uso operacional ativo e contínuo desta tabela no fluxo." |

**Regra de decisão antes de incluir volumetria:**
1. O número altera o entendimento do comportamento ou da estrutura do fluxo?
2. Se **não** — omitir.
3. Se **sim** — incluir com interpretação explícita em linguagem de negócio.

---

## Passo 4-C — Gerenciar arquivos de evidência reutilizáveis

**Executar para cada evidência encontrada no legado que suporte uma afirmação no fluxo.**

### 4-C.1 — Sanitizar nome do arquivo de evidência

| Regra | Detalhe |
|---|---|
| Remover prefixo `legado/` | Começar pelo primeiro segmento de pacote real |
| Substituir `/` e `\` por `__` | Duplo underline |
| Manter extensão do arquivo legado | Ex.: `.java`, `.xhtml` |
| Adicionar sufixo `.md` | Ao final do nome inteiro |

Exemplo: `legado/br/gov/iprev/gprev/service/ProcessoService.java` → `br__gov__iprev__gprev__service__ProcessoService.java.md`

Caminho de destino: `discovery/EVIDENCIAS-LEGADO/ARQUIVOS/<nome-sanitizado>.md`

### 4-C.2 — Criar ou complementar o arquivo de evidência

**Se o arquivo NÃO existir:**
- Criar a partir do template em [REFERENCE.md](REFERENCE.md) (seção "Template: arquivo de evidência").
- Preencher: caminho real, tipo de artefato, fluxo corrente, primeira entrada em "Evidências registradas".

**Se o arquivo JÁ existir:**
- Adicionar nova entrada em "Evidências registradas" (append — nunca remover anteriores).
- Atualizar `Última atualização`.
- Adicionar o fluxo/tela corrente em `Fluxos impactados` ou `Telas impactadas` **sem remover existentes**.

### 4-C.3 — Atualizar INDEX.md

Arquivo: `discovery/EVIDENCIAS-LEGADO/INDEX.md`

- Se não existir: criar com template em [REFERENCE.md](REFERENCE.md).
- Adicionar ou atualizar a linha do arquivo de evidência na tabela.
- Atualizar `Última atualização` do INDEX.md.

### 4-C.4 — Referenciar no FLUXO/TELA

No ponto do documento onde a afirmação é feita, incluir:

```
> **Evidência:** [`<nome-sanitizado>.md`](../EVIDENCIAS-LEGADO/ARQUIVOS/<nome-sanitizado>.md)
> <1–2 frases resumindo o observado e o impacto neste fluxo.>
>
>
```

**Proibido:** colar código, transcrever método, exibir snippet do legado diretamente no FLUXO ou na TELA.

---

## Passo 4-B — Busca dirigida no legado antes de abrir pendência

**Executar obrigatoriamente antes de registrar qualquer pendência do tipo "confirmar no legado".**

Para cada lacuna identificada nas seções 1–7 e 10–12, buscar em `discovery/arquivos-legado.txt` por termos-chave do fluxo. Exemplos de termos por domínio do sistema 156:

| Domínio | Termos a buscar em `arquivos-legado.txt` |
|---|---|
| Solicitação / Protocolo | `SolicitacaoService`, `SolicitacaoController`, `solicitacao`, `protocolo`, `encaminhamento` |
| Histórico / Ciclo de vida | `HistoricoService`, `historico`, `status`, `situacao`, `andamento` |
| Assunto / Categoria | `AssuntoService`, `AssuntoController`, `assunto`, `subdivisao`, `categoria` |
| Cidadão / Usuário | `UsuarioService`, `UsuarioController`, `cidadao`, `pessoa`, `autenticacao` |
| Notificação / Push | `NotificacaoService`, `PushPendenteService`, `notificacao`, `push`, `email` |
| URBS / Transporte | `OnibusService`, `ImportacaoVeiculos`, `urbs`, `onibus`, `veiculo`, `cartao` |
| Avaliação / Satisfação | `PesquisaSatisfacaoService`, `avaliacao`, `satisfacao`, `pesquisa` |
| Equipamento Urbano | `EquipamentoUrbanoService`, `equipamento`, `seuc` |
| Integração eCidadão | `eCidadaoNegocio`, `ApieCidadao`, `ecidadao` |
| Jobs (Hangfire) | `TimerImportacao`, `IHostedService`, `BackgroundService`, `hangfire` |

**Para cada termo encontrado:**
1. Registrar os caminhos candidatos diretamente na seção onde a lacuna aparece, no formato:
   ```
   > Candidatos código: `Api156.Application/Services/SolicitacaoService.cs` — [PEN]
   ```
2. Só abrir pendência `PEND-Fxxx-NN` se os candidatos **não forem suficientes** para confirmar o comportamento.

**Regra:** O volume de pendências "confirmar no legado" deve cair proporcionalmente à cobertura de candidatos encontrados em `arquivos-legado.txt`.

---

## Passo 4-D — Auto-verificação estrutural antes de finalizar

**Executar obrigatoriamente antes de encerrar a geração ou refinamento do arquivo FLUXO.**

Percorrer cada uma das 14 seções obrigatórias (não inclui a subseção 5.3, que é opcional) e aplicar os três verificadores abaixo:

### Verificador 1 — Seção inicia com tabela?

Para cada seção de 1 a 13:
- Verificar se o primeiro elemento após o título `## N. <Nome>` é uma tabela (linha iniciando com `|`).
- **Se sim:** inserir texto descritivo (2–6 linhas) antes da tabela, explicando o que a seção representa e seu papel no fluxo.
- Exceção: blocos `>` (blockquote de fonte/nota) não contam como tabela — verificar o elemento seguinte.

### Verificador 2 — Seção 1 contém tabela?

- Verificar se a Seção 1 (Objetivo) contém qualquer linha de tabela (`|`).
- **Se sim:** reescrever integralmente como texto narrativo, preservando as informações. Sem rótulos inline — texto neutro e afirmativo para o que é confirmado; o que não está confirmado vira pendência na Seção 13.
- A Seção 1 nunca pode conter tabela — sem exceção.

### Verificador 3 — Seção contém apenas `[PEN]` sem explicação?

Para cada seção de 1 a 13:
- Verificar se o único conteúdo textual é `[PEN]` ou uma tabela onde todas as células são `[PEN]`, sem qualquer texto explicativo.
- **Se sim:** inserir parágrafo explicando qual é a lacuna, por que não foi possível confirmar e qual seria o caminho para confirmação.
- Garantir que a pendência correspondente exista na Seção 13.

### Verificador 4 — Diagramas PlantUML presentes e corretos?

**Para a Seção 5.1 (diagrama de sequência):**
- Verificar se os critérios mínimos estão satisfeitos: Ator identificável (sempre presente) + ao menos uma tabela ou endpoint identificado (Seção 9 preenchida).
- **Se critérios mínimos atendidos e o diagrama estiver ausente:** inserir o diagrama, marcando Interface de entrada e Serviço como `[PEN] — candidato: <arquivo>` se não confirmados.
- **Se os critérios mínimos NÃO puderem ser satisfeitos e o diagrama estiver presente:** remover e abrir pendência.
- Verificar se algum participante não tem nota — se sim, adicionar `[PEN]`.

**Para a Seção 8.1 (diagrama de estados):**
- Verificar se a Seção 8 tem ao menos um status identificado.
- **Se sim e o diagrama estiver ausente:** gerar o diagrama com os valores identificados; transições sem evidência entram como tracejadas.
- Verificar se alguma transição sólida não tem referência a arquivo de evidência — se sim, converter para tracejado e registrar lacuna.

---

## Passo 5 — SQL Diagnóstico

Após a Seção 13, inserir bloco adicional com as queries do CF (não numerado como seção):

```
## SQL Diagnóstico

Queries derivadas do CF-<NNN>. Executar via MCP lido de `database.mcp_server` em `discovery-project.yml` (para este projeto: `project-0-Gprev-app-previdenciario`).
```

Copiar queries **verbatim** do CF. Nunca modificar lógica.

---

## Passo 6 — Atualizar DISC-00-INDICE.md

Adicionar (ou atualizar) a entrada na tabela "Onde consultar cada assunto":

```
| Fluxo <fluxo_codigo> — <Nome> | FLUXO-<fluxo_codigo>-<slug>.md | Seções 8, 9, 13 + SQL |
```

- O link deve apontar **sempre para o arquivo corrente** (`FLUXO-<fluxo_codigo>-<slug>.md`), sem sufixo de versão.
- Se a entrada já existir (de geração anterior), atualizar apenas a data em "Última atualização" — não duplicar a linha.

Adicionar na seção de pendências (se não existir):

```
| PEND-<fluxo_codigo>-01 | 🟡 Funcional | Revalidar seções 1–7 e 10–12 com código legado | FLUXO-<fluxo_codigo>-<slug>.md |
```

**Regras do DISC-00:**
- Nunca remover entradas anteriores.
- Nunca registrar link para `_historico/` na tabela principal — o histórico é referenciado apenas na seção opcional "Histórico de versões" do DISC-00, se houver.
- Não duplicar linhas: se o fluxo já tiver entrada, atualizar em vez de adicionar.

---

## Passo 7 — Gerar snapshot individual

Arquivo: `discovery/SNAP-FLUXO-<fluxo_codigo>-<YYYY-MM-DD>.md`

Conteúdo mínimo — ver template em [REFERENCE.md](REFERENCE.md):

- Fluxo processado (código + nome)
- Fontes lidas (status de cada documento obrigatório)
- Evidências encontradas por tipo, com contagens
- Quantidade de pendências abertas
- Divergências banco × legado detectadas
- Versionamento: ação realizada
- Bloqueio estrutural: se alguma seção crítica estiver inteiramente `[PEN]`

---

## Passo 8 — Relatório de encerramento

Ao finalizar, informar ao usuário com o seguinte checklist:

```
[ ] Arquivo corrente:      discovery/FLUXO-<fluxo_codigo>-<slug>.md
[ ] Histórico gerado:      <Nenhum (arquivo novo) | discovery/_historico/FLUXOS/FLUXO-<fluxo_codigo>-<slug>-<YYYY-MM-DD-HHMM>.md>
[ ] Snapshot gerado:       discovery/SNAP-FLUXO-<fluxo_codigo>-<YYYY-MM-DD>.md
[ ] DISC-00 atualizado:    Sim (link para arquivo corrente, sem sufixo de versão)
[ ] Pendências abertas:    <N> (PEND-<fluxo_codigo>-01 … NN)
[ ] Ação sobre corrente:   <Criado novo | Histórico salvo + sobrescrito | Histórico salvo + refinado>
[ ] Bloqueio estrutural:   <Nenhum | Seção(ões) X inteiramente [PEN]>
```

---

## Proibições absolutas

- **Não inserir a tag `[PEN]` no texto narrativo corrido** — `[PEN]` só aparece em: (a) células de tabelas estruturais (coluna `Evidência` ou célula de dado desconhecido), (b) Seção 13 (Pendências).
- **Não escrever hipótese ou incerteza como afirmação no texto narrativo** — o que não está confirmado vira pendência na Seção 13; o texto narrativo descreve apenas o que é fato ou descreve o fluxo de forma neutra.
- Não resumir o fluxo nem agrupar fluxos distintos.
- Não gerar "top N" de tabelas ou regras.
- Não escrever como manual de usuário ou especificação futura.
- Não deduzir regra de negócio sem evidência explícita de banco ou legado.
- Não inventar status, enum, transição, campo ou regra.
- Não apagar pendências existentes ao refinar.
- **Não gerar arquivo com sufixo `-v2`, `-v3` ou qualquer sufixo de versão na pasta `discovery/`** — o arquivo corrente é sempre `FLUXO-<FXXX>-<slug>.md`.
- **Não alterar o arquivo corrente existente sem antes salvar cópia em `discovery/_historico/FLUXOS/`** com timestamp no nome.
- **Não registrar link para `_historico/` na tabela principal do DISC-00** — histórico é referenciado apenas em seção opcional "Histórico de versões".
- **Não consolidar snapshots** (`SNAP-FLUXO-*` e `SNAP-REVALIDACAO-*`) — cada execução gera seu próprio snapshot como trilha de auditoria imutável.
- Não mencionar o novo stack como fonte.
- Não preencher seções 1–7 com conteúdo deduzido apenas do nome do fluxo ou das tabelas.
- Não alterar a estrutura ou a ordem das 14 seções obrigatórias.
- Não copiar conteúdo de FLUXOs de outros CF.
- **Não iniciar seção com tabela** — toda seção exige texto descritivo (2–6 linhas) antes da tabela.
- **Não usar tabela para explicar conceito** — conceitos e contexto são sempre texto narrativo.
- **Não gerar seção com apenas `[PEN]` sem explicação** — registrar a lacuna em linguagem natural e garantir pendência correspondente na Seção 13.
- **Não usar tabela na Seção 1 (Objetivo)** — a Seção 1 é obrigatoriamente textual, sem exceção.
- **Não escrever SQL cru solto** fora do bloco `## SQL Diagnóstico`.
- **Não escrever apenas nomes de tabela** sem contexto descritivo.
- **Não gerar volumetria isolada sem interpretação de negócio** — frases do tipo "A tabela `prev.X` possui N registros" são proibidas quando não demonstram predominância, anomalia, inatividade, criticidade operacional ou multiplicidade relacional. Se o número não altera o entendimento do fluxo, omiti-lo. A existência de uma tabela é confirmada por DDL — nunca depende de contagem.
- **Não escrever expressões técnicas cruas** como `campo = valor`, `tabela.coluna = X` fora do bloco SQL Diagnóstico.
- **Não iniciar parágrafo ou célula de tabela com nome de tabela** do banco de dados.
- **Não escrever expressões SQL isoladas** fora do bloco `## SQL Diagnóstico`.
- **Não escrever apenas nome de campo sem contexto descritivo** — sempre acompanhar de descrição em linguagem natural.
- **Não usar siglas sem explicação prévia** na primeira ocorrência do documento.
- **Não abrir pendência "confirmar no legado" sem antes executar o Passo 4-B** (busca dirigida em `arquivos-legado.txt`).
- **Não afirmar evidência de código legado sem criar/atualizar o arquivo de evidência correspondente** em `discovery/EVIDENCIAS-LEGADO/ARQUIVOS/` (Passo 4-C).
- **Não colar código, snippet ou transcrição de método legado** diretamente no FLUXO ou na TELA — toda evidência de código vai para o arquivo de evidência.
- **Não finalizar o arquivo sem executar o Passo 4-D** (auto-verificação estrutural dos três verificadores).
- **Não gerar diagrama de sequência (5.1) sem satisfazer os critérios mínimos** — se Ator + Banco não puderem ser identificados, omitir e abrir pendência.
- **Não inventar participantes no diagrama de sequência** sem candidato legado identificado (Passo 4-B) ou evidência de banco.
- **Não omitir o diagrama de estados (8.1) quando houver status identificados** — ausência de transições conhecidas não dispensa o diagrama; usar tracejado com `[PEN]`.
- **Não inventar transições no diagrama de estados** — apenas as derivadas de DADOS-06 ou candidatos identificados no Passo 4-B.
- **Não usar rótulos descritivos genéricos como nome de estado** sem indicar o valor real da coluna de status.
- **Nunca modificar o repositório legado** — somente arquivos em `discovery/` são criados ou editados.

---

## Compatibilidade NotebookLM

O documento gerado deve ser:

- **Duas camadas por seção:** texto descritivo (contexto, papel, dependência) seguido de tabela estruturada com coluna `Evidência`. Nenhuma seção pode ter apenas um dos dois.
- Sem ambiguidade — células desconhecidas carregam `[PEN]`; texto narrativo é limpo e sem tags.
- Seções claramente delimitadas por `---` e títulos numerados.
- Linguagem técnica, direta, repetível e consistente entre fluxos.
- Sem texto decorativo, introdutório ou de fechamento que não seja dado rastreável.
- A Seção 1 (Objetivo) é a única seção sem tabela — texto corrido que o NotebookLM indexa como contexto semântico do fluxo.

---

## Referências

- Template completo das 14 seções e snapshot: [REFERENCE.md](REFERENCE.md)
- Catálogo de CFs: `discovery/DISC-03-CATALOGO-DE-FLUXOS.md`
- Template canônico de fluxo: `.github/skill/discoverytoolkit/discovery-03-fundacao-bootstrap-templates/assets/FLUXO-TEMPLATE-LEGADO.md`
- Metodologia: `discovery/DISC-99-METODOLOGIA-E-ARQUITETURA-DO-DISCOVERY.md`
