---
description: Banco de questões da skill clarification com exemplos para cada categoria
applyTo: clarification
---

# Clarification — Question Bank & Taxonomy Mapping

Mapeamento de categorias de ambiguidade para questões concretas, detalhes de priorização, e exemplos de respostas esperadas.

---

## Estrutura Geral

### Taxonomia (10 Categorias)

```text
1. Functional Scope & Behavior
2. Domain & Data Model
3. Interaction & UX Flow
4. Non-Functional Quality Attributes
5. Integration & External Dependencies
6. Edge Cases & Failure Handling
7. Constraints & Tradeoffs
8. Terminology & Consistency
9. Completion Signals
10. Misc / Placeholders
```

### Critério de Priorização

```text
Priority = Impact × Uncertainty × Coverage_Gap

Impact:        O quanto a decisão afeta arquitetura/design/tests (1-5)
Uncertainty:   Quão vaga a especificação atual é (1-5)
Coverage_Gap:  Importância relativa entre as categorias (1-3)

P0 (Crítico):   Priority >= 15 (ex: 5×3×1 ou 5×2×2)
P1 (Alto):      Priority 8-14
P2 (Médio):     Priority 4-7
P3 (Baixo):     Priority < 4
```

---

## Categoria 1: Functional Scope & Behavior

### Descrição

Define o que o sistema FAZ vs. O QUE NÃO FAZ. Ambiguidade aqui impacta:

- Escopo de implementação (qual feature)
- Critérios de aceitação (que testamos)
- Gestão de expectativa do stakeholder

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | Core goals explícito, out-of-scope declarado, personas/roles distintas |
| ⚠️ Partial | Goals descritos mas não quantificados, alguns roles implícitos |
| ❌ Missing | Goals vagos (ex: "sistema rápido", "user-friendly"), sem out-of-scope |

### Template de Questão

```
**Prioridade:** P0-P1 (alta, bloqueia implementação)

**Categoria:** Functional Scope & Behavior

**Estrutura:**
- Contexto: Cita frase vaga da especificación
- Impacto: Descreve consequência (3-5 palavras)
- Recomendação: Baseada em best-practice / projeto anterior
```

### Exemplos de Questão

#### Exemplo 1.1: Definição de "User Search"

**Questão Pattern:**

```
A especificação menciona "usuário pode buscar documentos",
mas não clarifica QUEM pode buscar (todos? ou só authenticated users?).
```

**Handoff:**

```json
{
  "title": "Funcional: Quem pode buscar?",
  "description": "Busca pública ou somente usuários autenticados? Impacta autenticação, caching, auditoria.",
  "options": [
    {
      "label": "A",
      "description": "Públic (anyone, sem login)",
      "recommended": false
    },
    {
      "label": "B",
      "description": "Authenticated only (login obrigatório)",
      "recommended": true
    },
    {
      "label": "C",
      "description": "Ambos: public preview + authenticated Advanced",
      "recommended": false
    }
  ]
}
```

**Resposta Esperada:** A, B, C, ou short answer
**Integração:** Atualiza `## Functional Requirements` com bullet: "Search access: [A/B/C choice]"

#### Exemplo 1.2: Scope de "Create Document"

**Questão Pattern:**

```
Feature menciona "criar documentos". Escopo inclui
uploader de arquivo, editor de texto, ou ambos?
```

**Handoff:**

```json
{
  "title": "Funcional: Como documentos são criados?",
  "description": "Só upload de arquivo existente, editor in-browser, ou ambas as opções? Afeta UX, storage, processing.",
  "options": [
    {
      "label": "A",
      "description": "Upload de arquivo (Ex: .pdf, .docx)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Editor de texto in-browser",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Ambas (upload + editor)",
      "recommended": false
    }
  ]
}
```

---

## Categoria 2: Domain & Data Model

### Descrição

Define COMO os dados são estruturados, relacionados e evoluem. Ambiguidade aqui bloqueia:

- Design de banco de dados
- APIs (contratos)
- Migração de dados

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | Entidades descritas, tipos claros, relacionamentos explícitos, lifecycle definido |
| ⚠️ Partial | Entidades mencionadas mas sem tipos, lifecycle implícito |
| ❌ Missing | Sem modelo de dados ou apenas exemplos vagos |

### Exemplos de Questão

#### Exemplo 2.1: Identificador Único

**Questão Pattern:**

```
Especificação menciona "documento" mas não clarifica
como são identificados uniquamente. UUID, auto-increment, ou string slug?
```

**Handoff:**

