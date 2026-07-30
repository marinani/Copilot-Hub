---
name: discovery-fluxo-from-cf
description: "[DEPRECATED] Use discovery-20-fluxos-gerar no lugar. Esta versão antiga gera apenas rascunho básico com Dados + Estados do CF; a nova skill operacional trabalha a partir do catálogo consolidado e inclui UML, plano de testes e rastreabilidade reforçada."
---

# ⛔ DEPRECATED — Use `discovery-20-fluxos-gerar`

> **Esta skill foi supersedida pela versão industrial.**
>
> O que esta skill faz (rascunho com Dados + Estados do CF) é um subconjunto do que a versão industrial entrega, com qualidade muito inferior:
>
> | Capacidade | `discovery-fluxo-from-cf` | `discovery-20-fluxos-gerar` |
> |---|---|---|
> | Seções preenchidas | Apenas Dados e Estados | **14 seções completas** |
> | Regras de negócio | ❌ Placeholder | ✅ IIBA Business Rule Catalog |
> | Variações/cenários | ❌ Placeholder | ✅ Formato BDD |
> | Diagramas PlantUML | ❌ | ✅ Sequência + Estados |
> | Seção 14 Rastreabilidade | ❌ | ✅ 4 subseções |
> | Auto-verificação | ❌ | ✅ 4 verificadores |
>
> **Prompt para usar a versão industrial:**
> ```
> Gere o FLUXO-F001 em modo industrial a partir do CF-001
> ```
>
> **Quando esta skill ainda pode ser usada:** como "rascunho ultra-rápido" descartável quando não há tempo para o modo industrial — mas o resultado **nunca deve ser entregue sem refinamento posterior**.

---

# [CONTEÚDO ORIGINAL — MANTIDO PARA REFERÊNCIA]

## Papel

Gerar o arquivo inicial de um novo fluxo de discovery a partir de um **Fluxo Candidato (CF)** do `DISC-03-CATALOGO-DE-FLUXOS.md`, preenchendo apenas as seções que o CF fornece com evidência direta do banco. O restante permanece em placeholder — nenhum caminho feliz ou regra de negócio é inventado.

Esta skill é a **versão banco-enriquecida** de `discovery-fluxo-from-template`: enquanto aquela gera apenas o esqueleto, esta preenche automaticamente Dados, Estados e SQLs a partir do CF já produzido.

---

## Pré-requisitos

Antes de executar, verificar:

1. O usuário forneceu o **identificador do CF** (ex.: `CF-001`). Se não fornecido, perguntar.
2. O CF informado existe em `discovery/DISC-03-CATALOGO-DE-FLUXOS.md`.
3. O template oficial está disponível em `.github/skill/discoverytoolkit/discovery-03-fundacao-bootstrap-templates/assets/FLUXO-TEMPLATE-LEGADO.md`.
4. Nenhum arquivo `FLUXO-F001-*.md` (para o CF-001) já existe em `discovery/` — se existir, alertar e aguardar confirmação antes de prosseguir.

---

## Passo a passo

### 1. Ler o CF-alvo no DISC-03

Ler o arquivo completo:

```
discovery/DISC-03-CATALOGO-DE-FLUXOS.md
```

Localizar a seção do CF informado (ex.: `### CF-001 — Gestão de Processos Previdenciários`).

Extrair as seguintes informações:

| Campo | Onde encontrar no CF |
|---|---|
| Nome do fluxo | Linha `### CF-NNN — <Nome>` |
| Domínio de origem | Campo `**Domínio de origem:**` |
| Rótulo de confiança | Campo `**Rótulo de confiança:**` |
| Tabelas principais | Tabela `**Tabelas principais:**` (Tabela, Papel, Volume estimado) |
| Status/situação relevantes | Tabela `**Status/situação relevantes:**` (Coluna, Tabela, Valores mapeados) |
| Eventos observáveis | Lista `**Eventos observáveis no banco:**` |
| SQLs diagnósticas | Bloco de código `**SQLs diagnósticas:**` |

---

### 2. Derivar código do arquivo e slug

**Código do FLUXO:**

