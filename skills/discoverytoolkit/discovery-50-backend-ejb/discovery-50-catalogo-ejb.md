---
name: discovery-50-catalogo-ejb
description: Varre o legado para catalogar todos os EJBs (@Stateless/@Stateful) e gera/atualiza EJB-CATALOGO.md com numeração sequencial EJB-{NNN}-{PascalCase}. Deve ser executado ANTES da skill discovery-51-ejb. Relê o catálogo existente para não duplicar entradas já documentadas.
---

# Skill — discovery-50-catalogo-ejb

**Propósito:** Varrer o legado e produzir `EJB-CATALOGO.md` — o índice mestre de Session Beans, com numeração sequencial e status de documentação.

Esta skill é **pré-requisito obrigatório** para `discovery-51-ejb`. Chame-a uma única vez (ou sempre que quiser atualizar o catálogo) antes de documentar EJBs individualmente.

---

## 1. Pré-leitura obrigatória

Antes de iniciar, ler na ordem abaixo:

1. **`discovery-project.yml`** (raiz do workspace) → obter:
   - `paths.legado` — pasta-raiz do código legado
   - `paths.discovery` — pasta onde os artefatos serão gerados
2. Se existir, ler **`{paths.discovery}/EJB-CATALOGO.md`** → importar entradas já catalogadas (ID, nome, arquivo, tipo, status) para não duplicar nem reatribuir números.

---

## 2. Identificação dos EJBs no legado

Varrer a pasta `{paths.legado}` **recursivamente**. Considerar como EJB documentável:

| Critério | Detalhe |
|---|---|
| Anotação `@Stateless` | Session Bean sem estado — padrão da camada de serviço |
| Anotação `@Stateful` | Session Bean com estado — fluxos que mantêm conversação |

**Excluir obrigatoriamente:**
- Arquivos em subpastas de teste (`/test/`, `/tests/`)
- Classes com `@Entity`, `@MappedSuperclass`, `@Embeddable` — entidades JPA, não EJBs de serviço
- Actions/Beans/MBs de UI já cobertos pelo `discovery-40-interface`: classes com `@ManagedBean`, `@Named`, `@RequestScoped`, `@SessionScoped`, ou sufixos `Action`, `Bean`, `MB` **que possuam navegação JSF** (retornam `String` para navigation-rule ou têm `FacesContext` injetado)
- Classes de integração do módulo `integracao-ejb` — escopo separado

**Para cada EJB incluído, coletar:**
- Caminho relativo a `paths.legado`
- Interface `@Local` ou `@Remote` associada (mesmo nome base com sufixo `Local`/`Remote`, se existir)
- Tipo: `Stateless` ou `Stateful`
- Contagem de métodos públicos (não privados, não static helpers)
- Módulo de origem (ex.: `Previdenciario-ejb`)

---

## 3. Geração do slug PascalCase

Para cada EJB identificado:

1. Pegar o nome base da classe (sem extensão e sem caminho).
2. Normalizar para PascalCase:
   - Separadores reconhecidos: `-`, `_`, `.`, espaço
   - Capitalizar a primeira letra de cada palavra
   - Remover caracteres especiais (manter apenas letras e números)
   - Remover sufixos reconhecidos: `Bean`, `Impl`, `EJBImpl`, `EJB`, `Service`, `ServiceImpl`
   - Exemplos:
     - `CalculoContribuicaoBean.java` → `CalculoContribuicao`
     - `BeneficioServiceImpl.java` → `BeneficioService`
     - `PagamentoEJBImpl.java` → `Pagamento`
3. Se o slug gerado já existir no catálogo corrente (para arquivo diferente), adicionar sufixo `_2`, `_3`, etc.

---

## 4. Classificação do tipo

| Tipo | Critério |
|---|---|
| **STATELESS** | Classe anotada com `@Stateless` — sem estado entre chamadas |
| **STATEFUL** | Classe anotada com `@Stateful` — mantém estado de conversação entre chamadas |

---

## 5. Numeração sequencial

- Reutilizar os números já atribuídos no catálogo existente (lido no passo 1).
- Para novas entradas: atribuir o próximo número livre na sequência com 3 dígitos (`001`, `002`, …, `099`, `100`, …).
- **Nunca reutilizar um número**, mesmo que a entrada original tenha sido removida.
- Se o arquivo legado for renomeado: atualizar o campo `Arquivo`, mantendo o número.

---

## 6. Verificação de status

Para cada EJB catalogado, verificar se o artefato de documentação já foi gerado:

- Procurar por `EJB-{NNN}-*.md` em `{paths.discovery}/`.
- Se encontrado → status **🟢 documentado**
- Se não encontrado → status **🔴 pendente**

---

## 7. Geração do EJB-CATALOGO.md

Gerar ou sobrescrever `{paths.discovery}/EJB-CATALOGO.md` com o formato abaixo.

```markdown
# EJB-CATALOGO — Catálogo de Session Beans

> Gerado em: {data DD/MM/AAAA}
> Total: {N} EJBs · {N} documentados 🟢 · {N} pendentes 🔴 · {N} em andamento 🟡

## Legenda de status

- 🔴 pendente — ainda não documentado
- 🟡 em andamento — documentação iniciada (skill discovery-51-ejb em execução)
- 🟢 documentado — arquivo EJB-{NNN}-*.md gerado

---

## Índice

| # | ID | Nome | Arquivo | Interface | Tipo | Métodos públicos | Status | Artefato gerado |
|---|---|---|---|---|---|---|---|---|
| 1 | EJB-001 | CalculoContribuicao | `...CalculoContribuicaoBean.java` | `...CalculoContribuicaoLocal.java` | Stateless | 8 | 🔴 pendente | — |
| 2 | EJB-002 | Pagamento | `...PagamentoEJBImpl.java` | — | Stateless | 5 | 🟢 documentado | `EJB-002-Pagamento.md` |

---

## Detalhes por EJB

### EJB-001 — CalculoContribuicao

- **Arquivo:** `{caminho relativo}/CalculoContribuicaoBean.java`
- **Interface:** `{caminho}/CalculoContribuicaoLocal.java` _(se encontrado)_
- **Tipo:** Stateless
- **Módulo:** Previdenciario-ejb
- **Métodos públicos:** 8
- **Status:** 🔴 pendente
- **Artefato gerado:** —
```

---

## 8. Checklist de entrega

- [ ] `discovery-project.yml` lido; `paths.legado` e `paths.discovery` identificados.
- [ ] Catálogo existente lido (se houver) — nenhum número duplicado.
- [ ] Varredura de `@Stateless` e `@Stateful` executada em todos os módulos legado.
- [ ] Classes de UI (Actions/MBs/Beans com navegação JSF) excluídas.
- [ ] Classes do módulo `integracao-ejb` excluídas do escopo desta skill.
- [ ] Entidades JPA (`@Entity`, `@MappedSuperclass`) excluídas.
- [ ] Slug PascalCase gerado para cada EJB, sem duplicação.
- [ ] Tipo classificado (Stateless / Stateful).
- [ ] Interface Local/Remote identificada quando existir.
- [ ] Numeração sequencial atribuída (3 dígitos, sem lacunas novas).
- [ ] Status verificado: 🟢 para EJBs com artefato gerado, 🔴 para pendentes.
- [ ] `EJB-CATALOGO.md` gerado em `{paths.discovery}/`.
- [ ] Totais (documentados / pendentes) registrados no cabeçalho.

---

## 9. Como iniciar a documentação individual

Após gerar o catálogo, documente cada EJB chamando a skill `discovery-51-ejb`:

```
@discovery-50-backend documentar EJB-001
```