```json
{
  "title": "Dados: Como documentos são identificados?",
  "description": "UUID garante confiabilidade em distribuído; auto-increment é simples; slug é human-readable. Afeta API design, sharding.",
  "options": [
    {
      "label": "A",
      "description": "UUID (universally unique, bom para distribuído)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Auto-increment integer (simples, rápido)",
      "recommended": false
    },
    {
      "label": "C",
      "description": "String slug (human-readable, ex: 'user-guide-v2')",
      "recommended": false
    }
  ]
}
```

#### Exemplo 2.2: Relacionamento Usuário-Documento

**Questão Pattern:**

```
Um documento pode ter múltiplos autores?
Ou cada documento tem exatamente um owner?
```

**Handoff:**

```json
{
  "title": "Dados: Autoria de documentos (1:1 vs. N:N)",
  "description": "Afeta design de tabela, queries de permissão, histórico de mudanças.",
  "options": [
    {
      "label": "A",
      "description": "1:1 — todo doc tem exatamente 1 owner",
      "recommended": true
    },
    {
      "label": "B",
      "description": "N:N — múltiplos autores compartilham documento",
      "recommended": false
    }
  ]
}
```

---

## Categoria 3: Interaction & UX Flow

### Descrição

Define como USUÁRIO interage com o sistema. Ambiguidade aqui impacta:

- UX design
- Testes de aceitação (cenários)
- Acessibilidade / i18n

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | User journeys descritas, erro/empty/loading states mencionados, acessibilidade declarada |
| ⚠️ Partial | Happy path descrito, edge cases (erros, vazio) implícitos |
| ❌ Missing | Sem fluxo de usuário ou muito vago |

### Exemplos de Questão

#### Exemplo 3.1: Comportamento de "Search Not Found"

**Questão Pattern:**

```
Quando busca retorna 0 resultados, qual é o comportamento esperado?
- Mensagem amigável?
- Sugestões (you meant)?
- Histórico de buscas recentes?
```

**Handoff:**

```json
{
  "title": "UX: Quando busca não encontra resultados",
  "description": "Afeta experiência do usuário e carga de servidor (suggestions requerem compute).",
  "options": [
    {
      "label": "A",
      "description": "Mensagem simples 'Nenhum resultado encontrado'",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Mensagem + sugestões de busca alternativa",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Histórico de buscas recentes do usuário",
      "recommended": false
    }
  ]
}
```

#### Exemplo 3.2: Comportamento de Erro de Rede

**Questão Pattern:**

```
Se busca falhar por erro de rede, usuário vê:
- Retry automático?
- Retry manual (botão)?
- Fallback para cache?
```

**Handoff:**

```json
{
  "title": "UX: Erro de rede em busca",
  "description": "Retry automático melhora UX mas consome recursos; manual é seguro mas pode frustrar.",
  "options": [
    {
      "label": "A",
      "description": "Mensagem de erro + botão Retry manual",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Retry automático 3x com backoff exponencial",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Usar cache de resultados anteriores se disponível",
      "recommended": false
    }
  ]
}
```

---

## Categoria 4: Non-Functional Quality Attributes

### Descrição

Define como SISTEMA EXECUTA (velocidade, confiabilidade, segurança). Ambiguidade aqui causa:

- SLA breaches
- Incidentes de segurança
- Escalabilidade issues

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | Performance targets quantificados (ms), uptime %, security reqs explícitos |
| ⚠️ Partial | Alguns atributos mencionados, faltam métricas concretas |
| ❌ Missing | Adjetivos vagos ("rápido", "seguro") sem numbers |

### Exemplos de Questão

#### Exemplo 4.1: Performance SLA

**Questão Pattern:**

```
Especificação menciona "search deve ser rápido", mas sem target concreto.
Qual é o SLA de latência esperado?
```

**Handoff:**

```json
{
  "title": "Não-Funcional: SLA de Latência de Busca",
  "description": "Impacta tech stack (cache, índice, CDN). <100ms requer otimização; <500ms é standard.",
  "options": [
    {
      "label": "A",
      "description": "<100ms (próximo ao real-time, requer RAM cache)",
      "recommended": false
    },
    {
      "label": "B",
      "description": "<500ms (standard, implementável com índice tradição)",
      "recommended": true
    },
    {
      "label": "C",
      "description": "<2000ms (aceitável, podem usar DB relacional)",
      "recommended": false
    }
  ]
}
```

#### Exemplo 4.2: Uptime Requirement

**Questão Pattern:**

```
Qual é o uptime esperado do sistema?
99% (2 horas/mês downtime)?
99.9% (9 minutos/mês)?
99.99% (51 segundos/mês)?
```

