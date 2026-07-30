---
name: clarification
description: "Identifica e resolve ambiguidades em especificações de features. Executa varredura estruturada de cobertura, gera questões prioritizadas e integra respostas direto no arquivo de especificação usando handoff interativo. Use quando precisa clarificar requisitos, reduzir risco de rework ou preparar especificações para implementação."
---

# Clarification Skill — Disambiguação Estruturada de Especificações

> **Quando usar:** Especificações vagas, features complexas, requisitos incompletos, antes de implementação ou planning.

---

## O que Esta Skill Faz

1. **Varredura de Cobertura:** Analisa a especificação em 10 categorias (escopo funcional, modelo de dados, UX, não-funcionais, integrações, edge cases, constraints, terminologia, sinais de conclusão, misc).

2. **Geração de Questões:** Cria até 5 questões prioritizadas baseadas em impacto × incerteza, com respostas múltipla-escolha ou curtas.

3. **Interação Sequencial via Handoff:** Apresenta UMA questão por vez no chat com:
   - Recomendação técnica destacada
   - Tabela com opções e descrições
   - Validação de resposta do usuário

4. **Integração Incremental:** Após cada resposta, atualiza a especificação com:
   - Seção de Atualizações com histórico
   - Clarificações incorporadas em seções relevantes
   - Normalização de terminologia
   - Remoção de placeholders obsoletos

5. **Relatório Final:** Resumo de questões, caminho do arquivo atualizado, seções modificadas e cobertura de categorias.

---

## Estrutura de Perguntas

### Taxonomia de Categorias

```
├── Functional Scope & Behavior
│   ├── Core user goals & success criteria
│   ├── Explicit out-of-scope declarations
│   └── User roles / personas differentiation
├── Domain & Data Model
│   ├── Entities, attributes, relationships
│   ├── Identity & uniqueness rules
│   ├── Lifecycle/state transitions
│   └── Data volume / scale assumptions
├── Interaction & UX Flow
│   ├── Critical user journeys / sequences
│   ├── Error/empty/loading states
│   └── Accessibility or localization notes
├── Non-Functional Quality Attributes
│   ├── Performance (latency, throughput)
│   ├── Scalability (horizontal/vertical, limits)
│   ├── Reliability & availability
│   ├── Observability (logging, metrics, tracing)
│   ├── Security & privacy (authN/Z, data protection)
│   └── Compliance / regulatory constraints
├── Integration & External Dependencies
│   ├── External services/APIs and failure modes
│   ├── Data import/export formats
│   └── Protocol/versioning assumptions
├── Edge Cases & Failure Handling
│   ├── Negative scenarios
│   ├── Rate limiting / throttling
│   └── Conflict resolution (concurrent edits)
├── Constraints & Tradeoffs
│   ├── Technical constraints (language, storage, hosting)
│   └── Explicit tradeoffs or rejected alternatives
├── Terminology & Consistency
│   ├── Canonical glossary terms
│   └── Avoided synonyms / deprecated terms
├── Completion Signals
│   ├── Acceptance criteria testability
│   └── Measurable Definition of Done
└── Misc / Placeholders
    ├── TODO markers / unresolved decisions
    └── Ambiguous adjectives lacking quantification
```

### Critérios de Qualidade de Pergunta

✅ **Deve ser incluída se:**

- Resposta materialmente impacta arquitetura, modelagem de dados, decomposição de tarefas, design de testes, UX, ou prontidão operacional
- Reduz risco de rework downstream
- Previne desalinhamento em testes de aceitação

❌ **Deve ser excluída se:**

- Informação é melhor deferida para fase de planning
- Clarificação não impacta estratégia de implementação ou validação
- É questão puramente estilística ou trivial

---

## Fluxo de Interação com Handoff

### Passo 1: Carregar e Analisar Especificação

```
Especificação → Varredura Estruturada → Mapa de Cobertura (interno)
                                        ├── Clear ✅
                                        ├── Partial ⚠️
                                        └── Missing ❌
```

