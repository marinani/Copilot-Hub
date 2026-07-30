# discovery-80-consolidacao

## Objetivo
Consolidar e cruzar informações de fluxos, telas, endpoints e tabelas do Discovery Toolkit, gerando:
- JSON estruturado para automação e consumo por outras skills
- Markdown (.md) documentado para consulta de analistas e devs
- Base para geração de hyperlinks e navegação entre artefatos

## Funcionalidades
- Varredura automática dos arquivos de fluxo (CF-XXX), tela (TELA-XXX), endpoints e tabelas
- Geração de matriz cruzada:
  - Fluxo → Telas, Endpoints, Tabelas
  - Tela → Fluxos, Endpoints, Tabelas
  - Endpoint → Telas, Tabelas
  - Tabela → Telas, Endpoints, Fluxos
- Exportação em JSON e Markdown
- Inclusão de hyperlinks para navegação

## Exemplo de saída (Markdown)

| Fluxo   | Telas Relacionadas | Endpoints | Tabelas |
|---------|--------------------|-----------|---------|
| [CF-001](../../discovery/DISC-03-CATALOGO-DE-FLUXOS.md#cf-001) | [TELA-010](../../discovery/TELA-010-AtendimentoPessoaSup.md), [TELA-012](../../discovery/TELA-012-CriarFluxoProcesso.md) | `/api/processo`, `/api/fluxo` | `processo`, `processo_fluxo` |

## Observações
- A skill deve ser reexecutada sempre que houver alteração relevante em fluxos, telas, endpoints ou tabelas.
- O JSON gerado deve ser compatível para uso por outras skills (ex: geração de HTML, análise de impacto, etc).
- O Markdown deve ser claro, navegável e útil para analistas e desenvolvedores.

---

> Skill inicial — Estrutura e escopo definidos. Implementação do parser e gerador de matriz cruzada a seguir.