**Handoff:**

```json
{
  "title": "Não-Funcional: Disponibilidade (Uptime SLA)",
  "description": "99% = básico (1 instância ok); 99.9% = produção (múltiplas instâncias); 99.99% = crítico (multi-region, redundância).",
  "options": [
    {
      "label": "A",
      "description": "99% uptime (~43 minutos downtime/mês)",
      "recommended": false
    },
    {
      "label": "B",
      "description": "99.9% uptime (~4.3 minutos downtime/mês)",
      "recommended": true
    },
    {
      "label": "C",
      "description": "99.99% uptime (~26 segundos downtime/mês)",
      "recommended": false
    }
  ]
}
```

#### Exemplo 4.3: Security: Password Storage

**Questão Pattern:**

```
Qual é o padrão de hashing de senhas?
PBKDF2? bcrypt? Argon2?
```

**Handoff:**

```json
{
  "title": "Não-Funcional: Armazenamento de Senha",
  "description": "PBKDF2 é standard, bcrypt é recomendado, Argon2 é cutting-edge mas requer mais cuidado.",
  "options": [
    {
      "label": "A",
      "description": "PBKDF2 com 10k+ iterações",
      "recommended": true
    },
    {
      "label": "B",
      "description": "bcrypt com cost factor 12+",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Argon2id (latest, mais robusto)",
      "recommended": false
    }
  ]
}
```

---

## Categoria 5: Integration & External Dependencies

### Descrição

Define sistema em relação a MUNDO EXTERNO (APIs, serviços, formatos). Ambiguidade aqui causa:

- Integration failures
- Breaking changes com 3a-party
- Data loss / incompatibilidade

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | APIs 3a-party definidas, formatos documentados, failure modes descritos |
| ⚠️ Partial | Alguns integradores mencionados, detalhes vagos |
| ❌ Missing | Sem clareza sobre dependências externas |

### Exemplos de Questão

#### Exemplo 5.1: Qual Payment Gateway?

**Questão Pattern:**

```
Especificação menciona "integração com pagamento"
mas não especifica qual gateway (Stripe, PayPal, etc.).
```

**Handoff:**

```json
{
  "title": "Integração: Qual Payment Gateway?",
  "description": "Stripe = flexível + fees 2.9%; PayPal = familiar; MercadoPago = regional. Afeta compliance, fees, velocidade de integração.",
  "options": [
    {
      "label": "A",
      "description": "Stripe (international, flexible, 2.9% + $0.30/transação)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "PayPal (familiar, ~2.2% + fees)",
      "recommended": false
    },
    {
      "label": "C",
      "description": "MercadoPago (regional, mais barato em LATAM)",
      "recommended": false
    }
  ]
}
```

#### Exemplo 5.2: Formato de Dados Import/Export

**Questão Pattern:**

```
Feature permite exportar documentos. Qual é o formato esperado?
CSV? JSON? PDF?
```

**Handoff:**

```json
{
  "title": "Integração: Formato de exportação",
  "description": "CSV = tabular, simples; JSON = flexível, completo; PDF = display-friendly.",
  "options": [
    {
      "label": "A",
      "description": "CSV (tabular, compatível Excel)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "JSON (completo, preserva schema)",
      "recommended": false
    },
    {
      "label": "C",
      "description": "PDF (relatório reader-friendly)",
      "recommended": false
    }
  ]
}
```

---

## Categoria 6: Edge Cases & Failure Handling

### Descrição

Define comportamento em situações ANORMAIS. Ambiguidade aqui causa:

- User frustration
- Data corruption
- Security holes

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | Negative scenarios listados, error messages definidas, recovery strategy explícita |
| ⚠️ Partial | Alguns edge cases mencionados, não todos |
| ❌ Missing | Sem discussion de edge cases |

### Exemplos de Questão

#### Exemplo 6.1: Concurrent Edit (2 usuários mesma doc)

**Questão Pattern:**

```
Se 2 usuários editam o mesmo documento simultaneamente,
qual é o comportamento (conflict resolution)?
```

**Handoff:**

```json
{
  "title": "Edge Case: Edição Simultânea (Conflito)",
  "description": "Last-write-wins = simples mas perder edições; versioning = completo mas complexo; locking = impede conflito.",
  "options": [
    {
      "label": "A",
      "description": "Last-write-wins (último salvo sobrescreve)",
      "recommended": false
    },
    {
      "label": "B",
      "description": "Operational Transformation ou CRDT (merge automático)",
      "recommended": true
    },
    {
      "label": "C",
      "description": "Locking pessimista (primeiro user bloqueia)",
      "recommended": false
    }
  ]
}
```