- Prefixo `F` + número de três dígitos do CF.
- Exemplo: `CF-001` → `F001`; `CF-012` → `F012`.

**Slug:**

- Pegar o nome do CF (ex.: `Registro de Solicitacao do Cidadao`).
- Converter para kebab-case minúsculo sem acentos.
- Exemplo: `registro-de-solicitacao-do-cidadao`.

**Nome do arquivo de saída:**

```
discovery/FLUXO-F<NNN>-<slug>.md
```

Exemplo: `discovery/FLUXO-F001-registro-de-solicitacao-do-cidadao.md`

---

### 3. Ler o template

Ler o arquivo inteiro diretamente dos assets da skill:

```
.github/skill/discoverytoolkit/discovery-03-fundacao-bootstrap-templates/assets/FLUXO-TEMPLATE-LEGADO.md
```

---

### 4. Gerar o arquivo FLUXO-Fxxx-<slug>.md

Copiar a estrutura completa do template. Aplicar as substituições abaixo e manter todos os placeholders `<...>` nas seções não preenchidas.

#### 4.1 — Cabeçalho obrigatório

```markdown
**Tipo:** Fluxo
**Código:** F<NNN>
**Nome:** <Nome do CF — ex.: Gestão de Processos Previdenciários>
**Escopo:** Schema `prev` do banco previdenciário — evidência exclusivamente do banco (banco-only); sem referências ao novo stack
**Relacionados:** DISC-03-CATALOGO-DE-FLUXOS.md (CF-<NNN>), DADOS-05-MAPA-DADOS.md, DADOS-06-STATUS-E-TRANSICOES.md, DADOS-09-MAPA-FLUXO-TABELAS.md
**Última atualização:** <data de hoje — formato YYYY-MM-DD>
**Palavras-chave do domínio:** <domínio de origem do CF>, banco-only, schema prev, [PEN]
```

#### 4.2 — Bloco "Fonte de verdade"

Inserir logo após o cabeçalho, antes da Seção 1:

```markdown
---

## Fonte de verdade

| Rótulo | Significado |
|---|---|
| `` | Evidência direta do schema `dbo` via SQL Server (DDL, dados reais) |
| `` | Evidência do repositório `C:\projetos\156\api-156-main` |
| `` | Conclusão lógica sem confirmação direta |
| `[PEN]` | Sem evidência — indica lacuna a preencher |

> **Regra:** Nenhum dado neste arquivo entra sem rótulo. Não inventar regras, enums ou valores de status.

---
```

#### 4.3 — Seção "Dados (tabelas e campos críticos)"

Preencher com as tabelas do CF:

```markdown
## 8. Dados (tabelas e campos críticos)

> Fonte: CF-<NNN> em DISC-03-CATALOGO-DE-FLUXOS.md

### Tabelas principais

| Tabela | Papel | Volume estimado |
|---|---|---|
| `prev.<tabela_1>` | <papel> | <volume> |
| `prev.<tabela_2>` | <papel> | <volume> |
<!-- repetir para todas as tabelas do CF -->
```

Se o CF trouxer campos críticos além do volume, incluí-los como subseção:

```markdown
### Campos críticos confirmados

| Tabela | Coluna | Tipo/Valores | Rótulo |
|---|---|---|---|
| `prev.<tabela>` | `<coluna>` | <tipo ou valores mapeados> | |
```

#### 4.4 — Seção "Estados envolvidos"

**Preencher somente se o CF trouxer status/colunas com valores confirmados.**

```markdown
## 7. Estados envolvidos

> Fonte: CF-<NNN> em DISC-03-CATALOGO-DE-FLUXOS.md

| Coluna | Tabela | Valores mapeados | Rótulo |
|---|---|---|---|
| `<coluna>` | `prev.<tabela>` | <valores confirmados> | |
| `<coluna_com_pendencia>` | `prev.<tabela>` | [PEN] | [PEN] |
```

Se a seção do CF tiver campos com `[PEN]` nos valores, preservar essa marcação.

**Se o CF não trouxer status confirmados:** manter o placeholder original do template.

#### 4.5 — Seção "SQL diagnóstico"

