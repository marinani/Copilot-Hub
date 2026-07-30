# Critérios de Aceitação Completos — req-XXXX nome_do_requisito

## Metadados

| Campo               | Valor                                                               |
|---------------------|---------------------------------------------------------------------|
| Requisito de Origem | req-XXXX                                                            |
| Autor               | [Nome completo — proibido "IA", "Copilot", "Automático" ou similar] |
| Versão              | 1.0                                                                 |
| Data                | DD/MM/AAAA                                                          |
| Status              | Rascunho \| Em revisão \| Aprovado                                  |

> Este documento contém **todos os cenários de aceitação possíveis** para o requisito `req-XXXX`.
> Os documentos `req-XXXX` e `tec-req-XXXX` devem referenciar no máximo 5 cenários selecionados deste arquivo.
> A numeração `CA-NNN` é **local** — reinicia em `CA-001` a cada novo `cri-req-XXXX`.

---

## Processo de Geração (obrigatório antes de preencher)

1. Aplicar o protocolo de entendimento do `brainstorm.md` para mapear todos os atores, fluxos e casos de borda do requisito.
2. Para cada combinação (ator × ação × estado × resultado), gerar um cenário Gherkin distinto.
3. Cobrir obrigatoriamente: happy path, fluxos alternativos, falhas de validação, falhas de permissão, estado anterior incorreto e concorrência (quando aplicável).
4. Eliminar apenas duplicatas exatas; nunca eliminar variações de contexto ou estado.

---

## Cenários de Aceitação

### CA-001 — Fluxo principal com sucesso

```gherkin
Dado que [pré-condição do estado do sistema]
E [condição adicional]
Quando [ação executada pelo ator]
Então [resultado esperado principal]
E [resultado complementar esperado]
```

### CA-002 — Fluxo alternativo: [descrever condição]

```gherkin
Dado que [pré-condição alternativa]
Quando [ação executada]
Então [resultado alternativo esperado]
```

### CA-003 — Falha de validação: [descrever campo/regra]

```gherkin
Dado que [contexto com dado inválido]
Quando [ação executada]
Então [mensagem de erro esperada]
E [estado do sistema após a falha]
```

### CA-004 — Falha de permissão: [descrever perfil sem acesso]

```gherkin
Dado que o usuário possui perfil "[perfil sem permissão]"
Quando [ação executada]
Então [comportamento esperado — bloqueio, redirecionamento, mensagem]
```

### CA-005 — Caso de borda: [descrever condição limite]

```gherkin
Dado que [condição de borda — valor mínimo, máximo, vazio, null, etc.]
Quando [ação executada]
Então [resultado esperado na condição limite]
```

> **Adicionar quantos cenários forem necessários para cobertura completa.**
> Exemplos de categorias adicionais: concorrência, timeout, retry, dados duplicados, integração externa indisponível, rollback, estado de carregamento.

---

## Resumo de Cobertura

| Categoria                     | Cenários cobertos | Observações |
|-------------------------------|-------------------|-------------|
| Happy path (fluxo principal)  | CA-001            |             |
| Fluxos alternativos           |                   |             |
| Falhas de validação           | CA-003            |             |
| Falhas de permissão           | CA-004            |             |
| Casos de borda                | CA-005            |             |
| Concorrência / estado inválido|                   |             |
| Integrações externas          |                   |             |

---

## Cenários Selecionados para req-XXXX e tec-req-XXXX

> Listar aqui os **5 cenários mais representativos** que devem constar nos documentos `req-XXXX` e `tec-req-XXXX`. Priorizar: fluxo principal + casos de maior risco.

| Prioridade | Cenário | Justificativa da seleção |
|------------|---------|--------------------------|
| 1          | CA-001  | Fluxo principal          |
| 2          |         |                          |
| 3          |         |                          |
| 4          |         |                          |
| 5          |         |                          |

---

## Histórico de Alterações

| Versão | Data       | Autor | Descrição            |
|--------|------------|-------|----------------------|
| 1.0    | DD/MM/AAAA |       | Criação do documento |