#### Exemplo 6.2: Timeout em Busca Lenta

**Questão Pattern:**

```
Se busca não termina em X segundos, o que acontece?
Timeout com erro? Cancelamento silencioso?
```

**Handoff:**

```json
{
  "title": "Edge Case: Timeout em Busca Lenta",
  "description": "Impacta UX e confiabilidade. Timeout muito curto frustra; muito longo trava interface.",
  "options": [
    {
      "label": "A",
      "description": "Timeout 30s com retry option",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Cancelamento silencioso (sem notificar user)",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Timeout 5s com hint 'try refining search'",
      "recommended": false
    }
  ]
}
```

---

## Categoria 7: Constraints & Tradeoffs

### Descrição

Define LIMITES E DECISÕES COMPROMETIDAS. Ambiguidade aqui impede priorização.

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | Constraints técnicos listados, tradeoffs articulados com rationale |
| ⚠️ Partial | Alguns constraints mencionados, rationale vago |
| ❌ Missing | Sem clareza sobre constraints ou tecnologia |

### Exemplos de Questão

#### Exemplo 7.1: Linguagem/Stack Técnico

**Questão Pattern:**

```
Especificação não menciona tech stack. Há preference
por linguagem ou stack (Node.js, Python, .NET)?
```

**Handoff:**

```json
{
  "title": "Constraint: Tech Stack",
  "description": "Afeta hiring, time-to-market, ecosystem disponível. Node = rápido; Python = dados/ML friendly; .NET = enterprise.",
  "options": [
    {
      "label": "A",
      "description": "Node.js + Express (rápido, JavaScript full-stack)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Python + Django (dados/analytics friendly)",
      "recommended": false
    },
    {
      "label": "C",
      "description": ".NET C# (enterprise, type-safety)",
      "recommended": false
    }
  ]
}
```

#### Exemplo 7.2: Self-Hosted vs. SaaS

**Questão Pattern:**

```
Sistema deve rodare self-hosted (on-premise) ou
SaaS cloud (AWS/Azure/GCP)?
```

**Handoff:**

```json
{
  "title": "Constraint: Deployment Model",
  "description": "SaaS = operação simples, escala automática; self-hosted = controle, compliance, upgrade lento.",
  "options": [
    {
      "label": "A",
      "description": "SaaS Cloud (AWS/Azure/GCP)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Self-Hosted On-Premise",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Hybrid (cloud primary, self-hosted fallback)",
      "recommended": false
    }
  ]
}
```

---

## Categoria 8: Terminology & Consistency

### Descrição

Define GLOSSÁRIO CANÔNICO. Ambiguidade aqui causa:

- Miscommunication entre times
- Contradicao em documentacao
- API inconsistente

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | Glossário definido, termo canônico consistente |
| ⚠️ Partial | Alguns termos canônicos, outro sinonímia |
| ❌ Missing | Sinônimos usados intercambiavelmente |

### Exemplos de Questão

#### Exemplo 8.1: "Document" vs. "Resource" vs. "File"?

**Questão Pattern:**

```
Especificação usa "documento", "resource", e "file"
como sinônimos. Qual é a terminologia canônica?
```

**Handoff:**

```json
{
  "title": "Terminologia: Nome da entidade principal",
  "description": "Selecione o termo canônico. Todos os outros serão normalizados ou descontinuados.",
  "options": [
    {
      "label": "A",
      "description": "Document (user-facing, genérico)",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Resource (API/system-facing)",
      "recommended": false
    },
    {
      "label": "C",
      "description": "File (storage-focused)",
      "recommended": false
    }
  ]
}
```

---

## Categoria 9: Completion Signals

### Descrição

Define COMO SABER quando feature ESTÁ PRONTA. Ambiguidade aqui causa:

- Scope creep
- Done-done ambiguity
- Teste incompleto

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | AC testáveis listados, DoD definido, métricas de sucesso explícitas |
| ⚠️ Partial | ACs mencionados mas não testáveis |
| ❌ Missing | Sem AC ou DoD claro |

### Exemplo de Questão

#### Exemplo 9.1: Acceptance Criteria para Search

**Questão Pattern:**

```
AC para search feature:
- Deve retornar resultados em <500ms?
- Deve suportar regex ou só keyword-match?
- Deve ser case-insensitive?
```

**Resposta Aberta:**