Inserir as queries do CF como seção dedicada dentro do FLUXO. Se o template não tiver essa seção explicitamente, adicionar ao final, antes das pendências:

```markdown
## SQL diagnóstico

> Queries derivadas do CF-<NNN>. Executar via MCP `project-0-156-project-1-api156-sqlserver`.

```sql
-- <descrição da query 1>
<SQL 1 copiada verbatim do CF>
```

```sql
-- <descrição da query 2>
<SQL 2 copiada verbatim do CF>
```
```

Copiar as queries **verbatim** do CF, sem modificação de lógica.

#### 4.6 — Bloco "Origem e confiabilidade"

Inserir ao final do arquivo (antes de pendências, se houver seção):

```markdown
---

## Origem e confiabilidade

| Campo | Valor |
|---|---|
| **CF de origem** | CF-<NNN> — <Nome do CF> |
| **Fonte** | `discovery/DISC-03-CATALOGO-DE-FLUXOS.md` |
| **Rótulo de confiança herdado** | <rótulo do CF — ex.:> |
| **Seções preenchidas** | Cabeçalho, Dados (tabelas), Estados (se aplicável), SQL diagnóstico |
| **Seções com placeholder** | Objetivo, Quem usa, Pré-condições, Entradas, Caminho feliz, Variações, Erros, Pontos de atenção |
| **Próximo passo** | Revalidação no código legado — skill `discovery-validacao-banco-codigo` |
```

#### 4.7 — Demais seções

Manter **todos os placeholders originais** do template para:

- Seção 1: Objetivo
- Seção 2: Quem usa
- Seção 3: Pré-condições
- Seção 4: Entradas necessárias
- Seção 5: Caminho feliz
- Seção 6: Variações
- Seção 9: Erros e exceções
- Seção 10: Pontos de atenção operacional

**Nunca narrar** o caminho feliz com base apenas no nome do fluxo ou das tabelas. Toda regra de comportamento deve vir do código legado (etapa posterior).

**Remover** o bloco de orientações do template (blockquote com "ORIENTAÇÕES DE USO DESTE TEMPLATE").

---

### 5. Atualizar DISC-00-INDICE.md

Adicionar o novo FLUXO na tabela "Onde consultar cada assunto":

```markdown
| **Fluxo F<NNN> — <Nome do CF>** (banco-only, a revalidar) | **FLUXO-F<NNN>-<slug>.md** | Seção "Dados" + "Estados" + "SQL diagnóstico" |
```

E adicionar na seção de pendências (se existir):

```markdown
| F<NNN>-P01 | 🟡 Funcional | Revalidar seções 1–6 e 9–10 com código legado | Buscar `<entidade>` em `arquivos-legado.txt` e confirmar com ripgrep | FLUXO-F<NNN>-<slug>.md |
```

---

### 6. Criar snapshot de geração

Criar o arquivo:

```
discovery/SNAP-FLUXO-F<NNN>-GERACAO.md
```

Com o seguinte conteúdo:

