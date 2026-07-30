---
name: copilot-planning
description: "Planejamento operacional de execução do Copilot com técnica de onda, lote e waveless, incluindo rastreabilidade, histórico em diretório planning e regra de precedência por última onda. Suporta escalonamento automático de ondas por complexidade. Use quando a tarefa exigir execução segura por etapas, controle anti-hallucination, checklist formal e registro incremental de melhorias/erros."
---

# Copilot Planning

Skill para execução de tarefas com **planejamento estruturado**, reduzindo risco de perda de contexto, retrabalho e alucinação.

Este skill padroniza a execução em:

- **Onda (Wave):** macrofase com objetivo claro e entregáveis verificáveis.
- **Lote (Batch):** conjunto de ações menores dentro da onda, com foco em validação incremental.
- **Waveless:** fluxo contínuo e leve para tarefas muito pequenas, mantendo rastreabilidade mínima.

---

## Quando usar este skill

Use este skill quando:

- a tarefa tiver múltiplas etapas, dependências ou risco de inconsistência;
- houver necessidade de histórico de execução no workspace;
- for importante controlar mudanças por requisito ao longo de várias iterações;
- for necessário mitigar alucinações por meio de checkpoints formais.

Palavras-gatilho comuns: **planejamento**, **onda**, **lote**, **wave**, **waveless**, **checklist**, **execução por etapas**, **rastreabilidade**.

---

## Regras mandatórias

1. **Toda execução de tarefa deve ter onda e lotes** (mesmo que mínimos), salvo caso explicitamente classificado como _waveless_.
2. **Toda onda deve gerar histórico persistente** em diretório `planning/` na raiz do workspace.
    - 2.a **Se o diretório `planning/` ou subdiretórios/arquivos da onda não existirem, o agente deve criá-los automaticamente antes de continuar:**
        - `planning/`
        - `planning/onda-XXX/`
        - `1-plano.md`, `2-checklist.md`, `3-resumo.md`, `4-melhorias-e-erros.md`
3. **Não executar lote sem checklist da onda**.
4. **Não concluir onda sem resumo e registro de melhorias/erros**.
5. **Se o mesmo requisito aparecer alterado em múltiplas ondas, sempre prevalece a última onda executada**.
6. **Toda decisão deve ser baseada em evidência do workspace** (evitar suposição).
7. **`3-resumo.md` e `4-melhorias-e-erros.md` devem ser preenchidos de forma incremental**, à medida que cada lote for executado — nunca somente ao final da onda.
8. **Alta complexidade exige escalonamento automático de ondas**: se a demanda for identificada como complexa (ver seção abaixo), o agente deve planejar e criar todas as ondas necessárias antes de iniciar a execução.
9. **Após gerar a onda, o plano deve ser disponibilizado ao usuário por handoff e a execução deve aguardar aprovação explícita do usuário** antes do primeiro lote.
10. **Toda interação com o usuário no contexto deste skill deve ocorrer por meio de handoff**.

---

## Avaliação de complexidade e escalonamento de ondas

**Antes de iniciar qualquer execução**, o agente deve avaliar a complexidade da demanda usando os critérios abaixo:

### Indicadores de alta complexidade (exigem múltiplas ondas)

- Mais de 3 domínios/áreas de impacto distintos;
- Dependências entre partes que precisam ser entregues em sequência;
- Risco de inconsistência se tudo for feito em uma única passagem;
- Escopo estimado superior a 5 lotes;
- Presença de decisões arquiteturais que afetam etapas posteriores;
- Necessidade de validação intermediária antes de prosseguir.

### Comportamento esperado

- **Baixa complexidade:** 1 onda com lotes internos, ou _waveless_.
- **Média complexidade:** 2 a 3 ondas planejadas antes da execução.
- **Alta complexidade:** 4 ou mais ondas — o agente deve criar **todas as pastas e planos de onda antes de executar a primeira**, garantindo visão completa do escopo.

> O número de ondas não é fixo. O agente deve criar quantas ondas forem necessárias para cobrir a demanda com segurança e rastreabilidade.

### Registro do escalonamento

Ao identificar alta complexidade, registrar no `1-plano.md` da primeira onda:

- justificativa do escalonamento;
- número total de ondas planejadas;
- mapa resumido de cada onda (objetivo + critério de conclusão).

---

## Estrutura obrigatória no workspace

Ao iniciar o planejamento, garantir:

- diretório raiz: `planning/`, deve ser criado na raiz do workspace
- subpastas por onda enumerada, exemplo:
    - `planning/onda-001/`
    - `planning/onda-002/`
    - `planning/onda-003/`

Cada pasta de onda deve conter exatamente estes arquivos mínimos:

1. `1-plano.md`
2. `2-checklist.md`
3. `3-resumo.md`
4. `4-melhorias-e-erros.md`

> Essas subpastas devem ser mantidas como **histórico permanente do planejamento do workspace**.

---

## Técnica de Onda, Lote e Waveless

### 1) Onda (Wave)

A onda organiza o objetivo macro da execução.

Cada onda deve definir:

- objetivo da onda;
- requisitos/itens-alvo;
- critérios de conclusão;
- riscos conhecidos;
- dependências.

#### Critérios de qualidade da onda

- objetivo específico e verificável;
- escopo fechado (sem crescimento descontrolado);
- saída auditável (arquivos, decisões e validações registradas).