```
**Questão:** Quais são 3 acceptance criteria mais críticas para search?

**Sugerido:**
1. Retorna resultados em <500ms para corpus <1M docs
2. Case-insensitive keyword match (sem regex)
3. Exclui documentos não-accessible do usuário

**Formato:** 3 bullets, cada uma testável. Pode aceitar "sim"/"suggested"
ou descrever seus próprios critérios.
```

---

## Categoria 10: Misc / Placeholders

### Descrição

Captura TODOs, decisões postergadas, adjetivos vagos. Ambiguidade aqui bloqueia se crítica.

### Status Indicators

| Status | Sinais |
|--------|--------|
| ✅ Clear | TODOs resolvidos, placeholders preenchidos |
| ⚠️ Partial | Alguns TODOs, alguns placeholders ativos |
| ❌ Missing | Muitos TODOs, spec é glorificado outline |

### Exemplo de Questão

#### Exemplo 10.1: TODO não resolvido

**Questão Pattern:**

```
Especificação contém:
"TODO: definir permissões de acesso (read/write/admin)"

É crítico para esta release ou pode defer?
```

**Handoff:**

```json
{
  "title": "Misc: TODO - Permissões de Acesso",
  "description": "Afeta segurança e autorização. Se crítico, deve ser resolvido agora.",
  "options": [
    {
      "label": "A",
      "description": "Crítico - resolver agora como parte da feature",
      "recommended": true
    },
    {
      "label": "B",
      "description": "Nice-to-have - defer para versão futuro",
      "recommended": false
    },
    {
      "label": "C",
      "description": "Reconsiderar escopo - talvez não incluir nesta release",
      "recommended": false
    }
  ]
}
```

---

## Árvore de Priorização (Decision Tree)

```
Start: Arquivo especificação carregado

├─ Functional Scope (1 pergunta)
│  └─ IF vago → P0
│     ELSE → P2
│
├─ Domain & Data (1-2 perguntas)
│  ├─ Sem modelo → P0
│  └─ Modelo vago (IDs, relacionamentos) → P1
│
├─ Interaction & UX (1 pergunta)
│  └─ Sem happy path claro → P1
│
├─ Non-Functional (1-2 perguntas)
│  ├─ Performance/Security vago → P0 (segurança) / P1 (performance)
│  └─ Uptime/Reliability vago → P1
│
├─ Integration (1 pergunta se depende de 3a-party)
│  └─ Dependência indefinida → P1
│
├─ Edge Cases (1 pergunta se crítico)
│  └─ Concurrent/Conflict sem strategy → P1
│
├─ Constraints (1 pergunta se tech não decidido)
│  └─ Tech stack indefinido → P1
│
├─ Terminology (0-1 pergunta se sinonímia confusa)
│  └─ Glossário inconsistent → P2
│
├─ Completion Signals (1 pergunta se vago)
│  └─ AC não testáveis → P2
│
└─ Misc (0-1 pergunta se muitos TODOs)
   └─ Muitos TODOs não resolvidos → P2-P3

Selecionar Top 5 por (Priority × Impact_on_downstream_decisions)
Max questões = 5 por sessão
```

---

## Mapeamento: Pergunta → Seção de Atualização

```
Pergunta sobre...           → Atualizar seção...
─────────────────────────────────────────────────
Functional requirement      → ## Functional Requirements
User role/actor             → ## User Stories / ## Actors
Data entity/field           → ## Data Model
Non-functional metric       → ## Non-Functional / Quality Attributes
Edge case/error scenario    → ## Edge Cases / Error Handling
External service/API        → ## Integration / External Dependencies
Tech stack/constraint       → ## Constraints / Technical Decisions
Terminology                 → Todos (normalize + add glossary term)
Acceptance criterion        → ## Acceptance Criteria
TODO resolution             → Remove TODO, update relevant section
```

---

## Validação: Respostas Esperadas

### Múltipla-Escolha

```text
Input: "A"    → ✅ Válido, accept option A
Input: "a"    → ✅ Válido (case-insensitive)
Input: "yes"  → ✅ Válido, accept recommended option
Input: "B e C" → ❌ Inválido, múltiplas opções
Input: "não sei" → ❌ Inválido, request clarification
```

### Resposta Aberta Curta

```text
Input: "PostgreSQL" → ✅ Válido, 1 palavras
Input: "auto-increment int" → ✅ Válido, 3 palavras
Input: "auto-increment UUID de forma cross-field" → ❌ Inválido, >5 palavras
Input: "yes" → ✅ Válido, accept suggestion
```

---

Versão: 1.0 | Data: 19/03/2026