```markdown
# SNAP-FLUXO-F<NNN>-GERACAO

**Tipo:** Snapshot de Geração  
**Código:** SNAP-FLUXO-F<NNN>  
**Nome:** Snapshot de Geração do FLUXO-F<NNN> — <Nome do CF>  
**Escopo:** Registro da geração banco-only do FLUXO-F<NNN> a partir do CF-<NNN>  
**Relacionados:** FLUXO-F<NNN>-<slug>.md, DISC-03-CATALOGO-DE-FLUXOS.md (CF-<NNN>)  
**Última atualização:** <YYYY-MM-DD>  
**Palavras-chave do domínio:** geração, banco-only, snapshot, CF-<NNN>, FLUXO-F<NNN>

---

## CF de origem

| Campo | Valor |
|---|---|
| Identificador | CF-<NNN> |
| Nome | <Nome do CF> |
| Rótulo de confiança | <rótulo do CF> |
| Domínio de origem | <domínio> |

## Arquivos gerados

| Arquivo | Ação |
|---|---|
| `discovery/FLUXO-F<NNN>-<slug>.md` | Criado |
| `discovery/SNAP-FLUXO-F<NNN>-GERACAO.md` | Criado (este arquivo) |
| `discovery/DISC-00-INDICE.md` | Atualizado — entrada adicionada |

## Seções preenchidas

| Seção | Conteúdo | Rótulo |
|---|---|---|
| Cabeçalho | Código, Nome, Escopo, Relacionados, Palavras-chave | |
| Dados — Tabelas principais | <N> tabelas extraídas do CF | |
| Estados envolvidos | <preenchido / placeholder — indicar> | / [PEN] |
| SQL diagnóstico | <N> queries copiadas do CF | |
| Origem e confiabilidade | Metadados de rastreabilidade | — |

## Seções com placeholder (a preencher)

- Seção 1: Objetivo
- Seção 2: Quem usa
- Seção 3: Pré-condições
- Seção 4: Entradas necessárias
- Seção 5: Caminho feliz
- Seção 6: Variações
- Seção 9: Erros e exceções
- Seção 10: Pontos de atenção operacional

## Pendências abertas

| ID | Nível | O que falta | Como confirmar |
|---|---|---|---|
| P-01 | 🟡 Funcional | Revalidar seções de comportamento com código legado | Buscar `<entidade>` em `arquivos-legado.txt`; usar `rg` no legado |
| P-02 | 🟡 Dados | Confirmar semântica dos valores de status `[PEN]` | Query `SELECT DISTINCT <coluna> FROM prev.<tabela>` via MCP |

---

> **Snapshot imutável** — não atualizar após criação. Para o estado atual do FLUXO, consultar `FLUXO-F<NNN>-<slug>.md`.
```

---

### 7. Registrar pendências (OBRIGATÓRIO)

Após criar o FLUXO e o snapshot, revisar a Seção 13 (Pendências e lacunas) do FLUXO e registrar qualquer `[PEN]` encontrado.

Pendências são rastreadas **dentro do próprio arquivo FLUXO**, não em documento separado.

---

### 8. Instruir próximo passo

Após concluir, informar ao usuário:

> **Arquivo gerado:** `discovery/FLUXO-F<NNN>-<slug>.md`
>
> **Snapshot:** `discovery/SNAP-FLUXO-F<NNN>-GERACAO.md`
>
> **Seções preenchidas (banco):** Dados, Estados (se aplicável), SQL diagnóstico.
>
> **Próximo passo recomendado — Revalidação no legado:**
>
> Use `discovery/arquivos-legado.txt` para localizar arquivos do domínio `<domínio>` no código legado (ex.: `rg -l "<entidade>" discovery/arquivos-legado.txt`). Para cada seção com placeholder, confirmar com evidência de banco ou código legado antes de preencher. Consulte `DADOS-06` para status e `DADOS-09` para tabelas.
>
> Ao concluir o preenchimento completo, executar: `Consolide as pendências e atualize o DISC-90`.

---

## Restrições obrigatórias

- **Não inventar** caminho feliz, regras de negócio, condições de rejeição ou valores de status não presentes no CF.
- **Não usar código legado como fonte** neste passo — apenas o CF do DISC-03 e, como apoio opcional, DADOS-05/06/09/10.
- **Não mencionar o novo stack** como fonte de qualquer dado.
- **Não preencher** seções de comportamento (Objetivo, Caminho feliz, Variações, Erros) com conteúdo deduzido apenas do nome do fluxo.
- **Não modificar** as queries do CF — copiar verbatim.
- **Não remover** seções do template — manter placeholders onde não há dado confirmado.
- Toda afirmação que entrar no arquivo deve carregar um dos quatro rótulos de confiança.
- O bloco "Orientações de uso" do template deve ser **removido** do arquivo gerado.

---

## Referências adicionais

- Para fontes, rótulos e dependências, ver [references/REFERENCE.md](references/REFERENCE.md)
- Para o template estrutural, ver `.cursor/skills/discovery-bootstrap-templates/assets/FLUXO-TEMPLATE-LEGADO.md`
- Para o catálogo de CFs, ver `discovery/DISC-03-CATALOGO-DE-FLUXOS.md`
