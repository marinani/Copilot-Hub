---
description: Guia de implementação de handoff interativo para a skill clarification
applyTo: clarification
---

# Clarification — Handoff Integration Guide

## O que é Handoff?

Handoff é um mecanismo do VSCode Chat que permite interação estruturada entre o usuário e o agente, com canalização de respostas de múltipla-escolha ou entrada de formulário.

A skill `clarification` usa handoff para:

1. **Apresentar opções** de forma visual clara
2. **Canalizar respostas** para validação automática
3. **Registrar decisões** no contexto de forma estruturada
4. **Iterat continuamente** sem perder histórico

---

## Padrão de Payload Handoff

### Estrutura JSON

```json
{
  "role": "user",
  "content": "[Message content here]",
  "handoff": {
    "title": "Decisão de Arquitetura: [Ponto de Decisão]",
    "description": "[Contexto + Recomendação]",
    "options": [
      {
        "label": "A",
        "description": "[Descrição da opção A]",
        "recommended": true
      },
      {
        "label": "B",
        "description": "[Descrição da opção B]",
        "recommended": false
      }
    ]
  }
}
```

### Campos Obrigatórios

| Campo                   | Tipo    | Descrição                            |
| ----------------------- | ------- | ------------------------------------ |
| `title`                 | string  | Título curto (≤100 chars)            |
| `description`           | string  | Contexto + recomendação (≤500 chars) |
| `options`               | array   | Mínimo 2, máximo 5 opções            |
| `options[].label`       | string  | A, B, C, etc ou valor direto         |
| `options[].description` | string  | Descrição clara (≤200 chars)         |
| `options[].recommended` | boolean | Exatamente uma opção `true`          |

---

## Fluxo Passo-a-Passo

### 1. Análise Inicial (Sem Handoff)

**Entrada:**

```
/clarification documentacao/features/search.md
```

**Saída:**

```
🔍 **Análise de Especificação: search.md**

Varredura estruturada concluída.

| Categoria          | Status    | Issue                                       |
| ------------------ | --------- | ------------------------------------------- |
| Functional Scope   | ⚠️ Partial | "Search scope vago: full-text vs. indexed?" |
| Domain & Data      | ⚠️ Partial | "Modelo de índice não definido"             |
| Interaction & UX   | ✅ Clear   | -                                           |
| Non-Functional     | ❌ Missing | "Performance targets não especificados"     |
| Integration        | ✅ Clear   | -                                           |
| Edge Cases         | ⚠️ Partial | "Timeout behavior undefined"                |
| Constraints        | ✅ Clear   | -                                           |
| Terminology        | ✅ Clear   | -                                           |
| Completion Signals | ⚠️ Partial | "AC para busca vazia indefinido"            |
| Misc               | ❌ Missing | "TODO: definir estratégia de cache"         |

**5 questões prioritizadas em fila.**

Vou começar com a mais crítica...
```

### 2. Primeira Questão + Handoff

**Saída com Handoff:**

```
### **P0 - Search Type & Scope**

**Questão:** Que tipo de busca é esperado para esta feature?

**Contexto:** A especificação menciona "busca rápida" mas não clarifica
se é busca full-text em texto livre, busca indexed por campos estruturados,
ou busca facetada. Isso impacta diretamente:
- Arquitetura de índices (Elasticsearch vs. SQL LIKE vs. PostgreSQL FTS)
- Estrutura de dados (denormalização, tokens, filtering)
- Performance targets (SLA de latência)

**Recomendado:** Opção A - Full-text search em corpus textual é mais
simples de começar e cobre 80% dos casos de uso comuns. Se depois
precisar facetas, pode adicionar sem redesenhar core.
```

**Handoff JSON:**

```json
{
  "role": "user",
  "content": "### **P0 - Search Type & Scope**\n\n**Questão:** Que tipo de busca é esperado?\n\n**Recomendado:** Opção A - Full-text em corpus de texto.",
  "handoff": {
    "title": "P0 - Tipo de Busca: Full-text vs. Indexed vs. Faceted",
    "description": "Escolha impacta arquitetura de índices (Elasticsearch/SQL FTS), estrutura de dados e SLA de latência. Recomendado: Full-text (A) — opção mais simples, 80% dos casos cobertos.",
    "options": [
      {
        "label": "A",
        "description": "Full-text search em corpus de texto livre (ex: título, descrição, conteúdo)",
        "recommended": true
      },
      {
        "label": "B",
        "description": "Indexed search por campos estruturados (ex: filtro por categoria, autor, data)",
        "recommended": false
      },
      {
        "label": "C",
        "description": "Faceted search com múltiplas dimensões (ex: categoria + data + autor combinados)",
        "recommended": false
      },
      {
        "label": "D",
        "description": "Outro (descreva em ≤5 palavras)",
        "recommended": false
      }
    ]
  }
}
```

**VSCode Chat renderiza:**