### Passo 2: Gerar Questões Prioritizadas

```
Categorias Partial/Missing → Candidatos de Questão → Priorização (Impact × Uncertainty)
                                                     ↓
                                            Max. 5 Questões Selecionadas
```

### Passo 3: Loop Questão-Resposta (Handoff Interativo)

**Formato de Pergunta Múltipla-Escolha:**

```markdown
### [PRIORIDADE] **[PONTO DE DECISÃO]**

**Questão:** [Pergunta clara e específica]

**Recomendado:** Opção [X] - [Justificativa técnica 1-2 linhas]

| Opções | Descrição              |
| ------ | ---------------------- |
| A      | [Descrição da opção A] |
| B      | [Descrição da opção B] |
| C      | [Descrição da opção C] |

**Responda com:** A letra da opção (ex: "A"), "sim"/"recommended" para aceitar,
ou sua própria resposta curta (≤5 palavras).
```

**Formato de Pergunta Aberta-Curta:**

```markdown
### [PRIORIDADE] **[PONTO DE DECISÃO]**

**Questão:** [Pergunta clara]

**Sugerido:** [Resposta padrão baseada em best practices] - [Justificativa técnica]

**Formato:** Resposta curta (≤5 palavras).
Responda "sim"/"suggested" para aceitar, ou sua própria resposta.
```

### Passo 4: Validação e Integração

Após aceitação de resposta:

1. ✅ Validar resposta (múltipla-escolha ou ≤5 palavras)
2. 📝 Registrar em memória (não salva em disco ainda)
3. 📄 Aplicar a seção relevante da especificação
4. 💾 Salvar arquivo atomicamente
5. ➡️ Próxima questão

### Passo 5: Relatório Final

```
Questões Perguntadas: N/5 ✅
Caminho do Arquivo: [path]
Seções Modificadas: [lista]

Cobertura Final:
├── Clear      ✅ [N categorias]
├── Resolved   ⚡ [N categorias atualizadas]
├── Deferred   ⏳ [N categorias, rationale]
└── Outstanding ❌ [N categorias, rationale]

Próximo comando sugerido: [recomendação]
```

---

## Estrutura de Atualização na Especificação

### Seção `## Updates`

#### Criação Automática (primeira clarificação)

```markdown
## Updates

| Data da Atualização | Autor da Atualização | Descrição da Atualização                                |
| ------------------- | -------------------- | ------------------------------------------------------- |
| 19/03/2026          | AI Clarification Bot | Incorporated clarification: Q: [question] → A: [answer] |
| ...                 | ...                  | ...                                                     |

### Session 2026-03-19

- Q: [questão 1] → A: [resposta 1]
- Q: [questão 2] → A: [resposta 2]
```

#### Regra de Integração por Categoria

| Categoria de Ambiguidade    | Seção Alvo                               | Ação                                                               |
| --------------------------- | ---------------------------------------- | ------------------------------------------------------------------ |
| Escopo funcional            | `## Functional Requirements`             | Adiciona/clarifica bullet                                          |
| Distinção de ator           | `## User Stories` ou `## Actors`         | Atualiza role, constraint, cenário                                 |
| Forma de dados / entidades  | `## Data Model`                          | Adiciona campos, tipos, relacionamentos, constraints               |
| Atributo não-funcional vago | `## Non-Functional / Quality Attributes` | Converte adjetivo em métrica ou alvo explícito                     |
| Edge case / erro            | `## Edge Cases / Error Handling`         | Novo bullet ou subsection                                          |
| Conflito de terminologia    | Todos (normaliza)                        | Substitui termo, retém original com `(formerly "X")` se necessário |

#### Validação Pós-Integração

- ✅ Uma bullet por resposta aceita (sem duplicatas)
- ✅ Total de perguntas perguntadas ≤ 5
- ✅ Sem placeholders vagos obsoletos ("robust", "intuitive" sem quantificação)
- ✅ Sem contradições (statements antigos removidos se invalidados)
- ✅ Estrutura Markdown válida; novos headings: `## Clarifications`, `### Session YYYY-MM-DD`
- ✅ Terminologia consistente (mesmo termo canônico em todos os lugares)

