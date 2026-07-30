# Mapa Consolidado de Fluxos, Telas, Endpoints e Tabelas

Este documento é gerado automaticamente pela skill **discovery-80-consolidacao**.

## Visão Geral

- Cada seção apresenta a relação cruzada entre fluxos, telas, endpoints e tabelas.
- Hiperlinks facilitam a navegação entre artefatos.

---

## Fluxos e suas dependências

| Fluxo | Telas | Endpoints | Tabelas |
|-------|-------|-----------|---------|
| [CF-001](../../discovery/DISC-03-CATALOGO-DE-FLUXOS.md#cf-001) | [TELA-010](../../discovery/TELA-010-AtendimentoPessoaSup.md), [TELA-012](../../discovery/TELA-012-CriarFluxoProcesso.md) | `/api/processo`, `/api/fluxo` | `processo`, `processo_fluxo` |
| ...   | ...   | ...       | ...     |

## Telas e suas dependências

| Tela | Fluxos | Endpoints | Tabelas |
|------|--------|-----------|---------|
| [TELA-010](../../discovery/TELA-010-AtendimentoPessoaSup.md) | CF-001 | `/api/processo` | `processo`, `processo_fluxo` |
| ...  | ...    | ...       | ...     |

## Endpoints e suas dependências

| Endpoint | Telas | Tabelas |
|----------|-------|---------|
| `/api/processo` | TELA-010, TELA-012 | `processo`, `processo_fluxo` |
| ...      | ...   | ...     |

## Tabelas e suas dependências

| Tabela | Telas | Endpoints | Fluxos |
|--------|-------|-----------|--------|
| `processo` | TELA-010, TELA-012 | `/api/processo` | CF-001 |
| ...    | ...   | ...       | ...    |

---

> Atualize este documento executando a skill sempre que houver mudanças relevantes.
