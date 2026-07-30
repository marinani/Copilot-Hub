---
name: discovery-20-fluxos-catalago
description: Gera ou atualiza o catálogo mestre de fluxos candidatos a partir do banco e de artefatos discovery, depois para obrigatoriamente no chat para o usuário informar fluxos importantes não mapeados automaticamente. Saída principal: DISC-03-CATALOGO-DE-FLUXOS.md.
---

# Skill — discovery-20-fluxos-catalago

**Propósito:** gerar o catálogo inicial de fluxos candidatos e abrir um checkpoint obrigatório de validação humana no chat antes de consolidar a fila final.

---

## 1. Princípio operacional

Esta skill funciona em **duas fases internas**:

1. **Mapeamento automático** — usa banco e artefatos discovery para propor os fluxos principais.
2. **Checkpoint no chat** — pergunta ao usuário quais fluxos importantes ficaram faltando e só então consolida o catálogo final.

> **Regra obrigatória:** nunca encerrar a catalogação sem perguntar no chat por fluxos relevantes não mapeados automaticamente.

---

## 2. Fontes obrigatórias

Ler antes de iniciar:

1. `discovery-project.yml`
2. `discovery/DADOS-05-MAPA-DADOS.md` se existir
3. `discovery/DADOS-06-STATUS-E-TRANSICOES.md` se existir
4. `discovery/DADOS-10-ROTINAS-FUNCTIONS-PROCEDURES.md` se existir
5. `discovery/TELA-CATALOGO.md` se existir
6. Banco via MCP configurado no projeto

---

## 3. Fase A — Mapeamento automático banco-driven

Identificar fluxos principais a partir de evidências de banco:

- tabelas de maior volume
- colunas de status, situação, estado, tipo e canal
- procedures/functions com regras de negócio recorrentes
- tabelas de histórico, log, movimento e evento
- vínculos com telas já catalogadas

Para cada fluxo candidato, registrar no catálogo:

| Campo | Conteúdo |
|---|---|
| `CF-XXX` | identificador sequencial do fluxo candidato |
| Nome operacional | nome legível do fluxo |
| Origem | `AUTO-BANCO` |
| Confiança | `alta`, `media` ou `baixa` |
| Evidências | tabelas, status, SPs, telas, endpoints |
| Prioridade | `alta`, `media`, `baixa` |
| Status | `pendente`, `em andamento`, `documentado` |

---

## 4. Fase B — Checkpoint obrigatório no chat

Após gerar a lista automática, **parar e perguntar no chat**:

1. "Quais fluxos importantes do negócio não apareceram neste catálogo automático?"
2. "Existe algum fluxo prioritário que deve entrar manualmente agora?"
3. "Quais CFs devem ser tratados primeiro?"

Adicionar ao catálogo as respostas do usuário com:

- `Origem = MANUAL-CHAT`
- `Confiança = validada pelo usuário`
- campo `Validação humana` preenchido com data e observação resumida

> **Obrigatório:** os fluxos informados pelo usuário não podem ser descartados por falta de evidência técnica inicial. Devem entrar no catálogo com rastreabilidade de origem manual.

---

## 5. Saída gerada

Gerar ou atualizar `discovery/DISC-03-CATALOGO-DE-FLUXOS.md` com:

1. resumo da geração automática
2. seção de fluxos adicionados manualmente no chat
3. fila priorizada final
4. status por fluxo candidato

Formato mínimo por fluxo:

```markdown
### CF-001 — Nome do Fluxo

- **Origem:** AUTO-BANCO | MANUAL-CHAT
- **Confiança:** alta | media | baixa | validada pelo usuário
- **Validação humana:** DD/MM/AAAA — observação
- **Tabelas principais:** ...
- **Status relevantes:** ...
- **SPs / Functions:** ...
- **Telas relacionadas:** ...
- **Prioridade:** alta | media | baixa
- **Status do fluxo:** pendente | em andamento | documentado
- **Lacunas de evidência:** ...
```

---

## 6. Regras de qualidade

- Não gerar zero fluxos: se o banco falhar, criar um catálogo mínimo e abrir pendências.
- Não inventar regra de negócio: quando faltarem evidências, registrar lacuna.
- Sempre diferenciar claramente fluxo automático de fluxo informado no chat.
- Sempre perguntar ao usuário por fluxos faltantes antes de concluir.

---

## 7. Checklist

- [ ] Banco consultado para mapear fluxos candidatos
- [ ] DADOS-05, DADOS-06, DADOS-10 usados como enriquecimento
- [ ] TELA-CATALOGO.md usado para cruzar evidências de interface
- [ ] Catálogo preliminar gerado
- [ ] Perguntas obrigatórias feitas no chat
- [ ] Fluxos manuais incorporados ao catálogo
- [ ] DISC-03 consolidado e salvo