---

## Regras Comportamentais

### ✅ Proceder Com Caução

- Sempre confirmar: "Nenhuma ambiguidade crítica detectada?" antes de pular clarificação.
- Se arquivo de especificação não existe, instruir usuário a criar primeiro (não crie spec nova aqui).
- Máximo 5 perguntas totais por sessão; retries para uma pergunta NÃO contam como nova pergunta.

### ❌ Evitar

- Questões especulativas sobre tech stack (a menos que bloqueie funcionalidade).
- Perguntas de preferência estilística ou trivial.
- Mais de 5 questões (mesmo que houver mais categorias não resolvidas).
- Contradições entre questões e respostas anteriores.

### ⚡ Sinais de Encerramento

Pare de perguntar quando:

- Todas as ambiguidades críticas forem resolvidas
- Usuário sinaliza "pronto", "done", "fim", "sem mais perguntas"
- Você fez 5 perguntas
- Fila de questões se esvaziar (nenhuma questão significativa restante)

### 📢 Sinalização de Conclusão Incompleta

Se quota de perguntas (5) se esgotar COM categorias não resolvidas (high-impact):

- Listar explicitamente como **Deferred** com rationale
- Recomendar rodar `/clarify` novamente depois

---

## Integração com Handoff no VSCode Chat

### Invocação no Chat

```markdown
/clarification [caminho/para/especificacao.md]
```

**Exemplos:**

- `/clarification documentacao/features/login.md`
- `/clarification src/specs/payment-integration.md`

### Fluxo Interativo

1. **Primeira mensagem:** Análise & 1ª questão
2. **Resposta do usuário:** Validação, integração, 2ª questão
3. **Repetir:** Até conclusão ou sinal de parada
4. **Última mensagem:** Relatório final + próximos passos

### Failsafe: Nenhuma Ambiguidade

```
Análise realizada. Status:

| Categoria | Status |
|-----------|--------|
| Functional Scope & Behavior | ✅ Clear |
| Domain & Data Model | ✅ Clear |
| ... | ✅ Clear |

Nenhuma ambiguidade crítica detectada.
A especificação está pronta para implementação.

Próximo: Prosseguir para planning/design ou rodar /architecture.
```

---

## Referências

- **Prompt Original:** `.github/prompts/clarify.prompt.md`
- **Arquivo Especificação:** Ser fornecido pelo usuário ou identificado automaticamente
- **Output:** Arquivo de especificação atualizado + histórico de clarificações

---

## Troubleshooting

### "Arquivo não encontrado"

```
❌ Não consegui localizar a especificação em [caminho].

Opções:
1. Forneça o caminho correto: /clarification [caminho/correto]
2. Crie a especificação primeiro:
   - Use /featurize ou /spec-driven-workflow
   - Depois rodar /clarification
```

### "Resposta ambígua"

```
❌ Resposta não clara. Você respondeu: "[resposta]"

Opções esperadas: A, B, C, D, ou resposta curta (≤5 palavras).

Reforme sua resposta ou escolha uma opção.
```

### "Quota de perguntas atingida com ambiguidades restantes"

```
⚠️ Limite de 5 perguntas atingido. Categorias ainda com ambiguidades:
- [Categoria A]: [Rationale por que deferred]
- [Categoria B]: ...

Recomendação: Rodar `/clarification` novamente após planning/design
para refinar essas áreas.
```

---

## Quando Usar Esta Skill

✅ **Use quando:**

- Feature specification está incompleta ou vaga
- Antes de iniciar planning ou design
- Requisitos foram recolhidos mas precisam de refinamento
- Múltiplas interpretações possíveis existem
- Você quer reduzir rework risk antes de implementação
- Testes de aceitação ainda não estão claros

❌ **Não use quando:**

- Especificação está completa e todos concordam
- Spike exploratório (pode pular, mas avise que rework risk aumenta)
- Simples bug fix ou pequenan tarefa