```
┌─────────────────────────────────────────────────────┐
│ P0 - Tipo de Busca: Full-text vs. Indexed vs. ...   │
│                                                      │
│ Escolha impacta arquitetura de índices... (...)    │
│                                                      │
│ ☆ Full-text search em corpus de texto              │
│   (Recomendado)                                     │
│                                                      │
│ ○ Indexed search por campos estruturados            │
│                                                      │
│ ○ Faceted search com múltiplas dimensões            │
│                                                      │
│ ○ Outro (descreva em ≤5 palavras)                   │
│                                                      │
│ [Selecionar] [Cancelar]                             │
└─────────────────────────────────────────────────────┘
```

### 3. Resposta do Usuário + Validação

**Usuário clica:** `☆ Full-text search em corpus de texto`

**Bot processa:**

```
✅ Resposta validada: Opção A

Handoff status: Sucesso
Valor extraído: full-text search
Registrando em memória...
```

### 4. Integração na Especificação

**Operação Atômica:**

```python
# Pseudocódigo
spec_file = load("documentacao/features/search.md")

# Garantir seção Updates
if no "## Updates" section:
    insert_after_overview("""
## Updates

| Data da Atualização | Autor                | Descrição                     |
| ------------------- | -------------------- | ----------------------------- |
| 19/03/2026          | AI Clarification Bot | Initial clarification session |

### Session 2026-03-19
""")

# Registrar pergunta-resposta
append_to_session("""
- Q: Search type (full-text vs. indexed vs. faceted)? → A: Full-text search in free text corpus
""")

# Atualizar seções relevantes
section = spec_file.get_section("## Functional Requirements") or create_section()
section.add_bullet("Search scope: Full-text search over textual corpus (title, description, content)")

# Atualizar Data Model se aplicável
data_model = spec_file.get_section("## Data Model")
data_model.add_bullet("Search Index: Full-text index on searchable fields (TBD tech: PostgreSQL FTS / Elasticsearch)")

# Salvar atomicamente
spec_file.save()
```

**Arquivo após integração:**

```markdown
## Functional Requirements

- User can search across all documents by keywords
- **Search scope: Full-text search over textual corpus (title, description, content)**
- Search results limited to documents user has access to

## Data Model

- Documents:
  - id: UUID
  - title: String
  - content: Text
  - **Search Index: Full-text index on searchable fields (TBD tech: PostgreSQL FTS / Elasticsearch)**
  - metadata: JSON

## Updates

| Data da Atualização | Autor                | Descrição                     |
| ------------------- | -------------------- | ----------------------------- |
| 19/03/2026          | AI Clarification Bot | Initial clarification session |

### Session 2026-03-19

- Q: Search type (full-text vs. indexed vs. faceted)? → A: Full-text search in free text corpus
```

### 5. Segunda Questão

**Saída (similar ao passo 2):**

```
✅ Primeira clarificação integrada. Próxima questão...

---

### **P1 - Search Performance SLA**

**Questão:** Qual é o SLA de latência esperado para resultados de busca?

**Contexto:** "Search rápida" não é testável. Precisamos de um target:
- <100ms: Requer índice em-memória (Redis, Elasticsearch), custo alto
- <500ms: Índice tradicional em disco, good para maioria dos casos
- <2s: Busca em banco relacional, mais simples, trade-off aceitável

**Recomendado:** Opção B - <500ms cobre "rápido" percebido pelo usuário
e é implementável com PostgreSQL FTS ou Elasticsearch standard.
```

### 6. Loop Contínuo

Processo repete: **Pergunta → Handoff → Resposta → Validação → Integração → Próxima Pergunta**

Até:

- 5 perguntas perguntadas, OU
- Usuário sinalize "done" / "pronto" / "fim", OU
- Fila de questões se esvaziar

### 7. Relatório Final

```
## ✅ Sessão Concluída

**Resumo:**
- Questões perguntadas: 3 de 5
- Arquivo atualizado: documentacao/features/search.md
- Ambiguidades resolvidas: 3
- Deferred para planning: 2

**Seções Modificadas:**
- Functional Requirements: 1 bullet adicionado
- Data Model: 1 bullet adicionado
- Non-Functional: (será na próxima pergunta)

**Cobertura Atualizada:**

| Categoria        | Status        | Notas                                    |
| ---------------- | ------------- | ---------------------------------------- |
| Functional Scope | ✅ Resolved    | Escopo de busca definido                 |
| Domain & Data    | ⚠️ Partial     | Índice tecnologia TBD, pode ser planning |
| Interaction & UX | ✅ Clear       | -                                        |
| Non-Functional   | ⚡ In Progress | (P1 respondida justo agora)              |
| Edge Cases       | ⏳ Deferred    | Timeout/retry exceeds quota              |

**Próximo passo:**
```

/clarification documentacao/features/search.md

```
(para continuar com mais 5 questões se necessário)

Ou:
```

/planning-and-task-breakdown documentacao/features/search.md

```
(para prosseguir para fase de planning/design)
```

---

## Formato Exato de Resposta com Handoff

### Respostas Esperadas

