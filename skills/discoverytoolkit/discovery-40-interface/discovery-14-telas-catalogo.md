---
name: discovery-14-telas-catalogo
description: Varre o legado para catalogar todas as telas (JSP/XHTML/Java) e gera/atualiza TELA-CATALOGO.md com numeração sequencial TELA-{NNN}-{PascalCase}. Deve ser executado ANTES da skill discovery-14-Telas. Relê o catálogo existente para não duplicar entradas já documentadas.
---

# Skill — discovery-14-telas-catalogo

**Propósito:** Varrer o legado e produzir `TELA-CATALOGO.md` — o índice mestre de telas, com numeração sequencial e status de documentação.

Esta skill é **pré-requisito obrigatório** para `discovery-14-Telas`. Chame-a uma única vez (ou sempre que quiser atualizar o catálogo) antes de documentar telas individualmente.

---

## 1. Pré-leitura obrigatória

Antes de iniciar, ler na ordem abaixo:

1. **`discovery-project.yml`** (raiz do workspace) → obter:
   - `paths.legacy` — pasta-raiz do código legado
   - `paths.discovery` — pasta onde os artefatos serão gerados
2. Se existir, ler **`{paths.discovery}/TELA-CATALOGO.md`** → importar entradas já catalogadas (ID, nome, arquivo legado, tipo, status) para não duplicar nem reatribuir números.

---

## 2. Identificação das views no legado

> ⚠️ **REGRA CRÍTICA DE PERFORMANCE:** trabalhar **apenas com nomes de arquivo** — **NÃO abrir nem ler o conteúdo** de nenhum arquivo durante a catalogação. Todo o processamento deve ser feito sobre caminhos e nomes. A leitura de conteúdo acontece somente na fase de documentação (`discovery-14-Telas`), uma tela por vez.

Usar `file_search` ou `list_dir` para obter a lista de arquivos. **Não usar `read_file` nesta fase.**

Filtros de inclusão (pelo nome/caminho, sem ler conteúdo):

| Extensão | Inclusão |
|---|---|
| `*.xhtml`, `*.jsp`, `*.jsf` | Qualquer arquivo que não seja excluído pelos critérios abaixo |
| `*Action.java`, `*Bean.java`, `*MB.java`, `*Controller.java` | **Apenas** quando não existir XHTML/JSP/JSF de mesmo nome base — evitar duplicação |

**Excluir pelo nome** (sem ler conteúdo):
- Nome começa com `_` → fragmento sem URL própria
- Nome contém `template`, `layout`, `menu`, `header`, `footer`, `sidebar` → componente reutilizável
- Caminho contém `/test/` ou `/tests/`

---

## 3. Geração do slug PascalCase

Para cada view identificada:

1. Pegar o nome base do arquivo (sem extensão e sem caminho).
2. Normalizar para PascalCase:
   - Separadores reconhecidos: `-`, `_`, `.`, espaço
   - Capitalizar a primeira letra de cada palavra
   - Remover caracteres especiais (manter apenas letras e números)
   - Remover sufixos reconhecidos quando vier de Java: `Action`, `Bean`, `MB`, `Controller`
   - Exemplos:
     - `cadastro-contribuinte.xhtml` → `CadastroContribuinte`
     - `consultaHistoricoPA.xhtml` → `ConsultaHistoricoPA`
     - `BeneficioAction.java` → `Beneficio`
3. Se o slug gerado já existir no catálogo corrente (para arquivo diferente), adicionar sufixo `_2`, `_3`, etc.

---

## 4. Classificação do tipo — baseada SOMENTE no nome do arquivo

> **Não ler conteúdo para classificar.** A heurística abaixo é baseada exclusivamente no nome do arquivo. O agente documentador corrige o tipo ao investigar o arquivo real na fase `discovery-14-Telas`.

| Tipo | Critério (pelo nome do arquivo, case-insensitive) |
|---|---|
| **AUXILIAR** | Nome contém qualquer um de: `lista`, `consulta`, `pesquisa`, `busca`, `relatorio`, `grid`, `popup`, `modal`, `selecao` |
| **PRINCIPAL** | Todos os demais |