---

## Exemplo de Sessão Completa

**Usuário:**

```
/clarification documentacao/features/user-authentication.md
```

**Bot (Análise + 1ª Questão):**

```
## Análise de Cobertura

Especificação: documentacao/features/user-authentication.md

| Categoria | Status |
|-----------|--------|
| Functional Scope | ⚠️ Partial |
| Domain & Data | ⚠️ Partial |
| Interaction & UX | ✅ Clear |
| Non-Functional | ❌ Missing |
| ...

Geradas 5 questões prioritizadas. Iniciando loop...

---

### **P0 - Password Storage & Hashing**

**Questão:** Qual é o requisito mínimo para armazenamento de senhas?

**Recomendado:** Opção A - PBKDF2 é padrão industrial para autenticação
com excelente suporte em frameworks enterprise.

| Opções | Descrição |
|--------|-----------|
| A | PBKDF2 (ou equivalente bcrypt) com 10k+ iterações |
| B | SHA-256 com salt aleatório (rápido, pouco overhead) |
| C | Plaintext com TLS (máxima performance) |
| D | Hardware security module (HSM) com PKI |

**Responda com:** A letra (ex: "A"), "sim"/"recommended", ou sua resposta (≤5 palavras).
```

**Usuário:**

```
A
```

**Bot (Integração + 2ª Questão):**

```
✅ Resposta registrada: PBKDF2 (ou equivalente bcrypt) com 10k+ iterações

Integrando... arquivo atualizado.

| Data | Autor | Descrição |
|------|-------|-----------|
| 19/03/2026 | AI Clarification Bot | Q: Password storage requirement? → A: PBKDF2 with 10k+ iterations |

**Seção atualizada:** Non-Functional → Security & Privacy
- Password hashing: PBKDF2 (or equivalent bcrypt) with ≥10,000 iterations

---

### **P1 - 2FA Requirement**

**Questão:** 2FA é obrigatório para todos os usuários ou opcional?

**Recomendado:** Opção B - 2FA opcional permite adoção gradual,
reduz atrito inicial mantendo segurança para usuários sensíveis.

| Opções | Descrição |
|--------|-----------|
| A | 2FA obrigatório para todos |
| B | 2FA optativo, usuário ativa quando quiser |
| C | 2FA obrigatório só para admins |

**Responda com:** A letra, "sim"/"recommended", ou resposta curta.
```

**[Continua até 5 questões ou conclusão...]**

**Bot (Relatório Final):**

```
## ✅ Clarificações Completadas

**Questões:** 3 de 5 perguntadas e respondidas

**Arquivo:** documentacao/features/user-authentication.md

**Seções Atualizadas:**
- Functional Requirements (2 clarificações)
- Non-Functional / Security (1 clarificação)
- Data Model (0 clarificações)

**Cobertura Final:**

| Categoria | Status | Observações |
|-----------|--------|-------------|
| Functional Scope | ✅ Clear | Resolvido: roles e escopo |
| Domain & Data | ⚠️ Partial | Deferred: estrutura de 2FA pode esperar planning |
| Interaction & UX | ✅ Clear | Já coberto |
| Non-Functional | ✅ Resolved | Adicionado: password hashing, 2FA scope |
| ... | ✅ Clear | ... |

**Outstanding/Deferred:**
- Email verification flow: exceeds quota, melhor refinar em design phase
- Rate limiting per IP/user: baixo impacto, plan-level decision

**Próximo comando recomendado:**
```

/planning-and-task-breakdown documentacao/features/user-authentication.md

```

Ou, se quiser aprofundar ambiguidades restantes:
```

/clarification documentacao/features/user-authentication.md

```

```

---

## Histórico de Versão

| Versão | Data       | Mudanças                                                                 |
| ------ | ---------- | ------------------------------------------------------------------------ |
| 1.0    | 19/03/2026 | Skill inicial, transformado de clarify.prompt.md com handoff integration |