#### Múltipla-Escolha

- ✅ "A"
- ✅ "B"
- ✅ "yes" (aceita recomendação)
- ✅ "recommended"
- ❌ Respostas incompletas ou ambíguas resultam em pedido de clarificação

#### Resposta Aberta Curta

- ✅ "PostgreSQL FTS"
- ✅ "500ms"
- ✅ "elastic search"
- ✅ "sim" (aceita sugestão)
- ✅ "suggested"
- ❌ Respostas > 5 palavras resultam em erro de validação

#### Sinais de Parada

- ✅ "pronto"
- ✅ "done"
- ✅ "fim"
- ✅ "sem mais"
- ✅ "próximo passo"

---

## Validação de Resposta — Lógica

```
IF user_input.matches(/^[a-eA-E]$/):
    return mcq_answer(user_input)
ELIF user_input.lower() in ["yes", "sim", "recommended", "suggested"]:
    return accept_recommendation()
ELIF user_input.matches(/^.{1,50}$/):  # <=5 palavras = ~50 chars
    return accept_short_answer(user_input)
ELSE:
    return request_disambiguation()
    return False  # não consome uma pergunta
```

---

## Exemplo de Falha & Recovery

### Cenário: Resposta Ambígua

**Bot:**

```
### **P0 - Search Scope**

**Recomendado:** Opção A - Full-text search

[Handoff com 4 opções]
```

**Usuário:** `maybe A or B depending on requirements`

**Bot:**

```
❌ Resposta não clara ou muito longa.

Respondeu: "maybe A or B depending on requirements"

A busca pode ser:
- **A - Full-text** (recomendado): texto livre
- **B - Indexed**: por campos
- Ou você prefere uma **abordagem diferente?**

Por favor, confirme:
- Responda com a letra (A ou B)
- Ou "sim" para aceitar a recomendação
- Ou descreva sua opção em ≤5 palavras
```

**Usuário:** `A`

**Bot:**

```
✅ Resposta validada e registrada: Opção A (Full-text search)
```

---

## Integração com Ferramentas Coexistentes

### Handoff + Spec-Driven Workflow

```
1. /spec-driven-workflow documentacao/features/search.md
   → Cria especificação inicial estruturada

2. /clarification documentacao/features/search.md
   → Refina ambiguidades

3. /planning-and-task-breakdown documentacao/features/search.md
   → Planning baseado em spec clarificada
```

### Handoff + Database-MCP

Se clarificação identificar decisão sobre persistência:

```
- Q: Persistência em PostgreSQL ou Elasticsearch?
- A: PostgreSQL + FTS

Depois:
/mcp database-mcp
→ Explora schema PostgreSQL, cria documentação
```

---

## Regras para Manutenção da Skill

### Quando Atualizar

- Feature flag de handoff no VSCode muda
- Nova categoria de ambiguidade descoberta
- Novo padrão de pergunta provado efetivo

### Versionamento

```yaml
---
name: clarification
version: "1.0"  # SEM .md extension
last_updated: "19/03/2026"
compatibility: "vscode-chat >= 1.x"
---
```

---

## Troubleshooting para Implementadores

### Problema: Handoff não renderiza

**Causa:** Payload JSON inválido

**Checklist:**

- ✅ `options` é array com 2-5 elementos?
- ✅ Exatamente um `recommended: true`?
- ✅ Strings sem quebras de linha não escapadas?
- ✅ VSCode Chat versão suportada?

### Problema: Resposta não capturada

**Causa:** Usuario respondeu via texto, não via botão

**Solução:** Bot deve parsear resposta textual como fallback:

```
IF user_selected_button:
    use handoff_response
ELSE IF user_typed_text:
    validate_and_parse_text(user_input)  # fallback parser
```

### Problema: Arquivo não salva

**Causa:** Permissão de escrita ou path inválido

**Checklist:**

- ✅ Path é relativo ao workspace root?
- ✅ Arquivo existe (não criar spec nova)?
- ✅ Permissão de escrita no diretório?

---

## Template de Novos Tipos de Pergunta

Se precisar adicionar novo padrão:

```markdown
### Novo Padrão: [Nome]

**Handoff JSON Template:**
```json
{
  "handoff": {
    "title": "[Titulo]",
    "description": "[Recomendacao + Contexto]",
    "options": [
      {
        "label": "[Valor 1]",
        "description": "[Descricao 1]",
        "recommended": true
      }
    ]
  }
}
```

**Validação:**

- Que descrever como validar resposta deste tipo
- Exemplos de respostas válidas/inválidas
- Como integrar resposta na spec

```

---

## Referências Internas

- `.github/prompts/clarify.prompt.md` — Prompt original
- `.github/skills/clarification/SKILL.md` — Skill principal
- `.github/skills/brainstorming/SKILL.md` — Padrão Socratic que inspira clarification
- `.github/skills/database-mcp/SKILL.md` — Exemplo de handoff em MCP

---

Versão: 1.0 | Data: 19/03/2026