> Use `⚠️ revisar` na coluna Tipo quando o nome for ambíguo.

---

## 5. Numeração sequencial

- Reutilizar os números já atribuídos no catálogo existente (lido no passo 1).
- Para novas entradas: atribuir o próximo número livre na sequência com 3 dígitos (`001`, `002`, …, `099`, `100`, …).
- **Nunca reutilizar um número**, mesmo que a entrada original tenha sido removida.
- Se o arquivo legado for renomeado: atualizar o campo `Arquivo Legado`, mantendo o número.

---

## 6. Verificação de status

Para cada tela catalogada, verificar se o artefato já foi gerado:

- Procurar por `TELA-{NNN}-*.md` em `{paths.discovery}/`.
- Se encontrado → status **🟢 documentada**
- Se não encontrado → status **🔴 pendente**

---

## 7. Geração do TELA-CATALOGO.md

Gerar ou sobrescrever `{paths.discovery}/TELA-CATALOGO.md` com o formato abaixo.

```markdown
# TELA-CATALOGO — Catálogo de Telas

> Gerado em: {data DD/MM/AAAA}
> Total: {N} telas · {N} documentadas 🟢 · {N} pendentes 🔴 · {N} em andamento 🟡

## Legenda de status

- 🔴 pendente — ainda não documentada
- 🟡 em andamento — documentação iniciada (skill discovery-14-Telas em execução)
- 🟢 documentada — arquivo TELA-{NNN}-*.md gerado

---

## Índice

| # | ID | Nome | Arquivo Legado | Tipo | Status |
|---|---|---|---|---|---|
| 1 | TELA-001 | CadastroContribuinte | `cadastroContribuinte.xhtml` | PRINCIPAL | 🔴 pendente |
| 2 | TELA-002 | ConsultaBeneficio | `consultaBeneficio.xhtml` | AUXILIAR | 🟢 documentada |

---

## Detalhes por tela

### TELA-001 — CadastroContribuinte

- **Arquivo legado:** `{caminho relativo a paths.legacy}/cadastroContribuinte.xhtml`
- **Java associado:** `{caminho}/CadastroContribuinte.java` _(se encontrado)_
- **Tipo:** PRINCIPAL
- **Status:** 🔴 pendente
- **Artefato gerado:** —

### TELA-002 — ConsultaBeneficio

- **Arquivo legado:** `{caminho}/consultaBeneficio.xhtml`
- **Java associado:** `{caminho}/ConsultaBeneficio.java` _(se encontrado)_
- **Tipo:** AUXILIAR
- **Status:** 🟢 documentada
- **Artefato gerado:** `TELA-002-ConsultaBeneficio.md`
```

---

## 8. Checklist de entrega

- [ ] `discovery-project.yml` lido; `paths.legacy` e `paths.discovery` identificados.
- [ ] Catálogo existente lido (se houver) — nenhum número duplicado.
- [ ] Varredura de `*.xhtml`, `*.jsp`, `*.jsf` e Java MBs/Actions executada.
- [ ] Arquivos de template e fragmento excluídos.
- [ ] Slug PascalCase gerado para cada tela, sem duplicação.
- [ ] Tipo classificado (PRINCIPAL / AUXILIAR / SEM-FLUXO).
- [ ] Numeração sequencial atribuída (3 dígitos, sem lacunas novas).
- [ ] Status verificado: 🟢 para telas com artefato gerado, 🔴 para pendentes.
- [ ] `TELA-CATALOGO.md` gerado em `{paths.discovery}/`.
- [ ] Totais (documentadas / pendentes) registrados no cabeçalho.

---

## 9. Como iniciar a documentação individual

Após gerar o catálogo, documente cada tela chamando a skill `discovery-14-Telas`:

```
@discovery-40-interface documentar TELA-001
@discovery-40-interface documentar CadastroContribuinte
```

A skill `discovery-14-Telas` lê este catálogo para identificar o arquivo legado e o número sequencial correto. Repita o comando para cada tela, uma por vez.