### 2) Lote (Batch)

Lote é o recorte operacional da onda.

Características:

- pequeno o suficiente para validação rápida;
- orientado a resultado concreto (ex.: atualizar arquivo, validar requisito, revisar conflito);
- com status explícito: `pendente`, `em andamento`, `concluído`, `bloqueado`.

#### Regras de execução por lote

- executar um lote por vez quando houver dependência;
- validar antes de avançar para o próximo;
- **ao concluir cada lote**, atualizar imediatamente `3-resumo.md` com o que foi feito e `4-melhorias-e-erros.md` com o que foi identificado — não aguardar o fim da onda.

### 3) Waveless

Waveless é permitido para tarefas simples e de baixo risco, mas **não elimina governança**.

Quando usar:

- tarefa atômica com impacto local;
- sem dependências críticas;
- sem alteração transversal de requisitos.

Mesmo em waveless, registrar minimamente:

- objetivo;
- ação executada;
- evidência/resultado;
- riscos residuais.

> Se o escopo crescer, migrar imediatamente de _waveless_ para modelo formal de **onda + lotes**.

---

## Fluxo operacional obrigatório

1. **Avaliar complexidade** da demanda (ver seção de escalonamento).
2. Classificar demanda: **onda+lotes** ou **waveless**.
3. Garantir existência de `planning/`.
4. Se onda+lotes:
    - criar todas as pastas de onda necessárias (`onda-XXX`) com base na complexidade avaliada;
    - criar `1-plano.md`, `2-checklist.md`, `3-resumo.md`, `4-melhorias-e-erros.md` em cada pasta.
5. Definir lotes no `1-plano.md` e itens verificáveis no `2-checklist.md`.
6. **Disponibilizar o plano ao usuário por handoff e aguardar aprovação explícita** antes de iniciar qualquer lote.
7. Executar lotes com validação incremental somente após aprovação.
8. **Após cada lote concluído:** atualizar `3-resumo.md` com o que foi executado e `4-melhorias-e-erros.md` com o que foi identificado.
9. Ao finalizar a onda, consolidar `3-resumo.md` e `4-melhorias-e-erros.md` com visão completa da onda.
10. Em conflitos entre ondas para o mesmo requisito, aplicar regra de precedência da última onda.

---

## Regra de precedência entre ondas (conflito de requisito)

Se um mesmo requisito foi alterado em mais de uma onda:

- considerar válida **a alteração da última onda executada**;
- registrar no `3-resumo.md` da onda mais recente a substituição da decisão anterior;
- manter referência à onda anterior para auditabilidade.

Ordem de precedência:

1. maior número da onda (ex.: `onda-014` > `onda-013`)
2. em caso excepcional de empate, considerar timestamp mais recente do registro de execução.

---

## Template mínimo dos arquivos da onda

### `1-plano.md`

- Identificação da onda
- Objetivo
- Escopo (in/out)
- Lotes planejados
- Dependências
- Critérios de conclusão
- *(Se onda-001 com escalonamento):* mapa de todas as ondas planejadas

### `2-checklist.md`

- Itens verificáveis por lote
- Critérios de aceite
- Status por item (`[ ]`, `[x]`, `[-] bloqueado`)

### `3-resumo.md`

> **Preenchimento incremental:** atualizar após cada lote concluído. Consolidar ao final da onda.

- O que foi executado (por lote)
- Evidências
- Resultados alcançados
- Requisitos impactados
- Decisões finais da onda

### `4-melhorias-e-erros.md`

> **Preenchimento incremental:** registrar imediatamente ao identificar erros ou oportunidades durante a execução dos lotes.

- Erros encontrados
- Causa provável
- Correção aplicada
- Risco residual
- Sugestões de melhoria contínua

---

## Boas práticas anti-hallucination

- quebrar escopo em lotes pequenos com validação objetiva;
- registrar fontes/evidências antes de concluir cada lote;
- não preencher lacunas com suposição;
- sempre reconciliar mudanças de requisito com histórico de ondas anteriores;
- usar o resumo da onda para consolidar verdade operacional;
- nunca assumir que uma onda é suficiente sem avaliar a complexidade da demanda.

---

## Checklist rápido de conformidade

- [ ] Complexidade da demanda foi avaliada antes de iniciar.
- [ ] Foi criado/validado `planning/` na raiz.
- [ ] A execução está organizada em onda e lotes (ou waveless justificado).
- [ ] O número de ondas reflete a complexidade real da demanda.
- [ ] As pastas de todas as ondas necessárias foram criadas antes de executar a primeira.
- [ ] A pasta de cada onda foi enumerada corretamente.
- [ ] Existem os 4 arquivos obrigatórios em cada onda.
- [ ] Lotes foram executados com validação incremental.
- [ ] `3-resumo.md` e `4-melhorias-e-erros.md` foram atualizados após cada lote (não apenas ao final).
- [ ] Conflitos de requisito entre ondas respeitam a última onda executada.

---

## Resultado esperado

Com este skill, o Copilot executa tarefas com:

- previsibilidade;
- rastreabilidade histórica;
- escalonamento automático proporcional à complexidade real da demanda;
- menor risco de perda de dados/contexto;
- redução de alucinação por checkpoints formais e registro incremental;
- decisão consistente quando houver múltiplas ondas para o mesmo requisito.
