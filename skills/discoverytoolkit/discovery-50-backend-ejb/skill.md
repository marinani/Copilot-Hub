---
name: discovery-50-backend
description: Roteador de skills do grupo discovery-50-backend. Documenta a camada de negócio (EJBs @Stateless/@Stateful) do sistema. Execute em pipeline: catalogo-ejb → ejb (um por invocação). PRÉ-REQUISITO: discovery-10-banco deve estar executado — as fichas de DADOS-10 são a fonte de verdade das regras de negócio. Paralelo ao discovery-40-interface. Quando o usuário pedir para "executar o backend" ou "executar o discovery backend", execute as skills na sequência abaixo.
---

# Skill Router — discovery-50-backend

Este roteador documenta a camada de serviço/negócio do sistema: Session Beans EJB (`@Stateless` e `@Stateful`).

> **Posição na sequência:** Passo 3b — após `discovery-10-banco`, paralelo ao `discovery-40-interface`, antes de `discovery-20-fluxos`.
> Os fluxos industriais lêem os `EJB-*.md` para preencher:
> - Seção 5 (Regras de negócio) — RN-EJB-* e RN-SP-* dos EJBs chamados
> - Seção 11 (Integrações) — EJBs invocados pelo fluxo
> - Seção 14.3 (Rastreabilidade) — artefatos EJB como referência

## Skills disponíveis

| Skill                        | Descrição resumida                                                                          |
|------------------------------|---------------------------------------------------------------------------------------------|
| discovery-50-catalogo-ejb    | Varre o legado e gera/atualiza EJB-CATALOGO.md com numeração sequencial EJB-{NNN}          |
| discovery-51-ejb             | Documenta UM EJB por invocação: objetivo, métodos, RN, dependências, Mermaid, Gherkin, NFR |

## Saídas que alimentam os Fluxos

- `EJB-CATALOGO.md` — índice mestre de EJBs com status de documentação
- `EJB-{NNN}-{PascalCase}.md` — documentação individual por EJB

## Execução automática em sequência

Quando o usuário pedir para **executar o backend** ou **executar o discovery backend**, execute as skills nesta ordem, uma após a outra, sem pular etapas:

### Passo 1 — Catálogo de EJBs
Leia e execute integralmente as instruções de `discovery-50-catalogo-ejb.md`.
Aguarde a geração de `EJB-CATALOGO.md` antes de prosseguir.

### Passo 2 — Documentação individual
Para cada EJB com status 🔴 pendente no catálogo:
Leia e execute integralmente as instruções de `discovery-51-ejb.md`.
Documente um EJB por vez; aguarde a conclusão e a atualização do status no catálogo antes de avançar ao próximo.

## Como usar manualmente

- Para catalogar: `@discovery-50-backend catalogar EJBs`
- Para documentar um EJB específico: `@discovery-50-backend documentar EJB-001`
- Para rodar o pipeline completo: `executar o backend`

---

> Consulte cada skill individual para detalhes de uso, parâmetros e restrições.
